import pygame
import random
import math


class knife(pygame.sprite.Sprite):
    def __init__(self, image, position, size=(20, 30), **kwargs):
        pygame.sprite.Sprite.__init__(self)
        # 导入图片
        self.images = []
        #image = pygame.image.load(image)
        self.images.append(pygame.transform.scale(image, size))
        self.image_idx = 0
        self.image = self.images[self.image_idx]
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.centery = position
        self.mask = pygame.mask.from_surface(self.image)
        # 定义一些必要的变量
        self.speed = -10
        self.refresh_rate = 10
        self.refresh_counter = 0
        self.coll = 0
    '''画到屏幕上'''
    def draw(self, screen):
        screen.blit(self.image, self.rect)
    '''更新'''
    def remove(self):
        self.kill()
    def update(self):
        self.loadImage()
        self.rect = self.rect.move([self.speed, 0])
        if self.coll == 1:
            self.kill()
        if self.rect.right < 0:
            self.kill()
        #self.refresh_counter += 1
    '''载入当前状态的图片'''
    def loadImage(self):
        self.image = self.images[0]
        rect = self.image.get_rect()
        rect.left, rect.top = self.rect.left, self.rect.top
        self.rect = rect
        self.mask = pygame.mask.from_surface(self.image)
        

class gun(pygame.sprite.Sprite):
    def __init__(self, image, position, size=(60, 20), **kwargs):
        pygame.sprite.Sprite.__init__(self)
        # 导入图片
        self.images = []
        #image = pygame.image.load(image)
        self.images.append(pygame.transform.scale(image, size))
        self.image_idx = 0
        self.image = self.images[self.image_idx]
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.centery = position
        self.mask = pygame.mask.from_surface(self.image)
        # 定义一些必要的变量
        self.speed = -10
        self.refresh_rate = 10
        self.refresh_counter = 0
        self.coll = 0
        self.Bullet = False
        
        self.bullets = pygame.sprite.Group()
    '''画到屏幕上'''
    def draw(self, screen):
        screen.blit(self.image, self.rect)
    '''更新'''
    def remove(self):
        self.kill()
    def update(self):
        self.loadImage()
        self.rect = self.rect.move([self.speed, 0])
        if self.coll == 1:
            self.kill()
        if self.rect.right < 0:
            self.kill()
        #self.refresh_counter += 1
    '''载入当前状态的图片'''
    def loadImage(self):
        self.image = self.images[0]
        rect = self.image.get_rect()
        rect.left, rect.top = self.rect.left, self.rect.top
        self.rect = rect
        self.mask = pygame.mask.from_surface(self.image)
    
    def shoot(self,dino):
        bullet = gun.Bullet(dino.rect.midright)
        self.bullets.add(bullet)
        
        
        
    class Bullet(pygame.sprite.Sprite):
        def __init__(self, position):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.Surface((10, 5))
            self.image.fill((255, 0, 0))  
            self.rect = self.image.get_rect()
            self.rect.midleft = position
            self.speed = 10

        def update(self):
            self.rect.x += self.speed
            if self.rect.left > 800:  # 屏幕右边界外移除子弹
                self.kill()
                
        

class Weapon_base():
    def __init__(self, Weapon_class,Weapon_image,cfg):
        #super().__init__()
        self.cfg = cfg
        self.Weapon = Weapon_class
        self.Weapon_image = Weapon_image
        self.Weapon_sprites_group = []
        for i in range(len(self.Weapon)):
            self.Weapon_sprites_group.append(pygame.sprite.Group())
        
        self.weapon_index = [0]*len(self.Weapon)
        self.use_weapon_index = [0]*len(self.Weapon)
        
    def add_Weapon(self):#这个应该不用修改
        for i in range(len(self.Weapon_sprites_group)):
            if 2>random.randrange(0, 500):
                position_ys = [self.cfg.SCREENSIZE[1]*0.82/2, self.cfg.SCREENSIZE[1]*0.75/2, self.cfg.SCREENSIZE[1]*0.60/2, self.cfg.SCREENSIZE[1]*0.20/2]
                self.Weapon_sprites_group[i].add(self.Weapon[i](self.Weapon_image[i],position=(600, random.choice(position_ys))))
        
    def update(self):# 改
        for i in range(len(self.Weapon_sprites_group)):
            for sprites in self.Weapon_sprites_group[i]:
                sprites.update()
        
        #self.bullt_gun.bullets.update()
        
        
    def draw(self,screen):# 改
        for i in range(len(self.Weapon_sprites_group)):
            for sprites in self.Weapon_sprites_group[i]:
                sprites.draw(screen)    
            
        #self.bullt_gun.bullets.draw(screen)
        
        
    def dino_get_detect_collide(self,dino): #恐龙与武器碰撞得到相应武器
        weapom_get_index = 0
        for i in range(len(self.Weapon_sprites_group)):
            for item in self.Weapon_sprites_group[i]:
                if pygame.sprite.collide_mask(dino, item):
                        item.remove()
                        if self.weapon_index[i] == 0:
                            self.weapon_index = [0]*len(self.Weapon)
                            self.weapon_index[i] = 1
                            weapom_get_index += 1
        return weapom_get_index
                            
                            
                
class Weapon_manager(Weapon_base):
    def __init__(self, Weapon_class, Weapon_image, cfg):
        super().__init__(Weapon_class, Weapon_image, cfg)

        self.bullt_gun = self.Weapon[1](self.Weapon_image[1], position=(300, 300))  # Gun with bullets
        

    def weapon_update(self, screen):
        self.bullt_gun.bullets.update()
        self.bullt_gun.bullets.draw(screen)

        
    def use_weapon(self, dino, index):  # Control dino to use weapon
        if self.weapon_index[0] == 1 and index == 0:  # Knife
            self.use_weapon_index[0] = 1
            self.weapon_index[0] = 0

        if self.weapon_index[1] == 1 and index == 1:  # Gun
            self.use_weapon_index[1] = 1
            self.bullt_gun.shoot(dino)
            self.weapon_index[1] = 0

        
        if index == 3:  # Knife
            self.use_weapon_index[0] = 0

    def weapon_obstacle_collide(self, dino, obstacle_manager):  # Detect weapon interaction with obstacles
        obstacle_die_index = 0
        if self.use_weapon_index[0] == 1:  # Knife
            for i in range(len(obstacle_manager.obsticle)):
                for item in obstacle_manager.obsticle_sprites_group[i]:
                    if pygame.sprite.collide_mask(dino, item):
                        item.remove()
                        obstacle_die_index += 1
                        self.use_weapon_index[0] = 0

        if self.use_weapon_index[1] == 1:  # Gun
            for i in range(len(obstacle_manager.obsticle)):
                for bullet in self.bullt_gun.bullets:
                    for item in obstacle_manager.obsticle_sprites_group[i]:
                        if pygame.sprite.collide_mask(bullet, item):
                            item.remove()
                            obstacle_die_index += 1
                            bullet.kill()

        

        return obstacle_die_index

                                     
        
