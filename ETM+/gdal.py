import numpy as np
import cv2
import time
from PIL import Image
'''class Sketcher:
    def __init__(self, windowname, dests, colors_func):
        self.prev_point = None
        self.windowname = windowname
        # dests is a set of images: copy & mask
        self.dests = dests
        self.colors_func = colors_func
        self.dirty = False
        self.show()
        cv.setMouseCallback(self.windowname, self.on_mouse)

    def show(self):
        cv2.imshow(self.windowname, self.dests[0])
        cv2.imshow(self.windowname + ":mask", self.dests[1])

    # on mouse function
    def on_mouse(self, event, x, y, flags, param):
        # point store the current position of the mouse
        point = (x, y)
        if event == cv2.EVENT_LBUTTONDOWN:
            # assignment of previous point
            self.prev_point = point
        elif event == cv2.EVENT_LBUTTONUP:
            self.prev_point = None
        # cv.EVENT_FLAG_LBUTTON & flags 代表按住左键拖拽
        if self.prev_point and flags & cv2.EVENT_FLAG_LBUTTON:
            # zip 把前后参数打包为元组
            for dst, color in zip(self.dests, self.colors_func()):
                cv2.line(dst, self.prev_point, point, color, 5)
                # Record this dirt
            self.dirty = True
            self.prev_point = point
            self.show()
'''
# 读取图片
img = cv2.imread(r'C:\Users\Hoshino Shen\Desktop\try1019.tif')
#img1= cv2.imread(r'C:\Users\Hoshino Shen\Desktop\123.png')
#遍历图片像素
'''img2 = np.copy(img)
rows,cols = img2.shape[:2]
for row in range(rows):
    for col in range(cols):
        img[row,col] = 255 - img[row,col]'''

# 图像转换为灰度图像
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 灰度二值化
_, mask = cv2.threshold(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), 10, 255, cv2.THRESH_BINARY_INV)
# _,mask = cv2.threshold(gray,10,255,cv2.THRESH_BINARY_INV)
# mask1 = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
dst = cv2.inpaint(img,mask,20,cv2.INPAINT_TELEA)
dst1 = cv2.inpaint(dst,mask,20,cv2.INPAINT_TELEA)
# dst = cv2.inpaint(img, mask, 10, cv2.INPAINT_NS)



'''def main():
    print("Usage: python inpaint <image_path>")
    print("Keys: ")
    print("t - inpaint using FMM")  # Fast Marching method
    print("n - inpaint using NS technique")
    print("r - reset the inpainting mask")
    print("ESC - exit")

    # Read image in color mode
    img_h = dst1

    # Return error if failed to read the image
    if img_h is None:
        print("Failed to read the image")
        return

    # Create the copy of the original image
    img_mask = img_h.copy()

    # Create a black mask of the image
    inpaintMask = np.zeros(img_h.shape[:2], np.uint8)
    # Create a Sketch
    # dests= img_mask, inpaintMask
    # color_func is a tuple : white with BGR and white on gray
    sketch = Sketcher('image', [img_mask, inpaintMask], lambda: ((255, 255, 255), 255))

    while True:
        ch = cv2.waitKey()
        # Esc
        if ch == 27:
            break

        if ch == ord('t'):
            t1 = time.time()
            res = cv2.inpaint(src=img_mask, inpaintMask=inpaintMask, inpaintRadius=3, flags=cv2.INPAINT_TELEA)
            res = np.hstack((img, res))
            t2 = time.time()
            print("Time: FMM = {} ms".format((t2 - t1) * 1000))
            cv2.imshow('Inpaint with FMM', res)
            cv2.imwrite("FMM-eye.png", res)

        if ch == ord('n'):
            t1 = time.time()
            res = cv2.inpaint(src=img_mask, inpaintMask=inpaintMask, inpaintRadius=3, flags=cv2.INPAINT_NS)
            res = np.hstack((img, res))
            t2 = time.time()
            cv2.imshow('Inpaint Output using NS Technique', res)
            cv2.imwrite("NS-eye.png", res)
        # type r to reset the image
        if ch == ord('r'):
            # The reason for which we copied image
            img_mask[:] = img
            inpaintMask[:] = 0
            sketch.show()

    print('Completed')'''

# 均值滤波
dst2 = cv2.blur(dst, (3,3))

#展示图像
cv2.imshow('img0', img)
# cv2.imshow('img10',mask1)
cv2.imshow('img1', mask)
cv2.imshow('img2', dst)
cv2.imshow('img3', dst1)
cv2.imshow('img4', dst2)
cv2.waitKey(0)
cv2.destroyAllWindows()