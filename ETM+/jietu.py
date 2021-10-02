import cv2 as cv

#图1
src=cv.imread('E:\sheji\chong.tif')
print(src.shape)
cropImg=src[1497:2110,3230:3843]

cv.imwrite("E:\sheji\chong1.tif",cropImg)
print(cropImg.shape)

#图二
src=cv.imread('E:\sheji\kong.tif')
print(src.shape)
cropImg=src[1485:2098,3411:4024]

cv.imwrite("E:\sheji\kong1.tif",cropImg)
print(cropImg.shape)