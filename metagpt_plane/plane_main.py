import sys
import pygame
import time
pygame.init()
from plane_sprites import *

from bullet import Buff1, Buff2
from player import Heromate, Hero
from enemy import Boss, Enemy
import json


class PlaneGame(object):
    """飞机大战主游戏"""

    def __init__(self):

        # 1. 创建游戏的窗口

        self.screen = pygame.display.set_mode(SCREEN_RECT.size)
        self.score = GameScore()
        # 创建结束界面
        self.canvas_over = CanvasOver(self.screen, self.score)
        # 2. 创建游戏的时钟
        self.clock = pygame.time.Clock()
        # 3. 调用私有方法，精灵和精灵组的创建
        self.__create_sprites()
        # 分数对象
        self.score = GameScore()
        # 程序控制指针
        self.index = 0
        # 音乐bgm
        self.bg_music = pygame.mixer.Sound("./music/game_music.ogg")
        self.bg_music.set_volume(0.3)
        self.bg_music.play(-1)
        # 游戏结束了吗
        self.game_over = False
        
        # 4. 设置定时器事件 - 创建敌机　1s
        pygame.time.set_timer(CREATE_ENEMY_EVENT, random.randint(1000, 2000))
        pygame.time.set_timer(HERO_FIRE_EVENT, 400)
        pygame.time.set_timer(BUFF1_SHOW_UP, random.randint(2000, 10000))
        pygame.time.set_timer(BUFF2_SHOW_UP, random.randint(1000, 10000))
        pygame.time.set_timer(ENEMY_FIRE_EVENT, 2000)
        pygame.time.set_timer(OUTPUT_CONTROL_EVENT, 200)
        self.control_lists = []

    def __create_sprites(self):

        # 创建背景精灵和精灵组
        bg1 = Background()
        bg2 = Background(True)

        self.back_group = pygame.sprite.Group(bg1, bg2)

        # 创建敌机的精灵组

        self.enemy_group = pygame.sprite.Group()

        # 创建英雄的精灵和精灵组
        self.hero = Hero()
        self.hero_group = pygame.sprite.Group(self.hero)

        # 创建敌军子弹组
        self.enemy_bullet_group = pygame.sprite.Group()

        # 血条列表
        self.bars = []
        self.bars.append(self.hero.bar)

        # 创建buff组
        self.buff1_group = pygame.sprite.Group()

        # 创建假象boom组
        self.enemy_boom = pygame.sprite.Group()

        # bomb列表
        self.bombs = []

    def start_game(self):

        while True:


            self.clock.tick(FRAME_PER_SEC)
            # 2. 事件监听
            self.__event_handler()
            # 3. 碰撞检测
            self.__check_collide()
            # 4. 更新/绘制精灵组
            self.__update_sprites()

            # 是否要结束游戏

            if self.game_over:
                self.canvas_over.update()
                return self.control_lists

            # 5. 更新显示
            pygame.display.update()

    def __event_handler(self):  # 事件检测
        #判断是否足以生成boss
        if self.score.getvalue() > 200+500*self.index:
            self.boss = Boss()
            self.enemy_group.add(self.boss)
            self.bars.append(self.boss.bar)
            self.index += 1

        for event in pygame.event.get():
            # 判断是否退出游戏
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == CREATE_ENEMY_EVENT:
                # 创建敌机精灵将敌机精灵添加到敌机精灵组
                if self.score.getvalue() < 20:
                    enemy = Enemy()
                else:
                    if random.randint(0, 100) % 4:
                        enemy = Enemy()
                    else:
                        enemy = Enemy(2)

                self.enemy_group.add(enemy)
                self.bars.append(enemy.bar)
            elif event.type == HERO_FIRE_EVENT:
                for hero in self.hero_group:
                    hero.fire(self.enemy_group)
            elif event.type == BUFF1_SHOW_UP:
                buff1 = Buff1()
                self.buff1_group.add(buff1)
            elif event.type == BUFF2_SHOW_UP:
                buff = Buff2()
                self.buff1_group.add(buff)
            elif event.type == OUTPUT_CONTROL_EVENT:
                self.output_control()
            else:
                if self.game_over:
                    flag = self.canvas_over.event_handler(event)
                    if flag == 1:
                        self.__start__()
                    elif flag == 0:
                        pygame.quit()
                        sys.exit()
                        
        # 使用键盘提供的方法获取键盘按键 - 按键元组
        keys_pressed = pygame.key.get_pressed()
        # 判断元组中对应的按键索引值 1
        if keys_pressed[pygame.K_RIGHT]:
            self.hero.speedx = 5
        elif keys_pressed[pygame.K_LEFT]:
            self.hero.speedx = -5
        else:
            self.hero.speedx = 0

        # 处理垂直移动
        if keys_pressed[pygame.K_UP]:
            self.hero.speedy = -5
        elif keys_pressed[pygame.K_DOWN]:
            self.hero.speedy = 5
        else:
            self.hero.speedy = 0

    def output_control(self):
        keys_pressed = pygame.key.get_pressed()
        controls = [0, 0, 0, 0]  # 初始化控制列表

        # 检查每个方向键的按键状态
        if keys_pressed[pygame.K_RIGHT]:
            controls[0] = 1
        if keys_pressed[pygame.K_LEFT]:
            controls[1] = 1
        if keys_pressed[pygame.K_UP]:
            controls[2] = 1
        if keys_pressed[pygame.K_DOWN]:
            controls[3] = 1
        self.control_lists.append(controls)

    def heros_move(self, x=0, y=0):
        self.hero.speedx = x
        self.hero.speedy = y


    def __check_collide(self):

        for enemy in self.enemy_group:
            for hero in self.hero_group:
                for bullet in hero.bullets:
                    if pygame.sprite.collide_mask(bullet, enemy):  # 这种碰撞检测可以精确到像素去掉alpha遮罩的那种哦
                        bullet.kill()
                        enemy.injury = bullet.hity
                        enemy.isboom = True
                        if enemy.bar.length <= 0:
                            self.enemy_group.remove(enemy)
                            self.enemy_boom.add(enemy)
                            enemy.isboom = True
                            self.score.increase(enemy.number * 10)

        # 2. 敌机撞毁英雄
        for enemy in self.enemy_group:
            if pygame.sprite.collide_mask(self.hero, enemy):
                if enemy.number < 3:
                    enemy.bar.length = 0  # 敌机直接死
                    self.hero.injury = self.hero.bar.value / 4  # 英雄掉四分之一的血
                    self.enemy_group.remove(enemy)
                    self.enemy_boom.add(enemy)
                    enemy.isboom = True
                else:
                    self.hero.bar.length = 0
                self.hero.isboom = True

        # 子弹摧毁英雄
        for bullet in self.enemy_bullet_group:
            if pygame.sprite.collide_mask(self.hero, bullet):
                bullet.kill()
                self.hero.injury = 1
                if self.hero.buff1_num > 0:
                    self.hero.music_degrade.play()
                    if self.hero.buff1_num== 5:
                        self.mate1.kill()
                        self.mate2.kill()
                    self.hero.buff1_num -= 1

                self.hero.isboom = True

        if not self.hero.alive():
            self.hero.rect.right = -10  # 把英雄移除屏幕
            if self.hero.buff1_num == 5:
                self.mate1.rect.right = -10
                self.mate2.rect.right = -10
            self.game_over = True

        # 3.buff吸收
        for buff in self.buff1_group:
            if pygame.sprite.collide_mask(self.hero, buff):
                if buff.speedy == 1:  # 用速度来区分
                    if self.hero.buff1_num < 6:
                        self.hero.buff1_num += 1
                        if self.hero.buff1_num == 5:
                            self.team_show()
                    #self.score.increase(enemy.number * 10)
                
                elif buff.speedy==2:
                        self.hero.buff2_num += 1
                #修改部分
                buff.kill()

    def team_show(self):
        self.mate1 = Heromate(-1)
        self.mate2 = Heromate(1)
        self.mate1.image = pygame.image.load("./images/life.png")
        self.mate1.rect = self.mate1.image.get_rect()
        self.mate2.image = pygame.image.load("./images/life.png")
        self.mate2.rect = self.mate2.image.get_rect()
        self.hero_group.add(self.mate1)
        self.hero_group.add(self.mate2)

    # 各种更新
    def __update_sprites(self):

        self.back_group.update()
        self.back_group.draw(self.screen)

        self.enemy_group.update()
        self.enemy_group.draw(self.screen)

        self.enemy_boom.update()
        self.enemy_boom.draw(self.screen)

        self.heros_update()
        self.hero_group.draw(self.screen)

        for hero in self.hero_group:
            hero.bullets.update()
            hero.bullets.draw(self.screen)

        self.buff1_group.update()
        self.buff1_group.draw(self.screen)

        self.bars_update()
        self.bombs_update()

        self.enemy_bullet_group.update()
        self.enemy_bullet_group.draw(self.screen)

        self.score_show()

    def heros_update(self):
        for hero in self.hero_group:
            if hero.number == 1:
                hero.rect.bottom = self.hero.rect.bottom
                hero.rect.left = self.hero.rect.right
            if hero.number == -1:
                hero.rect.bottom = self.hero.rect.bottom
                hero.rect.right = self.hero.rect.left
            hero.update()

    def bars_update(self):
        for bar in self.bars:
            if bar.length > 0:
                bar.update(self.screen)
            else:
                self.bars.remove(bar)

    def bullet_enemy_update(self):
        for enemy in self.enemy_group:
            enemy.bullets.update()
            enemy.bullets.draw(self.screen)

    def bombs_update(self):
        i = 1
        for bomb in self.bombs:
            self.screen.blit(bomb, (0, 700 - (bomb.get_rect().height) * i))
            i += 1

    def score_show(self):
        score_font = pygame.font.Font("./STCAIYUN.ttf", 33)
        image = score_font.render("SCORE:" + str(int(self.score.getvalue())), True, color_gray)
        rect = image.get_rect()
        rect.bottom, rect.right = 700, 480
        self.screen.blit(image, rect)

    @staticmethod
    def __start__():
    # 创建游戏对象
        game = PlaneGame()

        # 启动游戏，并获取控制列表
        control_lists = game.start_game()

        # 返回控制列表
        return control_lists


if __name__ == '__main__':
    try:
        control_lists = PlaneGame.__start__()
        # 确保输出为 JSON 格式
        print(json.dumps(control_lists))
    except Exception as e:
        # 如果发生错误，输出错误信息
        print(json.dumps({"error": str(e)}))
