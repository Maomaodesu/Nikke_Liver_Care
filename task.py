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
        ('free_shop_normal', 90, 150),
        ('free_shop_normal_0_diamond_purchase', 0, 0),
        ('REWARD', 0, 0),
        # 刷新普通商店领取每日免费物品 第二次进入商店会浪费钻石
        # ('free_shop_normal', 90, 50),
        # ('free_shop_normal_refresh_confirm', 0, 0),
        # ('free_shop_normal', 90, 150),
        # ('free_shop_normal_0_diamond_purchase', 0, 0),
        # ('REWARD', 0, 0),
    ])
    # 竞技场商店购买每日物品
    player.match_and_click_by_order_with_shift([
        ('arena_shop_unselected', 0, 0),
        ('arena_shop_selected', 0, 110)
    ])
    player.match_and_click_with_delay('arena_shop_purchase', 0.1)
    if player.match('free_shop_insufficient_funds') is not None:
        player.match_and_click_by_order_with_shift([
            ('arena_shop_purchase_cancel', 0, 0),
            ('RETURN', 0, 0)
        ])
    else:
        player.match_and_click_by_order_with_shift([
            ('REWARD', 0, 0)
        ])
    player.match_and_click_by_order_with_shift([
        ('arena_shop_unselected', 0, 0),
        ('arena_shop_selected', 0, 220)
    ])
    player.match_and_click_with_delay('arena_shop_purchase', 0.1)
    if player.match('free_shop_insufficient_funds') is not None:
        player.match_and_click_by_order_with_shift([
            ('arena_shop_purchase_cancel', 0, 0),
            ('RETURN', 0, 0)
        ])
    else:
        player.match_and_click_by_order_with_shift([
            ('REWARD', 0, 0)
        ])
    player.match_and_click_by_order_with_shift([
        ('arena_shop_unselected', 0, 0),
        ('arena_shop_selected', 0, 330)
    ])
    player.match_and_click_with_delay('arena_shop_purchase', 0.1)
    if player.match('free_shop_insufficient_funds') is not None:
        player.match_and_click_by_order_with_shift([
            ('arena_shop_purchase_cancel', 0, 0),
            ('RETURN', 0, 0)
        ])
    else:
        player.match_and_click_by_order_with_shift([
            ('REWARD', 0, 0)
        ])
    player.match_and_click_by_order_with_shift([
        ('arena_shop_unselected', 0, 0),
        ('arena_shop_selected', 0, 440)
    ])
    player.match_and_click_with_delay('arena_shop_purchase', 0.1)
    if player.match('free_shop_insufficient_funds') is not None:
        player.match_and_click_by_order_with_shift([
            ('arena_shop_purchase_cancel', 0, 0),
            ('RETURN', 0, 0)
        ])
    else:
        player.match_and_click_by_order_with_shift([
            ('REWARD', 0, 0),
            ('RETURN', 0, 0)
        ])



# 付费商店
def paid_shop():
    daily = False
    weekly = False
    monthly = False
    player.match_and_click_with_delay('paid_shop_1', 2)
    player.match_and_click_with_delay('paid_shop_2', 2)
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
            'paid_shop_info_close'])
        player.match_and_click_by_order_with_shift([
            # 日周月免费钻石
            ('paid_shop_gift', 0, 0),
            # 每日
            ('paid_shop_beginner_special_support_selected', 0, 120), ('paid_shop_free_diamond', 0, 0), ('REWARD', 0, 0),
            # 每周
            ('paid_shop_beginner_special_support_unselected', 0, 240), ('paid_shop_free_diamond', 0, 0),
            ('REWARD', 0, 0),
            # 每月 容易识别错识别成每日
            ('paid_shop_beginner_special_support_unselected', 0, 360), ('paid_shop_free_diamond', 0, 0),
            ('REWARD', 0, 0)
        ])
    player.match_and_click_with_delay('RETURN', 1)


