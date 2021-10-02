from PIL import Image,ImageFilter,ImageDraw,ImageEnhance
import  random
import os
import  numpy as np
from tqdm import tqdm

img_weight = 256
img_height = 256

def file_name(file_path):
    img_name_list = []
    for root,dirs,files in os.walk(file_path):
        for file in files:
            img_name = os.path.split(file)[1]
            img_name_list.append(img_name)
    return img_name_list

img_store_list = file_name(r'C:\Users\Administrator\Desktop\PG1\2019seg\train\src')
# print(img_store_list)

def add_noise(img):
    # length, height, dims = img.shape
    drawObject = ImageDraw.Draw(img)
    for i in range(250):
        tmp_x = np.random.randint(0,img.size[0])
        tmp_y = np.random.randint(0,img.size[1])
        drawObject.point((tmp_x,tmp_y),fill='black')#添加白噪声，噪点颜色可变
    return img

#色调增强
def random_color(img):
    img = ImageEnhance.Color(img)
    img = img.enhance(2)
    return img

def data_augment(row_roi,label_roi):
    #图像标签同时进行90，180，270旋转
    if np.random.random() < 0.25:
        row_roi = row_roi.rotate(90)
        label_roi = label_roi.rotate(90)
    if np.random.random() < 0.25:
        row_roi = row_roi.rotate(180)
        label_roi = label_roi.rotate(180)
    if np.random.random() < 0.25:
        row_roi = row_roi.rotate(270)
        label_roi = label_roi.rotate(270)

    #图像、标签同时竖直旋转
    if np.random.random() < 0.25:
        row_roi = row_roi.transpose(Image.FLIP_LEFT_RIGHT)
        label_roi = label_roi.transpose(Image.FLIP_LEFT_RIGHT)
    #图像、标签同时水平旋转
    if np.random.random() < 0.25:
        row_roi = row_roi.transpose(Image.FLIP_TOP_BOTTOM)
        label_roi = label_roi.transpose(Image.FLIP_TOP_BOTTOM)
    #对图像进行高斯模糊
    if np.random.random() < 0.25:
        row_roi = row_roi.filter(ImageFilter.GaussianBlur)
    #对图像进行色调增强
    if np.random.random() < 0.25:
        row_roi = random_color(row_roi)
    #对图像加噪声
    if np.random.random() < 0.25:
        row_roi = add_noise(row_roi)

    return row_roi,label_roi

def create_dataset(img_nums=100000,mode = 'orginal'):
    print('creating dataset...')
    src_path = r'C:\Users\Administrator\Desktop\PG1\2019seg\train\src'
    label_path = r'C:\Users\Administrator\Desktop\PG1\2019seg\train\label'
    single_img_count = img_nums/len(img_store_list)
    g_count = 0
    le = len(img_store_list)
    for i in tqdm(range(le)):
        count = 0
        row_img_path = src_path + os.sep + img_store_list[i]
        label_img_path = label_path + os.sep + img_store_list[i]
        row_img = Image.open(row_img_path)
        label_img = Image.open(label_img_path)

        while(count<single_img_count):
            w1 = random.randint(0,row_img.size[0] - img_weight)
            h1 = random.randint(0,row_img.size[1] - img_height)
            w2 = w1 + img_weight
            h2 = h1 + img_height

            row_img = row_img.crop((w1,h1,w2,h2))
            label_img = label_img.crop((w1,h1,w2,h2))

            if mode == 'augment':
                row_img,label_img = data_augment(row_img,label_img)
            row_img_store = r'E:\PycharmProjects\ImageProcessing\img_store\train_row\%d.tif' % g_count
            label_img_store = r'E:\PycharmProjects\ImageProcessing\img_store\train_label\%d.tif' % g_count
            print(label_img_store)
            row_img.save(row_img_store)
            label_img.save(label_img_store)

            count += 1
            g_count += 1


if __name__ == '__main__':
    create_dataset(mode='augment')
