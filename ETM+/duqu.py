import cv2
from os import gdal
from osg import gdal_array as ga
import os,math,ogr,osr

def cv2_repair(tif_name):
    # 读取tif影像
    tif_data = gdal_array.LoadFile(tif_name).astype('float32')

    # 获取掩膜
    mask = tif_data.sum(axis=0)
    mask = (mask == 0).astype(np.uint8)

    bands = tif_data.shape[0]

    res = []
    for i in tqdm(range(bands)):
        # cv.Inpaint(src, inpaintMask, dst, inpaintRadius, flags)
        # src：源图像，可以是8位、16位无符号整型和32位浮点型1通道或者8位无符号3通道
        # inpaintMask：掩膜，8位无符号整型
        # dst：和源图像具有一样大小的输出
        # inpaintRadius：算法考虑的每个已修复点的圆形邻域的半径     # flags：修复算法类型，可选cv2.INPAINT_NS和cv2.INPAINT_TELEA

        repaired = cv2.inpaint(tif_data[i], mask, 3, flags=cv2.INPAINT_TELEA)
        res.append(repaired)

    return np.array(res)

if __name__=="__main__":
    tif_name="E:\yun1.tif"
    cv2_repair(tif_name)