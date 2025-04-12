
import pygame
from plane_sprites import GameSprite, bloodline        
from Plane_Game.bullet4 import Bullet
from constants import *

class Hero(GameSprite):
    """英雄精灵"""

    def __init__(self):
        # 1. 调用父类方法，设置image&speed
        loaded_image = pygame.image.load("./images/me1.png")
        
        super().__init__(loaded_image)
        self.music_down = pygame.mixer.Sound("./music/me_down.wav")
        self.music_upgrade = pygame.mixer.Sound("./music/upgrade.wav")
        self.music_degrade = pygame.mixer.Sound("./music/supply.wav")
        
        self.number = 0
        # 2. 设置英雄的初始位置
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.bottom = SCREEN_RECT.bottom - 120

        # 3. 创建子弹的精灵组
        self.bullets = pygame.sprite.Group()
        # 4.爆炸
        self.isboom = False
        self.index1 = 1  # 控制动画速度
        self.index2 = 0
        # 5.buff1加成
        self.buff1_num = 0
        # 6,英雄血条
        self.bar = bloodline(color_green, 0, 700, 480, 8, 10)
        # 7，炸弹数目
        self.bomb = 0

    def update(self):

        # 英雄在水平方向移动和血条不同步,特殊
        self.rect.y += self.speedy
        self.rect.x += self.speedx

        # 控制英雄不能离开屏幕
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.right > SCREEN_RECT.right:
            self.rect.right = SCREEN_RECT.right
        elif self.rect.y < 0:
            self.rect.y = 0
        elif self.rect.bottom > SCREEN_RECT.bottom:
            self.rect.bottom = SCREEN_RECT.bottom

        # 英雄喷气动画

        self.image = pygame.image.load("./images/me" + str((self.index1 // 6) % 2 + 1) + ".png")
        self.index1 += 1

        # 英雄爆炸动画
        if self.isboom:
            self.bar.length -= self.injury * self.bar.weight
            if self.bar.length <= 0:  # 此时满足爆炸的条件了
                if self.index2 == 0:
                    self.music_down.play()
                if self.index2 < 17:  # 4*4+1
                    self.image = pygame.image.load("./images/me_destroy_" + str(self.index2 // 4) + ".png")
                    # 这个地方之所以要整除4是为了减慢爆炸的速度，如果按照update的频率60hz就太快了
                    self.index2 += 1
                else:
                    self.kill()
            else:
                self.isboom = False  # 否则还不能死

    # 发射子弹
    def fire(self, enemy_group):
        bullet_obj = Bullet(1,-2,0, enemy_group)  
        bullet_obj.player_fire(self)


class Heromate(Hero):
    def __init__(self, num):
        super().__init__()
        self.image = pygame.image.load("./images/life.png")
        self.number = num

    def update(self):

        if self.rect.right > SCREEN_RECT.right:
            self.rect.right = SCREEN_RECT.right
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.y < 0:
            self.rect.y = 0
        elif self.rect.bottom > SCREEN_RECT.bottom:
            self.rect.bottom = SCREEN_RECT.bottom

    def fire(self):
        for i in range(0, 1, 2):
            # 1. 创建子弹精灵
            bullet = Bullet()
            # 2. 设置精灵的位置
            bullet.rect.bottom = self.rect.y - i * 20
            bullet.rect.centerx = self.rect.centerx
            # 3. 将精灵添加到精灵组
            self.bullets.add(bullet)


