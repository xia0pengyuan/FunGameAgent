
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
from modules.sprites.weapon import *
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
    
    def run(self,run_ai =False):
        self.run_ai = run_ai
     
        flag =  True
        basic_score = 0
        while flag:
           
            screen, resource_loader, cfg = self.screen, self.resource_loader, self.cfg

            score = 0
            
            game_score_board = Scoreboard(resource_loader.images['numbers'], position=(336, 15), bg_color=cfg.BACKGROUND_COLOR)
            
            dino = Dinosaur(resource_loader.images['dino'])
            ground = Ground(resource_loader.images['ground'], position=(0, cfg.SCREENSIZE[1]/2))
            sub = SUB(resource_loader.images['knife'],resource_loader.images['gun'])
            
            obstacle_class = obstacle_manager(obstacle_class = [Cactus,Ptera],obstacle_image = [resource_loader.images['cacti'],resource_loader.images['ptera']],cfg = self.cfg)
            weapon_class = Weapon_manager(Weapon_class =[knife,gun],Weapon_image =[resource_loader.images['knife'],resource_loader.images['gun']] ,cfg = self.cfg)

            cloud_sprites_group = pygame.sprite.Group()
            
            score_timer = 0
         
            clock = pygame.time.Clock()
            while True:
                if not self.run_ai:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            QuitGame()
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                                dino.jump(resource_loader.sounds)
                            elif event.key == pygame.K_DOWN:
                                dino.duck()
                            elif event.key == pygame.K_a:
                                weapon_class.use_weapon(dino,0)
                            elif event.key == pygame.K_d:
                                weapon_class.use_weapon(dino,1)
                                
                        elif event.type == pygame.KEYUP:
                            if event.key == pygame.K_DOWN:
                                dino.unduck()
                            elif event.key == pygame.K_a:
                                weapon_class.use_weapon(dino,3)  
                                
        
                obstacle_class.add_obstacle()
                weapon_class.add_Weapon()
                    
                screen.fill(cfg.BACKGROUND_COLOR)
                
                if len(cloud_sprites_group) < 5 and random.randrange(0, 300) == 10:
                    cloud_sprites_group.add(Cloud(resource_loader.images['cloud'], position=(cfg.SCREENSIZE[0], random.randrange(30, 75))))
                
                obstacle_class.add_obstacle_timer += 1
                
                dino.update()
                ground.update()
                sub.update()
                
                obstacle_class.update()
                cloud_sprites_group.update()
                weapon_class.update()
                score_timer += 1
               
                if score_timer > (cfg.FPS//12):
                    score_timer = 0
                    score += 1
                    score = min(score, 99999)
                    if score % 100 == 0:
                        resource_loader.sounds['point'].play()

                weapon_get_score = weapon_class.dino_get_detect_collide(dino)          
                weapon_use_score = weapon_class.weapon_obstacle_collide(dino,obstacle_class)#障碍物与武器碰撞
                obsticle_collide_score = obstacle_class.collide(dino,resource_loader.sounds)
                
                basic_score = basic_score+50*weapon_get_score+300*weapon_use_score-500*obsticle_collide_score
                
                dino.draw(screen)
                ground.draw(screen)
                cloud_sprites_group.draw(screen)
                obstacle_class.draw(screen)
                weapon_class.draw(screen)
                weapon_class.weapon_update(screen)
                
                game_score_board.set(basic_score)
                
                game_score_board.draw(screen)
                
                sub.draw(screen,weapon_class.weapon_index)
                # --更新屏幕
                pygame.display.update()
                clock.tick(cfg.FPS)
                # --游戏是否结束
                if dino.is_dead:
                    break
                score += 1
                
                if score>=1500:
                    break
          
            if not self.run_ai:
                flag = GameEndInterface(screen, cfg, resource_loader)
            else:
                return basic_score


    

    

if __name__ == '__main__':
    dino = dino_game() 
    dino.run() 
