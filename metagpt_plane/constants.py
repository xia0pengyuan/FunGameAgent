import pygame

# 分数
SCORE = 0
# 屏幕大小的常量
SCREEN_RECT = pygame.Rect(0, 0, 480, 700)
# color
color_blue = (30, 144, 255)
color_green = (0, 255, 0)
color_red = (255, 0, 0)
color_purple = (148, 0, 211)
color_gray = (251, 255, 242)
# 刷新的帧率
FRAME_PER_SEC = 60  # 刷新率是60hz,即每秒update60次
# 创建敌机的定时器常量,自定义用户事件,其实就是int数,不同数表示不同事件
CREATE_ENEMY_EVENT = pygame.USEREVENT
# 英雄发射子弹事件
HERO_FIRE_EVENT = pygame.USEREVENT + 1
# buff1 出现的事件
BUFF1_SHOW_UP = pygame.USEREVENT + 2
# buff2
BUFF2_SHOW_UP = pygame.USEREVENT + 3
# 敌军发射子弹
ENEMY_FIRE_EVENT = pygame.USEREVENT + 4
# 发射炸弹
BOMB_THROW = pygame.USEREVENT + 5

OUTPUT_CONTROL_EVENT = pygame.USEREVENT + 6