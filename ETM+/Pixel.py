import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

path='E:\\yun1.tif'
img=Image.open(path)
re_img=np.asarray(img)

for i in range(55):
    for j in range(440):
        re_img[i,j]=0

Image.fromarray(np.uint8(re_img))
pil.show('111',Image)

