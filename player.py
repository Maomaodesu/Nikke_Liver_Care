import os
import random
import time
import math
import cv2
import numpy
import pyautogui
from PIL import ImageGrab

cwd = __file__.replace('player.py', '')  # cwd: 获取当前脚本文件的目录。
img_path = f'{cwd}\\img'  # 目标图片目录


# 初始化图片字典

# 初始化图片字典
def load_img_dictionary():
    img_dictionary = {}
    file_list = os.listdir(img_path)
    for file in file_list:
        name = file.split('.')[0]
        file_path = img_path + '/' + file
        content = [cv2.imread(file_path), name]
        img_dictionary[name] = content
    return img_dictionary


# 截图并转化为截图多维数组
def get_screen_nd_array(name='screen'):
    screen_img = ImageGrab.grab()
    if name != 'screen':
        screen_img.save(f'{cwd}\\screen\\{name}.jpg')
    # 将截图从PIL图像转换为N-dimensional array多维数组，然后将颜色空间从RGB转换为BGR（OpenCV默认使用BGR）
    screen_nd_array = cv2.cvtColor(numpy.array(screen_img), cv2.COLOR_RGB2BGR)
    return screen_nd_array


def mark(background, p1, p2):
    cv2.rectangle(background, p1, p2, (0, 0, 255), 3)


# 随机位置偏移，默认左右5个像素
def get_position_with_offset(position, range=5):
    x, y = position
    x += random.randint(-range, range)
    y += random.randint(-range, range)
    return (x, y)


def player_click_without_delay(position):
    # 电脑原本鼠标位置
    originPosition = pyautogui.position()
    x, y = get_position_with_offset(position)
    duration = random.uniform(0.01, 0.02)
    pyautogui.moveTo(x, y, duration=duration)
    pyautogui.click()
    pyautogui.moveTo(*originPosition, duration=duration)


class Player(object):
    def __init__(self, accuracy=0.8):
        super(Player, self).__init__()
        self.accuracy = accuracy
        self.wait_second = 3
        self.img_dictionary = load_img_dictionary()
        self.screen_nd_array = get_screen_nd_array()

    # 在background大图片上定位target_name对应的小图片位置
    # debug开启则会以图片形式显示查找结果
    def locate(self, background, img_name, debug=0):
        position_2d_array = []
        target, c_name = self.img_dictionary[img_name]
        h, w, _ = target.shape
        result = cv2.matchTemplate(background, target, cv2.TM_CCOEFF_NORMED)
        location = numpy.where(result >= self.accuracy)
        distance = lambda a, b: ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5  # 计算两点距离
        for y, x in zip(*location):
            center = x + int(w / 2), y + int(h / 2)
            if position_2d_array and distance(position_2d_array[-1], center) < 20:  # 忽略邻近重复的点
                continue
            else:
                position_2d_array.append(center)
                p2 = x + w, y + h
                mark(background, (x, y), p2)

        if debug:  # 在图上显示寻找的结果，调试时开启
            cv2.imshow(f'result for {img_name}:', background)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        res = len(position_2d_array)
        msg = f'查找结果：{c_name} 匹配到 {res} 个位置，识别精确度：{self.accuracy}'
        print(msg)
        if position_2d_array:
            position_2d = position_2d_array[0]
            return position_2d
        return None

    def match(self, exist_img_name):
        screen_nd_array = get_screen_nd_array()
        position_2d = self.locate(screen_nd_array, exist_img_name)
        if position_2d is not None:
            return position_2d
        else:
            return None

    def player_click(self, position):
        # 电脑原本鼠标位置
        originPosition = pyautogui.position()
        x, y = get_position_with_offset(position)
        duration = random.uniform(0.01, 0.02)
        pyautogui.moveTo(x, y, duration=duration)
        pyautogui.click()
        pyautogui.moveTo(*originPosition, duration=duration)
        time.sleep(self.wait_second)

    def match_and_click_with_delay(self, img_name, wait_second):
        matched_position_2d = self.match(img_name)
        if matched_position_2d is not None:
            player_click_without_delay(matched_position_2d)
            time.sleep(wait_second)

    def match_and_click_primary(self, img_name_list):
        for img_name in img_name_list:
            matched_position_2d = self.match(img_name)
            if matched_position_2d is not None:
                self.player_click(matched_position_2d)
                break

    def match_and_click_by_order(self, img_name_list):
        for img_name in img_name_list:
            matched_position_2d = self.match(img_name)
            if matched_position_2d is not None:
                self.player_click(matched_position_2d)

    def match_with_shift(self, img_name_with_shift):
        screen_nd_array = get_screen_nd_array()
        img_name, direction, distance = img_name_with_shift
        position_2d = self.locate(screen_nd_array, img_name)
        if position_2d is not None:
            position_2d_with_shift = (
                position_2d[0] + distance * math.cos(math.radians(direction)),
                position_2d[1] + distance * math.sin(math.radians(direction))
            )
            return position_2d_with_shift

    def match_and_click_by_order_with_shift(self, img_name_list_with_shift):
        for img_name_with_shift in img_name_list_with_shift:
            matched_position_2d_with_shift = self.match_with_shift(img_name_with_shift)
            if matched_position_2d_with_shift is not None:
                self.player_click(matched_position_2d_with_shift)

    def match_with_shift_twice(self, img_name_with_shift_twice):
        screen_nd_array = get_screen_nd_array()
        img_name, direction_1, distance_1, direction_2, distance_2,  = img_name_with_shift_twice
        position_2d = self.locate(screen_nd_array, img_name)
        if position_2d is not None:
            position_2d_with_shift = (
                position_2d[0] + distance_1 * math.cos(math.radians(direction_1)),
                position_2d[1] + distance_1 * math.sin(math.radians(direction_1))
            )
            position_2d_with_shift_twice = (
                position_2d_with_shift[0] + distance_2 * math.cos(math.radians(direction_2)),
                position_2d_with_shift[1] + distance_2 * math.sin(math.radians(direction_2))
            )
            return position_2d_with_shift_twice

    def match_and_click_by_order_with_shift_twice(self, img_name_list_with_shift_twice):
        for img_name_with_shift_twice in img_name_list_with_shift_twice:
            matched_position_2d_with_shift_twice = self.match_with_shift_twice(img_name_with_shift_twice)
            if matched_position_2d_with_shift_twice is not None:
                self.player_click(matched_position_2d_with_shift_twice)