# 模拟室
def simulation_room():
    player.match_and_click_by_order(
        ['ark', 'simulation_room', 'simulation_start_1', 'simulation_difficulty_5', 'simulation_zone_c'])
    if player.match('simulation_finished') is not None:
        player.match_and_click_with_delay('simulation_close', 3)
        player.match_and_click_with_delay('HOME', 3)
        return
    else:
        player.match_and_click_by_order(['simulation_start_2'])
    while True:
        player.match_and_click_by_order([
            # 进入模拟关卡
            'simulation_battle_normal', 'simulation_battle_hard', 'simulation_boss_battle',
            # 战斗开始 - 结束
            'simulation_quick_battle','simulation_battle_begin', 'simulation_battle_end'
        ])
        player.match_and_click_by_order([
            # 选择增益效果 EPIC
            'simulation_buff_EPIC', 'simulation_buff_confirm',
            # 选择增益效果 SSR
            'simulation_buff_SSR', 'simulation_buff_confirm',
            # 选择增益效果 SR
            'simulation_buff_SR', 'simulation_buff_confirm',
            # 选择增益效果 R
            'simulation_buff_R', 'simulation_buff_confirm'
        ])
        # 增益效果交换
        simulation_buff_owned = player.match('simulation_buff_owned')
        if simulation_buff_owned is not None:
            player.match_and_click_by_order_with_shift([
                ('simulation_buff_owned', 90, 80),
                ('simulation_buff_exchange_confirm', 0, 0)
            ])
        # 选择治疗和属性提升
        player.match_and_click_by_order([
            'simulation_treatment_room', 'simulation_treatment_cure',
            'simulation_treatment_confirm_1',
            'simulation_treatment_confirm_2'
        ])
        # 检查通关结束模拟
        if player.match('simulation_end') is not None:
            player.match_and_click_by_order([
                'simulation_end',
                'simulation_end_confirm'
            ])
            # 选择通关增益效果
            player.match_and_click_primary([
                'simulation_buff_EPIC', 'simulation_buff_SSR', 'simulation_buff_SR', 'simulation_buff_R'
            ])
            player.match_and_click_by_order_with_shift([
                ('simulation_end_buff_confirm', 0, 0),
                ('simulation_buff_owned', 90, 80),
                ('simulation_buff_exchange_confirm', 0, 0)
            ])
            time.sleep(5)
            break
    # 返回主页
    player.match_and_click_by_order(['HOME'])


# 咨询
def consult():
    # 对第一个nikke进行咨询
    player.match_and_click_by_order(['lobby', 'nikke', 'nikke_consult'])
    player.match_and_click_by_order_with_shift([('nikke_consult_all', 90, 120)])
    while True:
        # 循环结束条件 指挥官体力用尽 —— 快速咨询
        if player.match('nikke_consult_quick'):
            # 进行快速咨询
            player.match_and_click_with_delay('nikke_consult_quick', 0.1)
            # 检测指挥官体力用尽,结束咨询
            if player.match('nikke_consult_commander_end') is not None:
                break
            # 检测妮姬体力用尽,翻页并跳过本轮循环
            if player.match('nikke_consult_nikke_end') is not None:
                player.match_and_click_by_order(['nikke_consult_next'])
                continue
            # 否则进入快速咨询
            else:
                time.sleep(2.5)
                player.match_and_click_by_order(['CONFIRM', 'nikke_consult_next_step'])

        # 循环结束条件 指挥官体力用尽 ——普通咨询
        else:
            # 进行普通咨询
            player.match_and_click_with_delay('nikke_consult_normal', 0.1)
            # 检测指挥官体力用尽,结束咨询
            if player.match('nikke_consult_commander_end') is not None:
                break
            # 检测妮姬体力用尽,翻页并跳过本轮循环
            if player.match('nikke_consult_nikke_end') is not None:
                player.match_and_click_by_order(['nikke_consult_next'])
                continue
            # 否则进入普通咨询
            else:
                # 进入咨询动画
                while True:
                    # 进行普通咨询
                    player.match_and_click_with_delay('nikke_consult_normal', 0.1)
                    # 检测指挥官体力用尽,结束咨询动画
                    if player.match('nikke_consult_commander_end') is not None:
                        break
                    # 检测妮姬体力用尽,结束咨询动画
                    if player.match('nikke_consult_nikke_end') is not None:
                        break
                    player.match_and_click_by_order([
                        'CONFIRM', 'nikke_consult_normal_auto', 'nikke_consult_normal_option_1',
                        'nikke_consult_normal_skip', 'nikke_consult_next_step'
                    ])
                # 结束咨询动画并翻页
                player.match_and_click_by_order(['nikke_consult_next'])
    # 咨询结束，返回主页
    player.match_and_click_by_order(['HOME'])


# 新人竞技场
def arena():
    player.match_and_click_with_delay('ark', 4)
    player.match_and_click_with_delay('arena', 4)
    player.match_and_click_with_delay('arena_beginner', 4)
    while True:
        arena_beginner_logo = player.match('arena_beginner_logo')
        arena_beginner_battle_free = player.match('arena_beginner_battle_free')
        if arena_beginner_logo is not None:
            if arena_beginner_battle_free is None:
                player.match_and_click_by_order(['HOME'])
                break
        player.match_and_click_by_order_with_shift([
            ('arena_beginner_battle_free', 90, 220),
            ('arena_beginner_battle_enter', 0, 0),
            ('arena_next', 270, 200)
        ])


# 日常
def daily():
    # 防御前哨基地 一举歼灭 获取奖励
    defence_base()
    time.sleep(5)
    # 友情点
    friend_points()
    time.sleep(5)
    # 邮箱
    mail()
    time.sleep(5)
    # 新人竞技场
    arena()
    time.sleep(5)
    # 免费商店
    free_shop()
    time.sleep(5)
    # 付费商店
    paid_shop()
    time.sleep(5)
    # 咨询
    consult()
    time.sleep(5)
    # 模拟
    # simulation_room()


