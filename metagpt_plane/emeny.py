import pygame
from plane_sprites import GameSprite,bloodline
from bullet import Bullet
from constants import *
import random


class Boss(GameSprite):

    def __init__(self):
        loaded_image = pygame.image.load("./images/enemy3_n1.png")
        
        super().__init__(loaded_image , 0, 1)
        self.music_boom = pygame.mixer.Sound("./music/enemy3_down.wav")
        self.music_fly = pygame.mixer.Sound("./music/enemy3_flying.wav")
        self.music_fly.play(-1)
        self.rect.centerx = 240
        self.y = 200
        self.isboom = False
        self.number = 3
        self.index1 = 1  # 控制动画速度
        self.index2 = 0
        self.index3 = 0
        self.index4 = 0
        self.injury = 1
        self.bar = bloodline(color_purple, 0, 0, 480, 8, 200)
        self.bullets = pygame.sprite.Group()

    def fire(self):
            for j in range(2, 7):  # 每层5个
                bullet = Bullet(0, 1)
                bullet.injury = 1
                # 2. 设置精灵的位置
                bullet.rect.centerx = self.rect.centerx
                bullet.rect.y = self.rect.bottom
                if j == 2:
                    bullet.speedx = 0
                else:
                    bullet.speedx = (-1) ** j * ((j - 1) // 2) * 1

                self.bullets.add(bullet)

    def update(self):
        # 左右移
        global SCORE
        if self.index4 % 2 == 0:  # 降低帧速率,注意这两个指针不能一样
            # 内部为左右移动大概50像素
            if self.index3 % 50 == 0 and (self.index3 // 50) % 2 == 1:
                self.speedx = -self.speedx
            self.rect.x += self.speedx
            self.index3 += 1
        self.index4 += 1

        # 发电动画
        self.image = pygame.image.load("./images/enemy3_n" + str((self.index1 // 6) % 2 + 1) + ".png")
        self.index1 += 1

        # 爆炸动画
        if self.isboom:
            self.bar.length -= self.injury * self.bar.weight
            if self.bar.length <= 0:  # 此时满足爆炸的条件了
                self.music_fly.stop()
                if self.index2 == 0:
                    self.music_boom.play()
                if self.index2 < 29:  # 4*7+1
                    self.image = pygame.image.load("./images/enemy3_down" + str(self.index2 // 7) + ".png")
                    # 这个地方之所以要整除4是为了减慢爆炸的速度，如果按照update的频率60hz就太快了
                    self.index2 += 1
                else:
                    self.kill()
                    SCORE += self.bar.value
            else:
                self.isboom = False  # 否则还不能死


class Enemy(GameSprite):
    """敌机精灵"""

    def __init__(self, num=1):
        self.number = num
        # 1. 调用父类方法，创建敌机精灵，同时指定敌机图片
        loaded_image = pygame.image.load("./images/enemy" + str(num) + ".png")
        super().__init__(loaded_image)

        # music
        if num == 1:
            self.music_boom = pygame.mixer.Sound("./music/enemy1_down.wav")
        else:
            self.music_boom = pygame.mixer.Sound("./music/enemy2_down.wav")
        # 2. 指定敌机的初始随机速度 1 ~ 3
        self.speedy = random.randint(1, 3)

        # 3. 指定敌机的初始随机位置
        self.rect.bottom = 0
        max_x = SCREEN_RECT.width - self.rect.width
        self.rect.x = random.randint(0, max_x)

        # 4.爆炸效果
        self.isboom = False
        self.index = 0

        # 5.血条
        if self.number == 1:
            self.bar = bloodline(color_blue, self.rect.x, self.rect.y, self.rect.width, 2, 3)
        else:
            self.bar = bloodline(color_blue, self.rect.x, self.rect.y, self.rect.width, 3, 5)

        # 6,子弹
        self.bullets = pygame.sprite.Group()

    def fire(self):
        for i in range(0, 2):
            # 1. 创建子弹精灵
            bullet = Bullet(0, random.randint(self.speedy + 1, self.speedy + 3))
            # 2. 设置精灵的位置
            bullet.rect.bottom = self.rect.bottom + i * 20
            bullet.rect.centerx = self.rect.centerx

            # 3. 将精灵添加到精灵组
            self.bullets.add(bullet)

    def update(self):
        global SCORE
        # 1. 调用父类方法，保持垂直方向的飞行
        super().update()

        # 2. 判断是否飞出屏幕，如果是，需要从精灵组删除敌机
        if self.rect.y > SCREEN_RECT.height:
            # print("飞出屏幕，需要从精灵组删除...")
            # kill方法可以将精灵从所有精灵组中移出，精灵就会被自动销毁
            self.kill()
            self.bar.length = 0

        if self.isboom:
            self.bar.length -= self.bar.weight * self.injury
            if self.bar.length <= 0:
                if self.index == 0:  # 保证只响一次
                    self.music_boom.play()
                if self.index < 17:  # 4*4+1
                    self.image = pygame.image.load(
                        "./images/enemy" + str(self.number) + "_down" + str(self.index // 4) + ".png")
                    # 这个地方之所以要整除4是为了减慢爆炸的速度，如果按照update的频率60hz就太快了
                    self.index += 1
                else:
                    self.kill()
                    SCORE += self.bar.value


            else:
                self.isboom = False

