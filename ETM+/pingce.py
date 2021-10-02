import cv2
import numpy as np
import matplotlib.pyplot as plt
import time
import math

img=cv2.imread(r'E:\pingce\hdtd1.tif')      #修复后
img0=cv2.imread(r'C:\Users\Hoshino Shen\Desktop\chong1.tif')     #辅助图像

#把两张图片转成灰度图片
img0=cv2.cvtColor(img0,cv2.COLOR_BGR2GRAY)
img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)


#求得RMSE

row,col=img.shape               #获取修复图像像素点的宽度和高度
d=[]
'''for i in range(row):
    for j in range(col):
        s=img0[i,j]-img[i,j]
        d.append(s) '''         #获取全部的di

s1=[]           #原图灰度值
s2=[]           #修复后灰度值
for i in range(row):
    for j in range(col):
        s=img0[i,j]
        s1.append(s)

for i in range(row):
    for j in range(col):
        s=img[i,j]
        s2.append(s)

for i in s1:
        s=i*i-s2[s1.index(i)]*s2[s1.index(i)]
        d.append(s)

sum1=sum(d)
RMSE=math.sqrt(sum1/img.size)
print(RMSE)