# 图像坐标定位工具

在一些工作中我需要知道图像中某个位置的像素坐标值，每次都需要用Matlab中的数据游标来获取，这个过程繁琐且费时间，于是我编写了一个专门用来显示像素坐标的小工具；

只需要在想得到坐标值的位置按下鼠标右键即可得到该点的像素坐标值；

这个工具使用python3.7编写，使用Tkinter选取图像路径，OpenCV实现鼠标事件和界面显示。

# Show-Image-Coordinates

In some works I need to know the pixel coordinates value of a certain position in the image, I have to use the data cursor in Matlab to get it every time, it can be very distracting. As a solution to this problem, I have written a tool dedicated to displaying image pixel coordinates. 

You can get the coordinates of the pixel by clicking the right mouse button at anywhere you want.

This widget written in python 3.7. Tkinter is used for image path selection and OpenCV is used for implementing mouse events and interface.
