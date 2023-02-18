"""
One Hundred Thousandaire - An Action Scroller
This application was inspired by:
    Create an Idle Clicker Adventure Capitalist Style Game in Python Using Pygame! Full Game In An HOUR!
    https://www.youtube.com/watch?v=qCA7FBwKOgI
This version extends the youtube version by adding a speed multiplier as well as 
storing and graphing the results of the player actions.  
"""
__author__      = "Anthony B. Washington"
__license__     = 'MIT'  # https://mit-license.org/

import datetime
from matplotlib.dates import DateFormatter, MinuteLocator
import pandas as pd
import json
import os
import sys
import matplotlib.pyplot as plt


import numpy as np
import pygame

BUFFER = 200
MONITOR_WIDTH = 1920 - BUFFER
WIDTH = 760     #    420
HEIGHT = 680    #    620
FPS = 60

# colors
red     = (255, 000, 000) # #ff0000
orange  = (255, 127, 000) # #ff7f00
yellow  = (255, 255, 000) # #ffff00
green   = (000, 255, 000) # #00ff00
xxxblue = (000, 000, 255) # 
blue    = ( 30, 144, 255) # #1e90ff
violet  = (148, 000, 211) # #9400d3
gray    = (211, 211, 211) # #d3d3d3
xxxgray = ( 51,  51,  51) # 
black   = (  0,   0,   0) # 
white   = (255, 255, 255) # 
gold    = (255, 215,   0) # #ffd700

class Button(pygame.sprite.Sprite):
    """The base sprite class of the button objects. 

    Args:
        pygame (module): The pygame sprite module

    """
    def __init__(self, pos, images):
        super().__init__()
        self.images = images + list(reversed(images))
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.is_animating = False

    def animate(self):
        self.is_animating = True

    def update(self):
        if self.is_animating == True:
            self.index += 1
            if self.index % len(self.images) == 0:
                self.index = 0
                self.is_animating = False
            self.image = self.images[self.index]


class Game():
    """The game class is the main entry point and state manager of the 
    applicataion.
    """
    def __init__(self):
        """The Game class constructor.  
        
        Here we initialize pygame and all game objects.  
        """

        pygame.init()
        pygame.mixer.init()

        self.action_start_time = 0
        self.elapsed_time = 0
        self.width, self.height = WIDTH, HEIGHT  
        # dev_pos_x = MONITOR_WIDTH - WIDTH 
        # dev_pos_y = 133 
        # os.environ['SDL_VIDEO_WINDOW_POS'] = '%i,%i' % (dev_pos_x,dev_pos_y)
        game_icon = pygame.image.load('img/img_gold_pile.png')
        pygame.display.set_icon(game_icon)
        self.screen = pygame.display.set_mode((self.width, self.height))   
        pygame.display.set_caption("One Hundred Thousandaire")
        self.fps = 1260
        self.game_clock = pygame.time.Clock()  
        self.font = pygame.font.SysFont('Segoe UI Bold', 24)
        self.background_sound = pygame.mixer.music.load('snd/snd_background_loop.ogg')
        self.task_click_sound = pygame.mixer.Sound('snd/snd_task_click.wav')
        self.buy_click_sound = pygame.mixer.Sound('snd/snd_buy_click.ogg')

        self.all_sprites = pygame.sprite.Group()
        red_task_images   = self.get_task_images('red')
        self.red_task = Button((100, 100), red_task_images)
        self.all_sprites.add(self.red_task)


        self.is_running = True

    def get_task_images(self, btn_color):
        list = []
        path = f'img/{btn_color}/task/'
        for idx in range(8):
            img_path = path + f'{btn_color}_task_{idx}.png'
            list.append(pygame.image.load(img_path).convert_alpha())

        return list


    def run(self):
        """The method to loop through the game states. 
        """
        #pygame.mixer.music.play(loops=-1)

        while self.is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # if event.type == pygame.KEYDOWN:
                #     self.red_task.animate()
                if event.type == pygame.MOUSEBUTTONUP and not self.red_task.is_animating:
                    mouse_pos = pygame.mouse.get_pos()
                    for sprite in self.all_sprites:
                        if sprite.rect.collidepoint(mouse_pos) and self.red_task.is_animating == False:
                            self.task_click_sound.play()
                            self.red_task.animate()



            self.screen.fill((0,0,0))
            self.all_sprites.draw(self.screen)
            self.all_sprites.update()
            pygame.display.flip()
            self.game_clock.tick(FPS)
        
        pygame.quit()
        sys.exit(0)
        
if __name__ == "__main__":
    game = Game()
    game.run()

