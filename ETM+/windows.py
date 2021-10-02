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
print(mNum1[84])

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


#自动化区域直方图匹配均值算法
tboth=0
winh=0      #窗口绝对位置横坐标
winv=0      #窗口绝对位置纵坐标
line=0
newline=0
wflag=0
tflag=0

while not wflag:
    #确定窗口位置、窗口宽度以匹配
    for winw in range(25,row+1):
        if tflag==0:
            if winh + winw < row:
                for i in range(winv,winh+winw):
                    for j in range(winh,winh+winw):
                        if img[i,j]>=10 and img0[i,j]>=10:
                            tboth=tboth+1
                        if tboth==196:
                            tflag=1
                            break
                    if tflag:
                        break
                else:
                    continue
            else:
                print("test1")
                winw=row-winh-1
                newline=1
                break
        else:
            tflag=0
            break

    #窗口内匹配
    avg1=0
    for i in range(winv,winv+winw-1):
        for j in range(winh,winh+winw-1):
            avg1+=img0[i,j]/(winw*winw)     #得出待修复图像窗口内灰度均值

    avg2=0
    for i in range(winv,winv+winw-1):
        for j in range(winh,winh+winw-1):
            avg2+=scr[i,j]/(winw*winw)      #得出填充图像窗口内灰度均值

    for i in range(winv,winv+winw-1):
            for j in range(winh,winh+winw-1):
                if img[i,j]<=9:
                    img[i,j]=scr[i,j]+(avg1-avg2)
                if i==row-2 and j==row-2:
                    wflag==1

    if newline==0:
        winh=winh+winw

    else:
        winh=0
        line+=1
        winv=winv+winw
        newline=0



cv2.imwrite('E:\pingce\hdpj.tif',img)

cv2.imshow("img",img)
cv2.imshow("before",img0)
cv2.waitKey(0)
plt.hist(img.ravel(),256)
plt.show()