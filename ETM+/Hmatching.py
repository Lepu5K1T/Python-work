import cv2
import numpy as np
import matplotlib.pyplot as plt

img0=cv2.imread(r'C:\Users\Hoshino Shen\Desktop\yun1.tif')      #原图待修复
scr=cv2.imread(r'C:\Users\Hoshino Shen\Desktop\chong1.tif')     #目标图填充图像

#把两张图片转成灰度图片
img0=cv2.cvtColor(img0,cv2.COLOR_BGR2GRAY)
img=img0.copy()                                                 #做对比图
scr=cv2.cvtColor(scr,cv2.COLOR_BGR2GRAY)

#映射列表
mHist1=[]
mNum1=[]
inhist1=[]
mHist2=[]
mNum2=[]
inhist2=[]

# 对修复图像进行均衡化
for i in range(256):
    mHist1.append(0)
row,col=img.shape               #获取修复图像像素点的宽度和高度

for i in range(row):
    for j in range(col):
        mHist1[img[i,j]]=mHist1[img[i,j]]+1    #统计灰度值的个数
mNum1.append(mHist1[0]/img.size)

for i in range(0, 255):
    mNum1.append(mNum1[i]+mHist1[i+1]/img.size)

for i in range(256):
    inhist1.append(round(255*mNum1[i]))

# 对填充图像进行均衡化
for i in range(256):
    mHist2.append(0)
rows,cols=scr.shape               #获取填充图像像素点的宽度和高度

for i in range(rows):
    for j in range(cols):
        mHist2[scr[i,j]]=mHist2[scr[i,j]]+1       #统计灰度值的个数

mNum2.append(mHist2[0]/scr.size)

for i in range(0, 255):
    mNum2.append(mNum2[i]+mHist2[i+1]/scr.size)

for i in range(256):
    inhist2.append(round(255*mNum2[i]))

#直方图匹配
g = []                               #用于放入规定化后的图片像素
for i in range(256):
    a = inhist1[i]
    flag=True
    for j in range(256):
        if inhist2[j]==a:
            g.append(j)
            flag=False
            break
    if flag==True:
        minp=255
        for j in range(256):
            b = abs(inhist2[j] - a)
            if b<minp:
                minp=b
                jmin=j
        g.append(jmin)

for i in range(row):
    for j in range(col):
        img[i,j]=g[img[i,j]]

cv2.imwrite('E:\imgp.tif', img)



cv2.imshow("after",img)
cv2.waitKey(0)
plt.hist(img0.ravel(),256)
plt.show()