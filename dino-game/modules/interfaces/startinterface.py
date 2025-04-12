
import pygame
from ..sprites import Dinosaur
#from .....utils import QuitGame
import sys
def QuitGame(use_pygame=True):
    if use_pygame: pygame.quit()
    sys.exit()

'''游戏开始界面'''
def GameStartInterface(screen, sounds, cfg, resource_loader):
    dino = Dinosaur(resource_loader.images['dino'])
    ground = resource_loader.images['ground'].subsurface((0, 0), (83, 19))
    rect = ground.get_rect()#获得矩形边界
    rect.left, rect.bottom = cfg.SCREENSIZE[0]/20, cfg.SCREENSIZE[1]/2 
    clock = pygame.time.Clock()
    press_flag = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                QuitGame()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    press_flag = True
                    dino.jump(sounds)
        dino.update()
        screen.fill(cfg.BACKGROUND_COLOR)
        screen.blit(ground, rect)
        dino.draw(screen)
        pygame.display.update()
        clock.tick(cfg.FPS)
        if (not dino.is_jumping) and press_flag:
            return True