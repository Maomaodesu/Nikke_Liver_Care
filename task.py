import time
import pyautogui
import keyboard as keyboard

from player import Player
my_player = Player(accuracy=0.8)

######################################################### 修改player属性 ################################################
def change_accuracy(new_accuracy):
    my_player.change_accuracy(new_accuracy)
def change_interval(new_interval):
    my_player.change_interval(new_interval)
def change_click(click_pattern):
    my_player.change_click(click_pattern)

######################################################## 点击功能实现 ####################################################
# 收取每日资源
def gain_rewards(arena_shop_task):
    while True:
        # 收获珠宝
        if my_player.exist(['shop']):
            my_player.find_touch_skewing(['shop'], 90, 104)
            # my_player.find_touch(['destroy'])
        #
        #     if my_player.exist(['start_destroy']):
        #         my_player.find_touch(['start_destroy', 'REWARD'])
        #
        #     my_player.find_touch(['cancel', 'gain_reward', 'REWARD_2', 'REWARD', 'lobby'])
        # # 友情点
        # if my_player.exist(['friend']):
        #     my_player.find_touch(['friend', 'give', 'confirm', 'close'])
        # # 邮箱
        # if my_player.exist(['mail']):
        #     my_player.find_touch(['mail'])
        #     time.sleep(my_player.interval)
        #     my_player.find_touch(['gain_mail'])
        #     time.sleep(my_player.interval)
        #     my_player.find_touch(['REWARD', 'close_3'])
        # # 商店每日免费物品
        # if my_player.exist(['shop']):
        #     my_player.find_touch(['shop', '0'])
        #     my_player.find_touch(['buy', 'REWARD'])
        #     if arena_shop_task:
        #         my_player.find_touch(['arena_shop'])
        #         my_player.find_touch_skewing(['arena_shop_2'], 0, 110)
        #         my_player.find_touch(['buy', 'REWARD'])
        #         my_player.find_touch_skewing(['arena_shop_2'], 0, 220)
        #         my_player.find_touch(['buy', 'REWARD'])
        #         my_player.find_touch_skewing(['arena_shop_2'], 0, 330)
        #         my_player.find_touch(['buy', 'REWARD'])
        #         my_player.find_touch_skewing(['arena_shop_2'], 0, 440)
        #         my_player.find_touch(['buy', 'REWARD'])
        #     my_player.find_touch(['home', 'home'])
        #     time.sleep(my_player.interval)
        # # 付费商店每日,每周,每月钻石
        # if my_player.exist(['pay_shop']):
        #     my_player.find_touch(['pay_shop', 'gift'])
        #     time.sleep(my_player.interval)
        #
        #     if my_player.exist(['everymonth']):
        #         claim_free_diamond(my_player, ['everymonth'])
        #
        #     if my_player.exist(['everyweek']):
        #         claim_free_diamond(my_player, ['everyweek'])
        #
        #     claim_free_diamond(my_player, ['everyday'])
        #
        #     my_player.find_touch(['home'])
        # # 特殊竞技场收米
        # if my_player.exist(['ark']):
        #     my_player.find_touch(['ark', 'ark', 'arena', 'arena', 'special_arena', 'special_arena'])
        #     my_player.find_touch_skewing(['touch'], 90, 87)
        #     time.sleep(my_player.interval)
        #     my_player.find_touch(['gain_reward_2', 'REWARD', 'home'])
        #     time.sleep(my_player.interval)
        # # 任务委托收米
        # if my_player.exist(['base']):
        #     my_player.find_touch(['base'])
        #     time.sleep(my_player.interval * 2.5)
        #     my_player.find_touch(['board', 'gain_all', 'REWARD', 'dispatch_all', 'dispatch', 'home', 'home'])
        #     time.sleep(my_player.interval * 2.5)
        # # 日常任务
        # if my_player.exist(['mission']):
        #     my_player.find_touch_skewing(['mission'], 180, 155)
        #     my_player.find_touch(['gain_all_2', 'gain_all_2', 'REWARD', 'close_2'])
        #     if my_player.exist(['000']):
        #         break
        # # 露菲弹窗广告
        # if my_player.exist(['ad']):
        #     my_player.find_touch(['ad', 'confirm_2'])

def claim_free_diamond(player, location):
    player.find_touch(location)

    if player.exist(['free_diamond']):
        player.find_touch(['free_diamond', 'REWARD'])
