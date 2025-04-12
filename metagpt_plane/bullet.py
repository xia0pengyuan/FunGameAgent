import pygame
from plane_sprites import GameSprite
import random
from constants import *
import math


class Bullet(GameSprite):

    def __init__(self, color=1, speedy=-2, speedx=0, enemy_group=None, angle=0, wave_amplitude=0, homing_target=None):
        self.hity = color
        self.enemy_group = enemy_group
        self.target_enemy = homing_target
        self.wave_amplitude = wave_amplitude
        self.spiral_angle = angle
        self.frame_count = 0
        image = pygame.image.load("./images/bullet" + str(color) + ".png")
        super().__init__(image, speedy, speedx)

    def update(self):
        super().update()
        self.frame_count += 1

        # Homing mechanic
        if self.target_enemy:
            self.track_enemy()

        # Spiral motion
        elif self.spiral_angle:
            self.rect.x += int(5 * math.cos(math.radians(self.spiral_angle)))
            self.rect.y += int(5 * math.sin(math.radians(self.spiral_angle)))
            self.spiral_angle += 5

        # Wave pattern
        elif self.wave_amplitude:
            self.rect.x += int(self.wave_amplitude * math.sin(math.radians(self.frame_count * 10)))

        if self.rect.bottom < 0 or self.rect.y > 700:
            self.kill()

    def track_enemy(self):
        if self.target_enemy:
            dx = self.target_enemy.rect.centerx - self.rect.centerx
            dy = self.target_enemy.rect.centery - self.rect.centery
            dist = math.hypot(dx, dy)
            if dist > 0:
                self.rect.x += int(dx / dist * 5)
                self.rect.y += int(dy / dist * 5)

    @staticmethod
    def player_fire(player):
        # Basic firing
        if player.buff1_num == 0:
            bullet = Bullet()
            bullet.rect.bottom = player.rect.y
            bullet.rect.centerx = player.rect.centerx
            player.bullets.add(bullet)

        # Buff1 enhanced firing
        if player.buff1_num >= 1:
            for i in (0, 1):
                for j in range(2, player.buff1_num + 3):
                    bullet = Bullet(2, -3)
                    bullet.rect.bottom = player.rect.y - i * 20
                    offset = 15 * (j // 2)
                    bullet.rect.centerx = player.rect.centerx + (-1) ** j * offset
                    player.bullets.add(bullet)

        # Buff2 enhanced firing
        if player.buff2_num > 0:
            angle_offset = 0
            for i in range(player.buff2_num * 1):
                wave_amplitude = 5 * player.buff2_num if i % 2 == 0 else 0
                bullet = Bullet(3, -2, 0, angle=angle_offset, wave_amplitude=wave_amplitude)
                bullet.rect.bottom = player.rect.y
                bullet.rect.centerx = player.rect.centerx
                angle_offset += 36 // player.buff2_num
                player.bullets.add(bullet)


class Buff1(GameSprite):
    def __init__(self,x):
        image = pygame.image.load("./images/buff1.png")
        super().__init__(image, 1)
        self.rect.bottom = 0
        self.rect.x = x

    def update(self):
        super().update()
        if self.rect.bottom < 0:
            self.kill()


class Buff2(GameSprite):
    def __init__(self,x):
        image = pygame.image.load("./images/buff2.png")
        super().__init__(image, 2)
        self.rect.bottom = 0
        self.rect.x = x

    def update(self):
        super().update()
        if self.rect.bottom < 0:
            self.kill()
