import cv2
import numpy as np
import matplotlib.pyplot as plt
import time

img0=cv2.imread(r'C:\Users\Hoshino Shen\Desktop\kong.tif')      #原图待修复
scr=cv2.imread(r'C:\Users\Hoshino Shen\Desktop\chong.tif')     #目标图填充图像

#把两张图片转成灰度图片
img0=cv2.cvtColor(img0,cv2.COLOR_BGR2GRAY)
scr=cv2.cvtColor(scr,cv2.COLOR_BGR2GRAY)
img=img0.copy()                                                 #做对比图

#映射列表
mHist1=[]           #各个灰度值像素个数
mNum1=[]            #累计灰度直方图（频率）
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
        mHist1[img[i,j]]=mHist1[img[i,j]]+1    #统计各灰度值的个数
mNum1.append(mHist1[0]/img.size)


for i in range(0, 255):
    mNum1.append(mNum1[i]+mHist1[i+1]/img.size)
print(mNum1[0])

for i in range(256):
    inhist1.append(round(255*mNum1[i]))

# 对填充图像进行均衡化
for i in range(256):
    mHist2.append(0)
rows,cols=scr.shape               #获取填充图像像素点的宽度和高度

for i in range(rows):
    for j in range(cols):
        mHist2[scr[i,j]]=mHist2[scr[i,j]]+1     #统计灰度值的个数

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
            b=abs(inhist2[j]-a)
            if b<minp:
                minp=b
                jmin=j
        g.append(jmin)

for i in range(row):        #读成图像
    for j in range(col):
        img[i,j]=g[img[i,j]]


#直方图匹配均值算法
avg1=0
for i in range(row):
    for j in range(col):
        avg1+=img0[i,j]/img0.size     #得出待修复图像匹配后灰度均值
print(avg1)

avg2=0
for i in range(row):
    for j in range(col):
        avg2+=scr[i,j]/scr.size     #得出填充图像匹配后灰度均值
print(avg2)

for i in range(row):
    for j in range(col):
        if img[i,j]<=9:        #9/63
            img[i,j]=scr[i,j]+(avg1+avg2)/(avg1*avg2)

#直方图匹配中值算法
'''mivlst1=[]      #统计所有灰度值
for i in range(row):
    for j in range(col):
        mivlst1.append(img0[i,j])

mivlst1.sort()

if (row*col)%2:         #求得中值
    t=(row*col+1)/2
    miv1=mivlst1[int(t)]
else:
    t =(row*col)/2
    miv1=(mivlst1[int(t)]+mivlst1[int(t+1)])/2

mivlst2=[]      #统计所有灰度值
for i in range(row):
    for j in range(col):
        mivlst2.append(scr[i,j])

mivlst2.sort()

if (row*col)%2:         #求得中值
    t=(row*col+1)/2
    miv2=mivlst2[int(t)]
else:
    t =(row*col)/2
    miv2=(mivlst2[int(t)]+mivlst2[int(t+1)])/2

print(miv1)
print(miv2)

for i in range(row):
    for j in range(col):
        if img[i,j]<=56:        #9/56
            img[i,j]=scr[i,j]+(miv1-miv2)'''

cv2.imwrite('E:\pingce\qjt.tif',img)

cv2.imshow("img",img)
cv2.imshow("before",img0)
cv2.waitKey(0)
'''plt.hist(img.ravel(),256)
plt.show()'''