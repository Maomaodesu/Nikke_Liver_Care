import os
import random
import time
import math
import cv2
import numpy
import pyautogui
from PIL import ImageGrab

cwd = __file__.replace('player.py', '')  # cwd: 获取当前脚本文件的目录。
wanted_path = f'{cwd}\\wanted'  # 目标图片目录


class Player(object):
    #初始化Player对象时，设置精确度、点击间隔、点击模式等参数，并根据是否启用ADB模式来加载设备信息或物理屏幕尺寸。
    # accuracy 匹配精准度 0~1 #adb_mode开启ADB模式  #adb_num连接第几台ADB设备
    def __init__(self, accuracy=0.8):
        # 在player的构造方法中调用父类Object的构造方法，以便具备Object类的功能
        super(Player, self).__init__()
        #精准度
        self.accuracy = accuracy
        #点击间隔
        self.interval = 2.5
        #点击次数
        self.click_pattern = 1
        # 读取目标图片目录中的所有图片，并存储在字典target_map中，键为文件名，值为图像内容和文件名的列表。
        self.load_target()
        # 使用pyautogui.size()方法获取当前电脑屏幕的宽度和高度，分别存储在变量w和h中。
        w, h = pyautogui.size()
        # 打印电脑屏幕的物理尺寸
        print(f'Physical size: {w}x{h}')

    # 读取要查找的目标图片，名称为文件名
    # 返回字典target_map = {name1:[cv2_image1, name1], name2:...}
    def load_target(self):
        target_map = {}
        path = wanted_path
        file_list = os.listdir(path)
        for file in file_list:
            name = file.split('.')[0]
            file_path = path + '/' + file
            content = [cv2.imread(file_path), name]
            target_map[name] = content
        print(target_map.keys())
        self.target_map = target_map
        return target_map


    # ADB命令模拟点击屏幕，参数pos为目标坐标(x, y), 自带随机偏移
    # 或pyautogui鼠标点击，带偏移与延迟
    def touch(self, position):
        x, y = self.random_offset(position)
        origin = pyautogui.position()
        dt = random.uniform(0.01, 0.02)
        pyautogui.moveTo(x, y, duration=dt)
        if self.click_pattern == 1:
            # 单击
            pyautogui.doubleClick()
        elif self.click_pattern == 2:
            # 双击
            pyautogui.click()
        else:
            # 按压释放
            pyautogui.mouseDown(button='left')
            time.sleep(0.4)
            pyautogui.mouseUp(button='left')
        time.sleep(0.13)
        pyautogui.moveTo(*origin, duration=dt)


    # 随机位置偏移，默认左右5个像素
    def random_offset(self, position, range=5):
        x, y = position
        x += random.randint(-range, range)
        y += random.randint(-range, range)
        return (x, y)


    # 裁剪Img以加速检测， area[h1,h2,w1,w2]为高宽范围百分比
    # 选中区域为高h1%到h2% 宽w1%到w2%，返回裁剪后图片与左上角位置
    def cut(self, img, area=[0, 50, 0, 50]):
        h1, h2, w1, w2 = [e / 100 for e in area]
        h, w, c = img.shape
        h1, h2 = int(h * h1), int(h * h2)
        w1, w2 = int(w * w1), int(w * w2)
        small = img[h1:h2, w1:w2, :]
        start = [w1, h1]
        return small, start

    # 判断name_list中哪些目标存在，但不点击，全部目标遍历，返回同长度真假列表
    # 输入[name1,name2...]返回[name1_result, name2_result...]
    def exist(self, name_list, area=None):
        background = self.screen_shot()
        if area:
            background, start = self.cut(background, area)
        re = []
        name_list = name_list if type(name_list) == list else [name_list, ]
        for name in name_list:
            loc_pos = self.locate(background, name)
            cur = len(loc_pos) > 0
            re.append(cur)
        re = re[0] if len(re) == 1 else re
        time.sleep(0.2)
        return re


    # 寻找name_list中的目标，并点击第一个找到的目标，然后中止
    # 注意有优先级顺序，找到了前面的就不会再找后面的
    # 只返回第一个找到并点击的name，都没找到返回false
    def find_touch_same_screen(self, name_list, area=None):
        background = self.screen_shot()
        if area:
            background, start = self.cut(background, area)
        re = False
        name_list = name_list if type(name_list) == list else [name_list, ]
        for name in name_list:
            loc_pos = self.locate(background, name)
            if len(loc_pos) > 0:
                if area:  # 从裁剪后的坐标还原回裁前的坐标
                    loc_pos[0][0] += start[0]
                    loc_pos[0][1] += start[1]
                self.touch(loc_pos[0])  # 同一目标多个结果时只点第一个
                re = name
                break
        return re

    # 依次寻找name_list中的目标，并点击
    def find_touch(self, name_list, area=None):
        re = False
        name_list = name_list if type(name_list) == list else [name_list, ]
        for name in name_list:
            background = self.screen_shot()
            if area:
                background, start = self.cut(background, area)
            loc_pos = self.locate(background, name)
            if len(loc_pos) > 0:
                if area:  # 从裁剪后的坐标还原回裁前的坐标
                    loc_pos[0][0] += start[0]
                    loc_pos[0][1] += start[1]
                self.touch(loc_pos[0])  # 同一目标多个结果时只点第一个
                re = name
            time.sleep(self.interval)
        return re

    # 寻找目标，点击偏移指定方向距离的目标
    def find_touch_skewing(self, name_list, direction, distance):
        re = False
        name_list = name_list if type(name_list) == list else [name_list, ]
        for name in name_list:
            background = self.screen_shot()
            loc_pos = self.locate(background, name)
            if len(loc_pos) > 0:
                t = loc_pos[0]
                new_t = (t[0] + distance * math.cos(math.radians(direction)),
                         t[1] + distance * math.sin(math.radians(direction)))
                loc_pos[0] = new_t
                self.touch(loc_pos[0])  # 同一目标多个结果时只点第一个
                re = name
            time.sleep(self.interval)
        return re

        # 核心功能， 在background大图片上定位target_name对应的小图片位置
        # debug开启则会以图片形式显示查找结果

    def locate(self, background, target_name, debug=0):
        loc_pos = []
        target, c_name = self.target_map[target_name]
        h, w, _ = target.shape
        result = cv2.matchTemplate(background, target, cv2.TM_CCOEFF_NORMED)
        location = numpy.where(result >= self.accuracy)
        dis = lambda a, b: ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5  # 计算两点距离
        for y, x in zip(*location):
            center = x + int(w / 2), y + int(h / 2)
            if loc_pos and dis(loc_pos[-1], center) < 20:  # 忽略邻近重复的点
                continue
            else:
                loc_pos.append(center)
                p2 = x + w, y + h
                self.mark(background, (x, y), p2)

        if debug:  # 在图上显示寻找的结果，调试时开启
            cv2.imshow(f'result for {target_name}:', background)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        res = len(loc_pos)
        msg = f'查找结果：{c_name} 匹配到 {res} 个位置，识别精确度：{self.accuracy}'
        print(msg)
        return loc_pos

    # 在图上标记位置p1左上，p2右下
    def mark(self, background, p1, p2):
        cv2.rectangle(background, p1, p2, (0, 0, 255), 3)


    # 截屏并发送到目录./screen, 默认返回cv2读取后的图片，存储在player对象的screen属性下
    # 根据是否启用ADB模式来决定使用ADB命令截屏还是直接使用PIL截屏，并将截图保存到指定目录。
    def screen_shot(self, name='screen'):
        # 使用PIL库的ImageGrab.grab()方法截取当前屏幕并将其存储在screen变量中。
        screen = ImageGrab.grab()
        # 如果截图的名称不是默认的'screen'，则保存截图到硬盘。
        # 非默认情况才保存硬盘 否则直接读取内存文件，name没被更改过一般直接跳出if
        if name != 'screen':
            screen.save(f'{cwd}\\screen\\{name}.jpg')
        # 将截图从PIL图像转换为NumPy数组，然后将颜色空间从RGB转换为BGR（OpenCV默认使用BGR）
        screen = cv2.cvtColor(numpy.array(screen), cv2.COLOR_RGB2BGR)
        print('截图已完成 ', time.ctime())
        self.screen = screen
        return self.screen

    @staticmethod
    def continuous_click():
        pyautogui.mouseDown()
        time.sleep(0.23)
        pyautogui.mouseUp()
        time.sleep(0.021)

    # 修改精确度
    def change_accuracy(self, new_accuracy):
        self.accuracy = new_accuracy

    # 修改时间间隔
    def change_interval(self, new_interval):
        self.interval = new_interval

    # 修改点击模式
    def change_click(self, click_pattern):
        self.click_pattern = click_pattern