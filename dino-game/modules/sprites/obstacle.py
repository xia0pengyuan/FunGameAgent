
import random
import pygame


'''仙人掌'''
class Cactus(pygame.sprite.Sprite):
    def __init__(self, images, position=(600, 147), sizes=[(55, 70), (30, 50)], **kwargs):
        pygame.sprite.Sprite.__init__(self)
        # 导入图片
        self.images = []
        image = images[0]
        for i in range(3):
            self.images.append(pygame.transform.scale(image.subsurface((i*101, 0), (101, 101)), sizes[0]))

        self.image = random.choice(self.images)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.bottom = position
        self.mask = pygame.mask.from_surface(self.image)
        # 定义一些必要的变量
        self.speed = -10
    '''画到屏幕上'''
    def draw(self, screen):
        screen.blit(self.image, self.rect)
    '''更新'''
    def update(self):
        self.rect = self.rect.move([self.speed, 0])
        if self.rect.right < 0:
            self.kill()
    def remove(self):
        self.kill()

'''飞龙'''
class Ptera(pygame.sprite.Sprite):
    def __init__(self, image, position, size=(46, 40), **kwargs):
        pygame.sprite.Sprite.__init__(self)
        # 导入图片
        self.images = []
        for i in range(2):
            self.images.append(pygame.transform.scale(image.subsurface((i*92, 0), (92, 81)), size))
        self.image_idx = 0
        self.image = self.images[self.image_idx]
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.centery = position
        self.mask = pygame.mask.from_surface(self.image)
        # 定义一些必要的变量
        self.speed = -10
        self.refresh_rate = 10
        self.refresh_counter = 0
    '''画到屏幕上'''
    def draw(self, screen):
        screen.blit(self.image, self.rect)
    '''更新'''
    def update(self):
        if self.refresh_counter % self.refresh_rate == 0:
            self.refresh_counter = 0
            self.image_idx = (self.image_idx + 1) % len(self.images)
            self.loadImage()
        self.rect = self.rect.move([self.speed, 0])
        if self.rect.right < 0:
            self.kill()
        self.refresh_counter += 1
    '''载入当前状态的图片'''
    def loadImage(self):
        self.image = self.images[self.image_idx]
        rect = self.image.get_rect()
        rect.left, rect.top = self.rect.left, self.rect.top
        self.rect = rect
        self.mask = pygame.mask.from_surface(self.image)
    def remove(self):
        self.kill()    
        
class obstacle_manager():
    def __init__(self, obstacle_class,obstacle_image,cfg):
        """
        初始化障碍物管理器
        :param obstacle_classes: 障碍物类的列表
        :param obstacle_images: 障碍物图片的列表
        :param cfg: 游戏配置
        :param spawn_intervals: 生成时间间隔的列表
        """
        self.cfg = cfg
        self.obstacles =obstacle_class
        self.obstacle_images =obstacle_image
        self.obstacle_sprites_groups = [pygame.sprite.Group() for _ in range(len(self.obstacles))]
        self.add_obstacle_timer = 0
        self.obstacles_spawn_intervals = [80, 100, 60, 100]
        self.generated_obstacles = [0,1,1,0]
        self.current_interval_index = 0  # 当前使用的时间间隔索引
        self.current_interval = self.obstacles_spawn_intervals[0]-1


    def add_obstacle(self, time):

        if time >= self.current_interval:
            obstacle = self.generated_obstacles[self.current_interval_index]
            self.generate_obstacle(obstacle)

            self.current_interval_index += 1
            if self.current_interval_index < len(self.obstacles_spawn_intervals):
                self.current_interval = time + self.obstacles_spawn_intervals[self.current_interval_index]
            else:
                self.current_interval = float('inf')


    def generate_obstacle(self, obstacle_type):
        """
        根据障碍物类型生成障碍物
        :param obstacle_type: 障碍物类型索引
        """
        if obstacle_type == 0:  # 生成第一种障碍物
            self.obstacle_sprites_groups[0].add(self.obstacles[0](self.obstacle_images[0]))
        elif obstacle_type == 1:  # 生成第二种障碍物
            self.obstacle_sprites_groups[1].add(self.obstacles[1](
                self.obstacle_images[1],
                position=(600, self.cfg.SCREENSIZE[1] * 0.60 / 2,)
            ))

    def update(self):
        """
        更新障碍物
        """
        for group in self.obstacle_sprites_groups:
            group.update()

    def draw(self, screen):
        """
        绘制障碍物
        :param screen: 游戏屏幕
        """
        for group in self.obstacle_sprites_groups:
            group.draw(screen)

    def collide(self, dino, sounds):
        """
        检测碰撞并处理
        :param dino: 角色
        :param sounds: 音效
        :return: 碰撞计数
        """
        obs_collisions = 0
        for group in self.obstacle_sprites_groups:
            for obstacle in group:
                if pygame.sprite.collide_mask(dino, obstacle):
                    # dino.die(sounds)  # 可根据需要解开此行
                    obs_collisions += 1
                    obstacle.kill()  # 从组中移除障碍物
        return obs_collisions