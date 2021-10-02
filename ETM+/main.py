import cv2
import numpy as np
import matplotlib.pyplot as plt
import time

img0=cv2.imread(r'C:\Users\Hoshino Shen\Desktop\kong1.tif')      #原图待修复
scr=cv2.imread(r'C:\Users\Hoshino Shen\Desktop\chong1.tif')     #目标图填充图像

#把两张图片转成灰度图片
img0=cv2.cvtColor(img0,cv2.COLOR_BGR2GRAY)
scr=cv2.cvtColor(scr,cv2.COLOR_BGR2GRAY)
img=img0.copy()                                                 #做对比图

#映射列表
mHist1=[]           #各个灰度值像素个数
mNum1=[]            #累计灰度直方图（频率）
inhist1=[]          #比对期望（mNum*255）
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
print(mNum1[84])

for i in range(256):
    inhist1.append(round(255*mNum1[i]))

# 对填充图像进行均衡化

for i in range(256):
    mHist2.append(0)
rows,cols=scr.shape               #获取填充图像像素点的宽度和高度

for i in range(rows):
    for j in range(cols):
        mHist2[scr[i,j]]=mHist2[scr[i,j]]+1         #统计灰度值的个数

mNum2.append(mHist2[0]/scr.size)

for i in range(0,255):
    mNum2.append(mNum2[i]+mHist2[i+1]/scr.size)

for i in range(256):
    inhist2.append(round(255*mNum2[i]))

#直方图匹配
g=[]                               #匹配后的图片像素
for i in range(256):
    a=inhist1[i]
    flag=True
    for j in range(256):
        if inhist2[j]==a:
            g.append(j)
            flag=False
            break
    if flag==True:
        minp=255
        for j in range(256):        #循环求最小差值
            b = abs(inhist2[j]-a)
            if b<minp:
                minp=b
                jmin=j
        g.append(jmin)

for i in range(row):        #读成图像
    for j in range(col):
        img[i,j]=g[img[i,j]]

cv2.imwrite('E:\imgp.tif',img)

imgn=cv2.imread(r'E:\imgp.tif')

#灰度二值化
_, mask=cv2.threshold(cv2.cvtColor(imgn,cv2.COLOR_BGR2GRAY),55,255,cv2.THRESH_BINARY_INV) #9/55
mask=cv2.blur(mask,(2,2))

#dst=cv2.inpaint(img,mask,20,cv2.INPAINT_TELEA)

dst=cv2.inpaint(img,mask,20,cv2.INPAINT_NS)

#dst2=cv2.inpaint(dst,scr,20,cv2.INPAINT_NS)

cv2.imwrite('E:\pingce\hdtd1.tif',dst)

#均值滤波
dst3=cv2.blur(dst,(2,2))

cv2.imshow("before",img0)
cv2.imshow("mask",mask)
cv2.imshow("after",dst)
cv2.imshow("after2",dst3)
cv2.waitKey(0)
plt.hist(dst.ravel(),256)
plt.show()