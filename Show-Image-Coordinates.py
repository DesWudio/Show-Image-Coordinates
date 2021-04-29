import tkinter
import tkinter.filedialog
from tkinter import messagebox
from cv2 import cv2
import os
import time

# 全局变量
global zoom_gloabl
zoom_gloabl = 1 # 当前缩放倍数
location_win_inside = [0, 0]  # 窗口左上角位于图像中的坐标
zoom_Scale = 0.1  # 缩放尺度（速度）

# Tkinter选取图像
default_dir = r"文件路径"
fname = tkinter.filedialog.askopenfilename(
    title=u'选择文件', initialdir=(os.path.expanduser((default_dir))))
if fname == "":
    messagebox.showinfo("错误", "未选择有效图像，程序将退出!")
    os._exit(0)
print('选择文件路径为:\n %s \n' % fname)

size_org = cv2.imread(fname)  # 原始图像
size_zoomed = size_org.copy()  # 缩放前倍数

# 判断变量是否被定义
def isset(v):
    try:
        type(eval(v))
    except:
        return 0
    else:
        return 1

# 刷新窗口显示
global xx, yy  # 图像相对窗口的位置（窗口左上角在图像的坐标位置）
xx = 0  # 初始状态下，窗口左上角与图像原点重合
yy = 0
def check_location(img_size, win_size_rectify, win_insideimg): # 图像尺寸, 窗口尺寸,窗口在图像中的位置
    for i in range(2):
        if win_insideimg[i] < 0:
            win_insideimg[i] = 0
        elif win_insideimg[i] + win_size_rectify[i] > img_size[i] and img_size[i] > win_size_rectify[i]:
            win_insideimg[i] = img_size[i] - win_size_rectify[i]
        elif win_insideimg[i] + win_size_rectify[i] > img_size[i] and img_size[i] < win_size_rectify[i]:
            win_insideimg[i] = 0
    # print(img_size, win_size_rectify, win_insideimg)
    xx = win_insideimg[0]
    yy = win_insideimg[1]

# 计算缩放倍数
# 滚轮状态, 缩放速度, 当前倍数
def count_zoom(flag, step, zoom):
    if flag > 0:  # 滚轮上移
        zoom += step
        if zoom > 1 + step * 40:  # max 5x
            zoom = 1 + step * 40
    else:  # 滚轮下移
        zoom -= step
        if zoom < step:  # 最多只能缩小到0.1倍
            zoom = step
    zoom = round(zoom, 2)  # 取2位有效数字
    return zoom

