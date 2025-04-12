
import pygame


'''地板'''
class Ground(pygame.sprite.Sprite):
    def __init__(self, image, position, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        # 导入图片
        self.image_0 = image
        self.rect_0 = self.image_0.get_rect()
        self.rect_0.left, self.rect_0.bottom = position
        self.image_1 = image
        #self.image_1 = pygame.transform.scale(image1,(46, 40))
        self.rect_1 = self.image_1.get_rect()
        self.rect_1.left, self.rect_1.bottom = self.rect_0.right, self.rect_0.bottom
        # 定义一些必要的参数
        self.speed = -10
    '''更新地板'''
    def update(self):
        self.rect_0.left += self.speed
        self.rect_1.left += self.speed
        if self.rect_0.right < 0:
            self.rect_0.left = self.rect_1.right
        if self.rect_1.right < 0:
            self.rect_1.left = self.rect_0.right
    '''将地板画到屏幕'''
    def draw(self, screen):
        screen.blit(self.image_0, self.rect_0)
        screen.blit(self.image_1, self.rect_1)


'''云'''
class Cloud(pygame.sprite.Sprite):
    def __init__(self, image, position, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        # 导入图片
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = position
        # 定义一些必要的参数
        self.speed = -1
    '''将云画到屏幕上'''
    def draw(self, screen):
        screen.blit(self.image, self.rect)
    '''更新云'''
    def update(self):
        self.rect = self.rect.move([self.speed, 0])
        if self.rect.right < 0:
            self.kill()

class SUB(pygame.sprite.Sprite):
    def __init__(self, image,image1, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        # 导入图片
        self.image = pygame.transform.scale(image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = 75,175
        
        self.image1 = pygame.transform.scale(image1, (75, 75))
        self.rect1 = self.image1.get_rect()
        self.rect1.left, self.rect1.top = 175,175
        # 定义一些必要的参数
        #self.speed = -1
    '''将云画到屏幕上'''
    def draw(self, screen,weapon_class):
        screen.blit(self.image, self.rect)
        screen.blit(self.image1, self.rect1)
        
        if weapon_class[0] == 1:
            pygame.draw.polygon(screen, (255,0,0), [(100, 230), (75, 260), (125, 260)])
        if weapon_class[1] == 1:
            pygame.draw.polygon(screen, (0,255,0), [(200, 230), (175, 260), (225, 260)])
    '''更新云'''
    def update(self):
        return












'''记分板'''
class Scoreboard(pygame.sprite.Sprite):
    def __init__(self, image, position, size=(11, 13), is_highest=False, bg_color=None, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        # 导入图片
        self.images = []
        for i in range(12):
            self.images.append(pygame.transform.scale(image.subsurface((i*20, 0), (20, 24)), size))
        if is_highest:
            self.image = pygame.Surface((size[0]*8, size[1]))
        else:
            self.image = pygame.Surface((size[0]*5, size[1]))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = position
        # 一些必要的变量
        self.is_highest = is_highest
        self.bg_color = bg_color
        self.score = '00000'
    '''设置得分'''
    def set(self, score):
        self.score = str(score).zfill(5)
    '''画到屏幕上'''
    def draw(self, screen):
        self.image.fill(self.bg_color)
        for idx, digital in enumerate(list(self.score)):
            digital_image = self.images[int(digital)]
            if self.is_highest:
                self.image.blit(digital_image, ((idx+3)*digital_image.get_rect().width, 0))
            else:
                self.image.blit(digital_image, (idx*digital_image.get_rect().width, 0))
        if self.is_highest:
            self.image.blit(self.images[-2], (0, 0))
            self.image.blit(self.images[-1], (digital_image.get_rect().width, 0))
        screen.blit(self.image, self.rect)

""" class Scoreboard(pygame.sprite.Sprite):
    def __init__(self, image, position, size=(11, 13), is_highest=False, bg_color=None, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        # 导入图片
        self.images = []
        for i in range(12):
            self.images.append(pygame.transform.scale(image.subsurface((i*20, 0), (20, 24)), size))
        # 根据是否为最高得分的标志设置Surface的大小
        if is_highest:
            self.image = pygame.Surface((size[0]*14, size[1]))  # 调整宽度以容纳两个分数
        else:
            self.image = pygame.Surface((size[0]*10, size[1]))  # 调整宽度以容纳两个分数
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = position
        # 一些必要的变量
        self.is_highest = is_highest
        self.bg_color = bg_color
        self.score1 = '00000'
        self.score2 = '00000'

    '''设置得分'''
    def set(self, score1, score2):
        self.score1 = str(score1).zfill(5)
        self.score2 = str(score2).zfill(5)

    '''画到屏幕上'''
    def draw(self, screen):
        self.image.fill(self.bg_color)
        # 绘制第一个分数
        for idx, digital in enumerate(list(self.score1)):
            digital_image = self.images[int(digital)]
            self.image.blit(digital_image, (idx*digital_image.get_rect().width, 0))
        # 绘制第二个分数
        for idx, digital in enumerate(list(self.score2)):
            digital_image = self.images[int(digital)]
            self.image.blit(digital_image, ((idx+6)*digital_image.get_rect().width, 0))
        # 如果是最高分情况，还需要在左侧显示一些额外的图标
        if self.is_highest:
            self.image.blit(self.images[-2], (0, 0))
            self.image.blit(self.images[-1], (digital_image.get_rect().width, 0))
        screen.blit(self.image, self.rect) """
