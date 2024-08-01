import time
import pyautogui
import keyboard as keyboard
from player import Player

player = Player()


######################################################### 修改player属性 ################################################
def change_accuracy(new_accuracy):
    player.change_accuracy(new_accuracy)


def change_interval(new_interval):
    player.change_interval(new_interval)


def change_click(click_pattern):
    player.change_click(click_pattern)


######################################################## 点击功能实现 ####################################################


# 防御前哨基地 一举歼灭 获取奖励
def defence_base():
    player.match_and_click_by_order_with_shift([
        ('free_shop', 90, 100),
        ('destroy', 0, 0),
        ('destroy_start', 0, 0),
        ('REWARD', 0, 0),
        ('destroy_cancel', 0, 0),
        ('gain_reward', 0, 0),
        ('REWARD', 0, 0),
        ('gain_reward_click', 0, 0)
    ])


# 友情点
def friend_points():
    player.match_and_click_by_order([
        'friend', 'friend_give',
        'friend_confirm',
        'friend_close'])


# 邮箱
def mail():
    player.match_and_click_by_order(['mail', 'mail_get_all', 'REWARD', 'mail_close'])


# 免费商店
def free_shop():
    player.match_and_click_by_order_with_shift([
        # 普通商店领取每日免费物品
        ('free_shop', 0, 0),
        ('free_shop_normal_0_diamond', 0, 0),
        ('free_shop_normal_0_diamond_purchase', 0, 0),
        ('REWARD', 0, 0),
        # 刷新普通商店领取每日免费物品 容易识别错导致浪费钻石
        # ('free_shop_normal_free_refresh', 180, 50),
        # ('free_shop_normal_refresh_confirm', 0, 0),
        # ('free_shop_normal_0_diamond', 0, 0),
        # ('free_shop_normal_0_diamond_purchase', 0, 0),
        # ('REWARD', 0, 0),
        # 竞技场商店购买每日物品
        ('arena_shop_unselected', 0, 0),
        ('arena_shop_selected', 0, 110),
        ('arena_shop_purchase', 0, 0),
        ('REWARD', 0, 0),
        ('arena_shop_selected', 0, 220),
        ('arena_shop_purchase', 0, 0),
        ('REWARD', 0, 0),
        ('arena_shop_selected', 0, 330),
        ('arena_shop_purchase', 0, 0),
        ('REWARD', 0, 0),
        ('arena_shop_selected', 0, 440),
        ('arena_shop_purchase', 0, 0),
        ('REWARD', 0, 0),
        ('RETURN', 0, 0)
    ])


# 付费商店
def paid_shop():
    daily = False
    weekly = False
    monthly = False
    player.match_and_click_with_delay('paid_shop', 2)
    while True:
        paid_shop_free_diamond_daily_sold_out = player.match('paid_shop_free_diamond_daily_sold_out')
        if paid_shop_free_diamond_daily_sold_out:
            daily = True
        paid_shop_free_diamond_weekly_sold_out = player.match('paid_shop_free_diamond_weekly_sold_out')
        if paid_shop_free_diamond_weekly_sold_out:
            weekly = True
        paid_shop_free_diamond_monthly_sold_out = player.match('paid_shop_free_diamond_monthly_sold_out')
        if paid_shop_free_diamond_monthly_sold_out:
            monthly = True
        if daily & weekly & monthly:
            break
        player.match_and_click_by_order([
            # 消费年龄限制
            'paid_shop_age_limit',
            'paid_shop_age_limit_confirm',
            # 评价通知
            'paid_shop_info_close',
            # 日周月免费钻石
            'paid_shop_gift',
            # 每日
            'paid_shop_gift_daily', 'paid_shop_free_diamond', 'REWARD',
            # 每周
            'paid_shop_gift_weekly', 'paid_shop_free_diamond', 'REWARD',
            # 每月 容易识别错识别成每日
            'paid_shop_gift_monthly', 'paid_shop_free_diamond', 'REWARD'
        ])
    player.match_and_click_with_delay('RETURN',1)


# 模拟室
def simulation_room():
    player.match_and_click_with_delay('ark', 2)
    player.match_and_click_with_delay('simulation_room', 1)
    player.match_and_click_by_order([
        'simulation_start_1', 'simulation_difficulty_5', 'simulation_zone_c', 'simulation_start_2'
    ])
    while True:
        player.match_and_click_by_order([
            # 进入模拟关卡
            'simulation_battle_normal', 'simulation_battle_hard', 'simulation_boss_battle',
            # 战斗开始 - 结束
            'simulation_battle_begin', 'simulation_battle_end',
            # 选择增益效果
            'simulation_buff_SSR', 'simulation_buff_SR', 'simulation_buff_R',
            'simulation_buff_confirm',
            # 选择治疗和属性提升
            'simulation_treatment_room', 'simulation_treatment_cure',
            'simulation_treatment_confirm_1',
            'simulation_treatment_confirm_2'
        ])

        # 检查通关结束模拟
        position_2d = player.match('simulation_end')
        if position_2d is not None:
            player.match_and_click_by_order([
                'simulation_end',
                'simulation_end_confirm',
                # 选择通关增益效果
                'simulation_buff_SSR', 'simulation_buff_SR', 'simulation_buff_R',
                'simulation_end_buff_confirm'
            ])
            break
    # 返回主页
    player.match_and_click_by_order(['RETURN', 'RETURN'])


# 咨询
def consult():
    player.match_and_click_by_order(['lobby', 'nikke', 'nikke_consult'])
    while True:
        if player.match('nikke_consult_end'):
            player.match_and_click_by_order(['home'])
            break
        else:
            # 两个 RETURN 处理卡住的情况
            player.match_and_click_by_order([
                # 快速咨询
                'nikke_consult_target',
                'nikke_consult_quick', 'CONFIRM', 'RETURN',
                # 普通咨询
                'nikke_consult_normal', 'CONFIRM', 'nikke_consult_normal_auto',
                'nikke_consult_normal_option_1', 'RETURN',
            ])
            # 能返回大厅的情况下返回大厅
            if player.match('lobby'):
                player.match_and_click_by_order(['lobby'])
                break


# 新人竞技场
def arena():
    player.match_and_click_by_order([
        'ark', 'arena', 'arena_beginner'
    ])
    while True:
        if player.match('arena_beginner_battle_end'):
            player.match_and_click_by_order(['RETURN'])
            break
        player.match_and_click_by_order_with_shift([
            ('arena_beginner_battle_1', 90, 180),
            ('arena_beginner_battle_2', 0, 0),
            ('arena_next', 270, 200)
        ])


# 日常
def daily():
    # 防御前哨基地 一举歼灭 获取奖励
    # defence_base()
    # time.sleep(3)
    # # 友情点
    # friend_points()
    # time.sleep(3)
    # # 邮箱
    # mail()
    # time.sleep(3)
    # # 免费商店
    # free_shop()
    # time.sleep(3)
    # # 付费商店
    # paid_shop()
    # time.sleep(3)
    # 咨询
    consult()
    time.sleep(3)
    # 新人竞技场
    arena()
    time.sleep(3)
    #模拟
    simulation_room()


def test():
    # player.match('arena_beginner_battle_end')
    # player.match('arena_beginner_battle_1')
    player.match('CONFIRM')
    player.match('free_shop_normal_refresh_confirm')
    player.match('friend_confirm')
    player.match('nikke_consult_normal_confirm')
    player.match('paid_shop_age_limit_confirm')
    player.match('simulation_end_buff_confirm')
    player.match('simulation_treatment_confirm_1')
    player.match('simulation_treatment_confirm_2')
