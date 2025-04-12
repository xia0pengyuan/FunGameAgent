
import os
import random
import pygame
#from utils import QuitGame
from base import PygameBaseGame
from multiprocessing import Pool

#from modules.agent.agent import *
from modules.sprites.scene import *
from modules.sprites.obstacle import *
from modules.sprites.dinosaur import *
from modules.interfaces.endinterface import GameEndInterface
from modules.interfaces.startinterface import GameStartInterface
import sys
def QuitGame(use_pygame=True):
    if use_pygame: pygame.quit()
    sys.exit()
import numpy as np
import pickle



class Config():
    rootdir = os.path.split(os.path.abspath(__file__))[0]
    FPS = 60 
    TITLE = 'game'
    BACKGROUND_COLOR = (235, 235, 235)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    SCREENSIZE = (600, 300)
    IMAGE_PATHS_DICT = {
        'cacti': [os.path.join(rootdir, 'resources/images/cacti-big.png'), os.path.join(rootdir, 'resources/images/cacti-small.png')],
        'cloud': os.path.join(rootdir, 'resources/images/cloud.png'),
        'dino': [os.path.join(rootdir, 'resources/images/dino.png'), os.path.join(rootdir, 'resources/images/dino_ducking.png')],
        'gameover': os.path.join(rootdir, 'resources/images/gameover.png'),
        'ground': os.path.join(rootdir, 'resources/images/ground.png'),
        'numbers': os.path.join(rootdir, 'resources/images/numbers.png'),
        'ptera': os.path.join(rootdir, 'resources/images/ptera.png'),
        'replay': os.path.join(rootdir, 'resources/images/replay.png'),
        'knife': os.path.join(rootdir, 'resources/images/knife.png'),
        'gun': os.path.join(rootdir, 'resources/images/gun.png')
        
    }
  
    SOUND_PATHS_DICT = {
        'die': os.path.join(rootdir, 'resources/audios/die.wav'),
        'jump': os.path.join(rootdir, 'resources/audios/jump.wav'),
        'point': os.path.join(rootdir, 'resources/audios/point.wav')
    }
    

class dino_game(PygameBaseGame):
    game_type = 'trexrush'
    def __init__(self, **kwargs):
        self.cfg = Config()
        super(dino_game, self).__init__(config=self.cfg, **kwargs)
        self.run_ai = False
        self.actions = [pygame.K_UP,pygame.K_DOWN,pygame.K_DOWN,pygame.K_UP]
        #障碍物‘0’跳跃极限出现之后29帧数到45
        #跳跃持续37帧，也就是这之后38帧数才能做其他动作
        #障碍物‘1’的下蹲极限是出现之后22帧数到35帧数
        #下蹲持续时间30帧数，也就是这之后31帧数才能做其他动作
        self.spawn_intervals = [109, 131, 91, 138]

    def run(self):

        flag =  True
        basic_score = 0
        action_index = 0  
        action_timer = 0 
        interval_time =self.spawn_intervals[0] 
        duck_timer = 0  # 初始化下蹲计时器
        DUCK_DURATION = 30

        while flag:
           
            screen, resource_loader, cfg = self.screen, self.resource_loader, self.cfg
            
            game_score_board = Scoreboard(resource_loader.images['numbers'], position=(500, 15), bg_color=cfg.BACKGROUND_COLOR)
            
            dino = Dinosaur(resource_loader.images['dino'])
            ground = Ground(resource_loader.images['ground'], position=(0, cfg.SCREENSIZE[1]/2))
            
            obstacle_class = obstacle_manager(obstacle_class = [Cactus,Ptera],obstacle_image = [resource_loader.images['cacti'],resource_loader.images['ptera']],cfg = self.cfg)
            
            cloud_sprites_group = pygame.sprite.Group()
            
            score_timer = 0
         
            clock = pygame.time.Clock()
            while True:
                action_timer += 1
                if action_index < len(self.actions):  # 确保索引不超过 action_list 的长度
                    
                    if action_timer >= interval_time:
                        current_action = self.actions[action_index]  
                        
                        if current_action == pygame.K_UP:  # 跳跃
                            dino.jump(resource_loader.sounds)
                        elif current_action == pygame.K_DOWN:  # 下蹲
                            print(interval_time)
                            dino.duck()
                            duck_timer = DUCK_DURATION  # 设置下蹲持续时间

                        action_index += 1  # 切换到下一个动作
                        if action_index < len(self.actions):
                            interval_time += self.spawn_intervals[action_index]

                if dino.is_ducking:
                    if duck_timer > 0:
                        duck_timer -= 1  # 减少计时器
                    else:
                        dino.unduck() 
                
                obstacle_class.add_obstacle(action_timer)
                    
                screen.fill(cfg.BACKGROUND_COLOR)
                
                if len(cloud_sprites_group) < 5 and random.randrange(0, 300) == 10:
                    cloud_sprites_group.add(Cloud(resource_loader.images['cloud'], position=(cfg.SCREENSIZE[0], random.randrange(30, 75))))
                
                obstacle_class.add_obstacle_timer += 1
                
                dino.update()
                ground.update()
                
                obstacle_class.update()
                cloud_sprites_group.update()
                score_timer += 1

                obsticle_collide_score = obstacle_class.collide(dino,resource_loader.sounds)
                
                basic_score = basic_score-500*obsticle_collide_score
                
                dino.draw(screen)
                ground.draw(screen)
                cloud_sprites_group.draw(screen)
                obstacle_class.draw(screen)

                game_score_board.set(basic_score)
                
                game_score_board.draw(screen)
                
                pygame.display.update()
                clock.tick(cfg.FPS)
                # --游戏是否结束
                if dino.is_dead:
                    break
                
                if action_timer>=500:
                    break
          
            if not self.run_ai:
                flag = GameEndInterface(screen, cfg, resource_loader)
            else:
                return basic_score


if __name__ == '__main__':
    dino = dino_game() 
    dino.run() 
