import os
import cv2
import string
import random

MAX_WIDTH = 350
MAX_HEIGHT = 100


def handle_image(img_path):
    # 读取图片
    img = cv2.imread(img_path)
    # 将图片转化成灰度图
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # 将灰度图转化成二值图，像素值超过127的都会被重新赋值成255
    ret, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    return binary


def main():
    # 得到二值图
    img = handle_image("G:\\ts03\\me.jpg")
    img = cv2.resize(img, (MAX_WIDTH, MAX_HEIGHT))
    height, width = img.shape
    chars = string.ascii_letters + string.digits + r'~!@#$%^&*()_+{}[]\|><./'
    # 转化成列表
    chars = list(chars)
    # 遍历图像
    with open("G:\\ts03\\me.txt", 'w', encoding='utf-8') as f:
        for row in range(0, height):
            for col in range(0, width):
                if img[row][col] == 0:
                    ch = random.choice(chars)
                    f.write(ch)
                else:
                    f.write(' ')
            f.write('*\n')


if __name__ == '__main__':
    main()