# 鼠标事件
def mouse(event, x, y, flags, param):
    global location_click, location_release, img_plot, size_zoomed, location_win_inside, location_win, zoom_gloabl
    if event == cv2.EVENT_LBUTTONDOWN:  # 左键按下
        location_click = [x, y]  # 此时以窗口为基准鼠标的坐标
        location_win = [location_win_inside[0], location_win_inside[1]]
    # 左键拖曳
    elif event == cv2.EVENT_MOUSEMOVE and (flags & cv2.EVENT_FLAG_LBUTTON):
        location_release = [x, y]  # 此时以窗口为基准鼠标的坐标
        h1, w1 = size_zoomed.shape[0:2]  # 缩放后图像尺寸
        w2, h2 = win_size  # 窗口尺寸
        show_wh = [0, 0]  # 图像显示尺寸
        if w1 < w2 and h1 < h2:  # 图像尺寸小于窗口尺寸，拖拽无效
            show_wh = [w1, h1]
            location_win_inside = [0, 0]
        elif w1 >= w2 and h1 < h2:  # 仅图像宽大于窗宽，可左右拖拽
            show_wh = [w2, h1]
            location_win_inside[0] = location_win[0] + \
                location_click[0] - location_release[0]
        elif w1 < w2 and h1 >= h2:  # 仅图像高大于窗口高，可上下拖拽
            show_wh = [w1, h2]
            location_win_inside[1] = location_win[1] + \
                location_click[1] - location_release[1]
        else:  # 图像尺寸大于窗口尺寸，所有方向拖拽有效
            show_wh = [w2, h2]
            location_win_inside[0] = location_win[0] + \
                location_click[0] - location_release[0]
            location_win_inside[1] = location_win[1] + \
                location_click[1] - location_release[1]
        check_location([w1, h1], [w2, h2], location_win_inside)  # 刷新窗口显示
        img_plot = size_zoomed[location_win_inside[1]:location_win_inside[1] + show_wh[1],
                               location_win_inside[0]:location_win_inside[0] + show_wh[0]]  # 实际显示的图像

    elif event == cv2.EVENT_RBUTTONDOWN:  # 当鼠标右键点击时
        # xy = "x= %d,y= %d" %(x, y)
        # print(xy)
        # cv2.circle(img_plot, (x, y), 1, (255, 0, 0), thickness = -1)
        # cv2.putText(img_plot, xy, (x, y), cv2.FONT_HERSHEY_PLAIN, 1.0, (0,0,0), thickness = 1)
        if isset('xx'):  # 如果发生了位置移动，即图像左上角坐标不是0，0
            xi = int(x) + xx  # 使用图像左上角坐标x值 + 当前显示图像中所选点坐标x值
            # print(xx)
            yi = int(y) + yy  # y同上
            # print(yy)
            xi /= zoom_gloabl  # opencv放大图像会插值，所以需要按照放大倍数比例计算原图中像素坐标位置
            yi /= zoom_gloabl
            print("x=", xi, "y=", yi, "\n")
            pointinfo = "x= %(x)s y= %(y)s" % {'x': xi, 'y': yi}
            messagebox.showinfo("该点相对图像原点的绝对坐标", pointinfo)
            time.sleep(0)
        else:
            xi = xx
            yi = yy
            xi /= zoom_gloabl
            yi /= zoom_gloabl
            print("x=", x, "y=", y, "\n")
            pointinfo0 = "x= %(x)s y= %(y)s" % {'x': x, 'y': y}
            messagebox.showinfo("该点相对图像原点的绝对坐标", pointinfo0)

    elif event == cv2.EVENT_MOUSEWHEEL:  # 滚轮
        z = zoom_gloabl  # 缩放前的缩放倍数，用于计算缩放后窗口在图像中的位置
        zoom_gloabl = count_zoom(flags, zoom_Scale, zoom_gloabl)  # 计算缩放倍数
        print('zoom= %s' % zoom_gloabl)
        w1, h1 = [int(size_org.shape[1] * zoom_gloabl),
                  int(size_org.shape[0] * zoom_gloabl)]  # 缩放图像的尺寸
        w2, h2 = win_size  # 窗口的尺寸
        size_zoomed = cv2.resize(
            size_org, (w1, h1), interpolation=cv2.INTER_AREA)  # 图像缩放
        show_wh = [0, 0]  # 实际显示图像的尺寸
        if w1 < w2 and h1 < h2:  # 缩放后，图像尺寸小于窗口尺寸
            show_wh = [w1, h1]
            cv2.resizeWindow(win, w1, h1)
        elif w1 >= w2 and h1 < h2:  # 缩放后，图像高度小于窗口高度
            show_wh = [w2, h1]
            cv2.resizeWindow(win, w2, h1)
        elif w1 < w2 and h1 >= h2:  # 缩放后，图像宽度小于窗口宽度
            show_wh = [w1, h2]
            cv2.resizeWindow(win, w1, h2)
        else:  # 缩放后，图像尺寸大于窗口尺寸
            show_wh = [w2, h2]
            cv2.resizeWindow(win, w2, h2)
        location_win_inside = [int((location_win_inside[0] + x) * zoom_gloabl / z - x), int(
            (location_win_inside[1] + y) * zoom_gloabl / z - y)]  # 缩放后，窗口在图像的位置
        check_location([w1, h1], [w2, h2], location_win_inside)  # 矫正窗口在图像中的位置
        # print(location_win_inside, show_wh)
        # 窗口显示内容
        img_plot = size_zoomed[location_win_inside[1]:location_win_inside[1] + show_wh[1],
                               location_win_inside[0]:location_win_inside[0] + show_wh[0]]
    cv2.imshow(win, img_plot)

# 图像显示所需定义
win_size = [800, 600]
location_win = [0, 0]  # 按下鼠标前窗口左上角位于图像中的坐标
location_click, location_release = [0, 0], [0, 0]  # 以窗口为参考，鼠标左键点击和释放的位置

img_plot = size_org[location_win_inside[1]:location_win_inside[1] + win_size[1],
                    location_win_inside[0]:location_win_inside[0] + win_size[0]]  # 窗口中显示的图像

# 窗口显示
win = "hold down to drag, scroll to zoom, right click to show the coordinates"
cv2.namedWindow(win, cv2.WINDOW_NORMAL)
cv2.resizeWindow(win, win_size[0], win_size[1])
cv2.moveWindow(win, 700, 100)
cv2.setMouseCallback(win, mouse)
cv2.waitKey()
cv2.destroyAllWindows()