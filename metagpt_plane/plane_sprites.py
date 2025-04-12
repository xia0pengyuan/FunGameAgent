import random
import pygame
from constants import *

class GameScore(object):
    def __init__(self):
        self.score = 0

    def getvalue(self):
        return self.score

    def increase(self, amount):
        self.score += amount

    def decrease(self, amount):
        self.score -= amount

class GameSprite(pygame.sprite.Sprite):
    """飞机大战游戏精灵"""

    def __init__(self, image, speedy=1, speedx=0):
        # 调用父类的初始化方法
        super().__init__()

        # 定义对象的属性
        self.image = image
        self.rect = self.image.get_rect()
        self.speedy = speedy
        self.speedx = speedx
        self.injury = 1
        self.index = 0  # 记帧数变量
        self.bar = bloodline(color_blue, self.rect.x, self.rect.y - 10, self.rect.width)

    def update(self):
        # 在屏幕的垂直方向上移动
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        self.bar.x = self.rect.x
        self.bar.y = self.rect.y - 10


class Background(GameSprite):
    """游戏背景精灵"""

    def __init__(self, is_alt=False):

        # 1. 调用父类方法实现精灵的创建(image/rect/speed)
        image = pygame.image.load("./images/background.png")
        
        super().__init__(image)

        # 2. 判断是否是交替图像，如果是，需要设置初始位置
        if is_alt:
            self.rect.y = -self.rect.height

    def update(self):

        # 1. 调用父类的方法实现
        super().update()

        # 2. 判断是否移出屏幕，如果移出屏幕，将图像设置到屏幕的上方
        if self.rect.y >= SCREEN_RECT.height:
            self.rect.y = -self.rect.height

class bloodline(object):
    def __init__(self, color, x, y, length, width=2, value=2):
        self.color = color
        self.x = x
        self.y = y
        self.length = length
        self.width = width  # 线宽
        self.value = value * 1.0  # 血量用浮点数
        self.weight = length / value  # 每一滴血表示的距离
        self.color_init = color

    def update(self, canvas):
        if self.length <= self.value * self.weight / 2:
            self.color = color_red
        else:
            self.color = self.color_init
        self.bar_rect = pygame.draw.line(canvas, self.color, (self.x, self.y), (self.x + self.length, self.y),
                                         self.width)
        
class CanvasOver():
    def __init__(self, screen, score, total_time=30):
        self.img_again = pygame.image.load("./images/again.png")
        self.img_over = pygame.image.load("./images/gameover.png")
        self.rect_again = self.img_again.get_rect()
        self.rect_over = self.img_over.get_rect()
        self.rect_again.centerx = self.rect_over.centerx = SCREEN_RECT.centerx
        self.rect_again.bottom = SCREEN_RECT.centery
        self.rect_over.y = self.rect_again.bottom + 20
        self.screen = screen
        self.score = score


    def event_handler(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if self.rect_again.left < pos[0] < self.rect_again.right and \
                    self.rect_again.top < pos[1] < self.rect_again.bottom:
                return 1
            elif self.rect_over.left < pos[0] < self.rect_over.right and \
                    self.rect_over.top < pos[1] < self.rect_over.bottom:
                return 0

    def update(self):
        self.screen.blit(self.img_again, self.rect_again)
        self.screen.blit(self.img_over, self.rect_over)
        score_font = pygame.font.Font("./STCAIYUN.ttf", 50)
        image = score_font.render("SCORE:" + str(int(self.score.getvalue())), True, color_gray)
        rect = image.get_rect()
        rect.centerx, rect.bottom = SCREEN_RECT.centerx, self.rect_again.top - 20
        self.screen.blit(image, rect)
        
