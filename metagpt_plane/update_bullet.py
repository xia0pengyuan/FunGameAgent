
# bullet.py

import math
import time

class Bullet:
    def __init__(self, x, y, angle, speed):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = speed

    def update(self):
        self.x += self.speed * math.cos(math.radians(self.angle))
        self.y += self.speed * math.sin(math.radians(self.angle))

    @staticmethod
    def player_fire(x, y, buff_num2=None):
        if buff_num2 == 2:  # Spiral Barrage
            return Bullet.spiral_barrage(x, y)
        else:
            return Bullet.default_bullet(x, y)

    @staticmethod
    def spiral_barrage(x, y):
        bullets = []
        num_bullets = 12
        angle_increment = 360 / num_bullets
        for i in range(num_bullets):
            angle = i * angle_increment
            speed = 5  # Adjust speed as necessary
            bullets.append(Bullet(x, y, angle, speed))
        return bullets

    @staticmethod
    def default_bullet(x, y):
        return [Bullet(x, y, 0, 10)]  # Default bullet behavior


# buff1.py

class Buff1:
    def __init__(self):
        self.buff_num1 = 1  # Example buff number

    def apply_buff(self):
        # Logic for applying buff1
        pass


# buff2.py

class Buff2:
    def __init__(self):
        self.buff_num2 = 2  # Spiral Barrage buff number

    def apply_buff(self):
        # Logic for applying buff2
        pass
