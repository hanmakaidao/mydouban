# coding=utf-8
__author__ = 'tech.chao'

from PIL import Image
import pytesseract
from config import filepath

# 容错最大的有色判断
MAX_RGB_VALUE = 20
# 噪点大小
MAX_NOISY_COUNT = 10

# RGBA白色定义
WHITE_COLOR = (255, 255, 255)
# RGBA黑色定义
BLACK_COLOR = (0, 0, 0)


def print_char_pic(width, height, s_data):
    """
    画出字符图, 空格为白色, 点为黑色
    """
    _pic_str = ''
    for y in range(0, height):
        for x in range(0, width):
            _point = s_data[y * width + x]
            if _point == WHITE_COLOR:
                _pic_str += ' '
            else:
                _pic_str += '*'
        _pic_str += '\n'

    print(_pic_str)


def gen_white_black_points(image):
    """
    根据点阵颜色强制转换黑白点
    """
    data = image.getdata()
    new_data = []
    for item in data:
        if item[0] > MAX_RGB_VALUE and item[1] > MAX_RGB_VALUE and item[2] > MAX_RGB_VALUE:
            new_data.append(WHITE_COLOR)
        else:
            new_data.append(BLACK_COLOR)
    return new_data


def pre_concert(img):
    width,height = img.size
    threshold = 25
    for i in range(0,width):
        for j in range(0,height):
            p = img.getpixel((i,j))#抽取每个像素点的像素
            r,g,b = p
            if r > threshold or g > threshold or b > threshold:
                img.putpixel((i,j),WHITE_COLOR)
            else:
                img.putpixel((i,j),BLACK_COLOR)
    # img.show()
    # img.save("pre_fig.jpg")
    return img

# 对去除背景的图片做噪点处理
def remove_noise(self, window=1):
    if window == 1:
        window_x = [1, 0, 0, -1, 0]
        window_y = [0, 1, 0, 0, -1]
    elif window == 2:
        window_x = [-1, 0, 1, -1, 0, 1, 1, -1, 0]
        window_y = [-1, -1, -1, 1, 1, 1, 0, 0, 0]

    width, height = self.size
    for i in range(width):
        for j in range(height):
            box = []

            for k in range(len(window_x)):
                d_x = i + window_x[k]
                d_y = j + window_y[k]
                try:
                    d_point = self.getpixel((d_x, d_y))
                    if d_point == BLACK_COLOR:
                        box.append(1)
                    else:
                        box.append(0)
                except IndexError:
                    self.putpixel((i, j), WHITE_COLOR)
                    continue

            box.sort()
            if len(box) == len(window_x):
                mid = box[int(len(box) / 2)]
                if mid == 1:
                    self.putpixel((i, j), BLACK_COLOR)
                else:
                    self.putpixel((i, j), WHITE_COLOR)
    # self.show()
    # self.save("mov_noise_fig.jpg")
    return self

def reduce_noisy(width, height, points):
    """
    横向扫描, 获取最大边界大小. 除去小于最大噪点大小的面积.
    """
    # 标记位置, 初始化都是0, 未遍历过
    flag_list = []
    for i in range(width * height):
        flag_list.append(0)

    # 遍历
    for index, value in enumerate(points):
        _y = index // width
        _x = index - _y * width
        # print _x, _y
        if flag_list[index] == 0 and value == BLACK_COLOR:
            flag_list[index] = 1
            _tmp_list = [index]
            recursion_scan_black_point(_x, _y, width, height, _tmp_list, flag_list, points)
            if len(_tmp_list) <= MAX_NOISY_COUNT:
                for x in _tmp_list:
                    points[x] = WHITE_COLOR

        else:
            flag_list[index] = 1


def recursion_scan_black_point(x, y, width, height, tmp_list, flag_list, points):
    # 左上
    if 0 <= (x - 1) < width and 0 <= (y - 1) < height:
        _x = x - 1
        _y = y - 1
        _inner_recursion(_x, _y, width, height, tmp_list, flag_list, points)

    # 上
    if 0 <= (y - 1) < height:
        _x = x
        _y = y - 1
        _inner_recursion(_x, _y, width, height, tmp_list, flag_list, points)

    # 右上
    if 0 <= (x + 1) < width and 0 <= (y - 1) < height:
        _x = x + 1
        _y = y - 1
        _inner_recursion(_x, _y, width, height, tmp_list, flag_list, points)

    # 左
    if 0 <= (x - 1) < width:
        _x = x - 1
        _y = y
        _inner_recursion(_x, _y, width, height, tmp_list, flag_list, points)

    # 右
    if 0 <= (x + 1) < width:
        _x = x + 1
        _y = y
        _inner_recursion(_x, _y, width, height, tmp_list, flag_list, points)

    # 左下
    if 0 <= (x - 1) < width and 0 <= (y + 1) < height:
        _x = x - 1
        _y = y + 1
        _inner_recursion(_x, _y, width, height, tmp_list, flag_list, points)

    # 下
    if 0 <= (y + 1) < height:
        _x = x
        _y = y + 1
        _inner_recursion(_x, _y, width, height, tmp_list, flag_list, points)

    # 右下
    if 0 <= (x + 1) < width and 0 <= (y + 1) < height:
        _x = x + 1
        _y = y + 1
        _inner_recursion(_x, _y, width, height, tmp_list, flag_list, points)


def _inner_recursion(new_x, new_y, width, height, tmp_list, flag_list, points):
    _index = new_x + width * new_y
    if flag_list[_index] == 0 and points[_index] == BLACK_COLOR:
        tmp_list.append(_index)
        flag_list[_index] = 1
        recursion_scan_black_point(new_x, new_y, width, height, tmp_list, flag_list, points)
    else:
        flag_list[_index] = 1


def recognize_url(url):
    import urllib
    # urllib.urlretrieve(url, "imgs/tmp-img.jpg")
    img=url
    rebuildimg=filepath.image_path+"rebuild.jpg"
    img = Image.open(img)
    img = img.convert('RGB')
    w, h = img.size[0], img.size[1]
    # print w, h
    # point_list = gen_white_black_points(img)
    # print_char_pic(w, h, point_list)
    # reduce_noisy(w, h, point_list)
    remove_noise(pre_concert(img))
    # print_char_pic(w, h, point_list)

    # img.putdata(point_list)
    img.save(rebuildimg)
    # text=pytesseract.image_to_string(Image.open(rebuildimg))
    return rebuildimg

if __name__ == '__main__':
    #img = Image.open('imgs/captcha-1.jpg')
    # img = img.convert('RGBA')
    # w, h = img.size[0], img.size[1]
    # print w, h
    # point_list = gen_white_black_points(img)
    # print_char_pic(w, h, point_list)
    # reduce_noisy(w, h, point_list)
    # print_char_pic(w, h, point_list)
    #
    #
    # img.putdata(point_list)
    # img.save("imgs/rebuild.jpg")
    #
    # print pytesseract.image_to_string(Image.open('imgs/rebuild.jpg'))
    print(recognize_url('3c94e251474ef1ac72cd9760675d8eb7.jpg'))