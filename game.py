"""
One Hundred Thousandaire - An Idle Clicker
This application was inspired by:
    Create an Idle Clicker Adventure Capitalist Style Game in Python Using Pygame! Full Game In An HOUR!
    https://www.youtube.com/watch?v=qCA7FBwKOgI
"""
__author__      = "Anthony B. Washington"
__license__     = 'MIT'  # https://mit-license.org/

import datetime
import pandas as pd
import json
import os
import sys
import time

import matplotlib

matplotlib.use("Agg")

import matplotlib.backends.backend_agg as agg
import matplotlib.pyplot as plt
import matplotlib.figure

import numpy as np
import pygame
# from matplotlib.axis import Axis

BUFFER = 200
MONITOR_WIDTH = 1920 - BUFFER
WIDTH = 760    #    420
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
gold    = (255, 215,   0) # 



class Splash():
    """The introductory splash screen for One Hundred Thousandaire
    """
    def __init__(self, game):
        """The Splash screen constructor

        Args:
            game (_type_): A reference to the game object. 
        """
        self.game = game
        self.screen_splash = pygame.image.load('screen_splash1.png').convert_alpha()
    def on_event(self, event):
        """The method to manage pygame events upon each cycle. 

        Args:
            event (_type_): _description_
        """
        if event.type == pygame.QUIT:
            self.game.is_running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.start_now_button.collidepoint(event.pos):
                self.game.game_state = 'action'
            if self.leaderboard_button.collidepoint(event.pos):
                self.game.leaderboard = Leaderboard(self.game)
                self.game.game_state = 'leaderboard'

    def on_update(self):
        """The method to modify game objects.  """
        pass 
    def on_render(self):
        """The method to draw game objects to the screen. 
        """
        self.game.screen.blit(self.screen_splash, (0, 0))

        self.start_now_button = pygame.draw.rect(self.game.screen, gray, [int(WIDTH * 0.25)-50, 600, 100, 40])
        self.start_now_text = self.game.font.render("Start Now", True, black)
        self.game.screen.blit(self.start_now_text, (int(WIDTH * 0.25)-38, 612))
        self.leaderboard_button = pygame.draw.rect(self.game.screen, gray, [int(WIDTH * 0.75)-50, 600, 100, 40])
        self.leaderboard_text = self.game.font.render("Leaderboard", True, xxxblue)
        self.game.screen.blit(self.leaderboard_text, (int(WIDTH * 0.75) - 50, 612))        

        pygame.display.flip()
    def run(self):
        """The method to control the splash screen.  
        """
        for event in pygame.event.get():
            self.on_event(event)
        self.on_update()
        self.on_render()
           
class Action():
    """The class to handle all in game action. 

    Returns:
        _type_: _description_
    """
    def __init__(self, game):
        """The Action screen constructor

        Args:
            game (_type_): A reference to the game object. 
        """

        self.game = game          
        self.screen_action = pygame.image.load('screen_action1.png').convert_alpha()
        self.TASK_LENGTH = 450
       
        # game variables
        self.red_value      = 1
        self.orange_value   = 2
        self.yellow_value   = 3
        self.green_value    = 4
        self.blue_value     = 5
        self.gray_value     = 6
        self.violet_value   = 7
        self.drawing_red    = False
        self.drawing_orange = False
        self.drawing_yellow = False
        self.drawing_green  = False
        self.drawing_blue   = False
        self.drawing_gray   = False
        self.drawing_violet = False
        self.red_length     = 0
        self.orange_length  = 0
        self.yellow_length  = 0
        self.green_length   = 0
        self.blue_length    = 0
        self.gray_length    = 0
        self.violet_length  = 0
        self.red_speed      = 7
        self.orange_speed   = 6
        self.yellow_speed   = 5
        self.green_speed    = 4
        self.blue_speed     = 3
        self.gray_speed     = 2
        self.violet_speed   = 1

        # draw buttons variables
        self.red_value_cost = 1   
        self.red_owned = False
        self.red_manager_cost = 100
        self.red_multiplier_cost = 500
        self.orange_value_cost = 2
        self.orange_owned = False
        self.orange_manager_cost = 500
        self.orange_multiplier_cost = 1800
        self.yellow_value_cost = 3
        self.yellow_owned = False
        self.yellow_manager_cost = 1800
        self.yellow_multiplier_cost = 4000
        self.green_value_cost = 4
        self.green_owned = False
        self.green_manager_cost = 4000
        self.green_multiplier_cost = 10000
        self.blue_value_cost = 5
        self.blue_owned = False
        self.blue_manager_cost = 10000
        self.blue_multiplier_cost = 25000
        self.gray_value_cost = 6
        self.gray_owned = False
        self.gray_manager_cost = 25000
        self.gray_multiplier_cost = 60000
        self.violet_value_cost = 7
        self.violet_owned = False
        self.violet_manager_cost = 60000
        self.violet_multiplier_cost = 120000

    def draw_task(self, color, y_coord, value, draw, owned, length, speed):
        """The method to create the game task icons. 

        Args:
            color (Color): The RGB color of the task. 
            y_coord (int): The height position of the task. 
            value (int): The amount returned to the player after a task completes. 
            *draw (bool): The flag to test if the task is drawing the progress bar. 
            *length (int): The amount to update the task progress bar. 
            *speed (float): The speed at which to update the task progress bar. 

        Returns:
            A task object. 
        """
        if draw and length == self.TASK_LENGTH:
            draw = False
            length = 0
            self.game.score += value
        elif draw and self.TASK_LENGTH - length >= speed: # if the task button has been clicked and the task is not complete
            length += speed        
        elif draw and self.TASK_LENGTH - length < speed:
            length = self.TASK_LENGTH
        elif draw and length == self.TASK_LENGTH:
            draw = False
            length = 0
            game.score += value       
        
        # if draw and owned: 
        #     self.task = pygame.draw.circle(self.game.screen, color, (30, y_coord), 22, 1)
        #     value_text_color = color
        # else:
        #     self.task = pygame.draw.circle(self.game.screen, color, (30, y_coord), 22)
        #     value_text_color = black
        #self.task = pygame.draw.circle(self.game.screen, color, (160, y_coord), 28)

        #   min(height, width) / 2


        value_text_color = black
        self.task = pygame.draw.rect(self.game.screen, color, [100, y_coord - 25, 95, 50], border_radius=25)
        pygame.draw.rect(self.game.screen, color, [200, y_coord - 25, self.TASK_LENGTH, 50])
        pygame.draw.rect(self.game.screen, black, [205, y_coord - 20, self.TASK_LENGTH - 10, 40])
        pygame.draw.rect(self.game.screen, color, [200, y_coord - 25, length, 50])
        
        value_text = self.game.font.render("{:.2f}".format(value), True, value_text_color)
        self.game.screen.blit(value_text, (130, y_coord - 6))

        return self.task, length, draw

    def draw_buttons(self, color, x_coord, cost, owned, manager_cost, speed_multiplier):
        """The method to draw the task's action buttons. 

        Args:
            color (Color): The RGB color of the button. 
            x_coord (int): The vertical position of the button. 
            cost (int): The amount to withdraw from the score for buying additional task activity. 
            owned (bool): The flag to test if the automation manager is owned. 
            manager_cost (int): The amount to withdraw from the score for buying a manager. 
            speed_multiplier (float): The amount to withdraw from the score for buying a speed multiplier.

        Returns:
            tuple: A tuple containing: the color_button, the manager_button, and the speed_button
        """
        color_button = pygame.draw.rect(self.game.screen, color, [x_coord, 475, 60, 40])
        color_cost = self.game.font.render(str(round(cost, 2)), True, black)
        self.game.screen.blit(color_cost, (x_coord + 10, 485))
        if not owned:
            manager_button = pygame.draw.rect(self.game.screen, color, [x_coord, 535, 60, 40])
            manager_text = self.game.font.render(str(round(manager_cost, 2)), True, black)
        else:
            manager_button = pygame.draw.rect(self.game.screen, color, [x_coord, 535, 60, 40], 1, 1)
            manager_text = self.game.font.render('', True, black)
        self.game.screen.blit(manager_text, (x_coord + 3, 545))
        speed_button = pygame.draw.rect(self.game.screen, color, [x_coord, 595, 60, 40])
        speed_text = self.game.font.render(f'{speed_multiplier/1000}K', True, black)
        self.game.screen.blit(speed_text, (x_coord + 2, 605))
        return color_button, manager_button, speed_button    
     
    def build_tasks(self, action):
        """The method to make and return a dictionary of 'stats. 
        """
        # now = pygame.time.get_ticks()
        # if now >= self.game.elapsed_time:
        #     self.game.elapsed_time = now

        record_time = self.game.elapsed_time
        record_score = self.game.score         
        
        c, a = action.split("_")
        if c == 'red':
            pass
        if c == 'orange':
            pass
        if c == 'yellow':
            pass
        if c == 'green':
            pass
        if c == 'blue':
            pass
        if c == 'gray':
            pass
        if c == 'violet':
            pass        

        return {'ticks': record_time, 'score': record_score, 'action': action}

    def on_event(self, event):
        """The method to manage pygame events upon each cycle. 

        Args:
            event (_type_): _description_
        """
        if event.type == pygame.QUIT:
            self.game.is_running = False
        if event.type == pygame.MOUSEBUTTONDOWN: 
            if self.task1.collidepoint(event.pos) and self.drawing_red == False:
                pygame.mixer.Sound.play(self.game.task_click_sound)
                #self.game.stats['task_red'] = True
                self.game.task_list.append(self.build_tasks('red_task'))
                self.game.clicked_red_task += 1
                self.drawing_red = True
            if self.task2.collidepoint(event.pos) and self.drawing_orange == False:
                pygame.mixer.Sound.play(self.game.task_click_sound)
                self.game.task_list.append(self.build_tasks('orange_task'))
                self.game.clicked_orange_task += 1
                self.drawing_orange = True
            if self.task3.collidepoint(event.pos) and self.drawing_yellow == False:
                pygame.mixer.Sound.play(self.game.task_click_sound)
                self.game.task_list.append(self.build_tasks('yellow_task'))
                self.game.clicked_yellow_task += 1
                self.drawing_yellow = True
            if self.task4.collidepoint(event.pos) and self.drawing_green == False:
                pygame.mixer.Sound.play(self.game.task_click_sound)
                self.game.task_list.append(self.build_tasks('green_task'))
                self.game.clicked_green_task += 1
                self.drawing_green = True
            if self.task5.collidepoint(event.pos) and self.drawing_blue == False:
                pygame.mixer.Sound.play(self.game.task_click_sound)
                self.game.task_list.append(self.build_tasks('blue_task'))
                self.game.clicked_blue_task += 1
                self.drawing_blue = True
            if self.task6.collidepoint(event.pos) and self.drawing_gray == False:
                pygame.mixer.Sound.play(self.game.task_click_sound)
                self.game.task_list.append(self.build_tasks('gray_task'))
                self.game.clicked_gray_task += 1
                self.drawing_gray = True
            if self.task7.collidepoint(event.pos) and self.drawing_violet == False:
                pygame.mixer.Sound.play(self.game.task_click_sound)
                self.game.task_list.append(self.build_tasks('violet_task'))
                self.game.clicked_violet_task += 1
                self.drawing_violet = True

            if self.red_buy_value.collidepoint(event.pos) and self.game.score >= self.red_value_cost:
                pygame.mixer.Sound.play(self.game.buy_click_sound)
                self.game.task_list.append(self.build_tasks('red_more'))
                self.game.clicked_more_red += 1
                self.red_value += 0.15
                self.game.total_spent += self.red_value_cost
                self.game.score -= self.red_value_cost                
                self.red_value_cost += 0.1
            if self.orange_buy_value.collidepoint(event.pos) and self.game.score >= self.orange_value_cost:
                pygame.mixer.Sound.play(self.game.buy_click_sound)
                self.game.task_list.append(self.build_tasks('orange_more'))
                self.game.clicked_more_orange += 1
                self.orange_value += 0.3
                self.game.total_spent += self.orange_value_cost
                self.game.score -= self.orange_value_cost                
                self.orange_value_cost += 0.2
            if self.yellow_buy_value.collidepoint(event.pos) and self.game.score >= self.yellow_value_cost:
                pygame.mixer.Sound.play(self.game.buy_click_sound)
                self.game.task_list.append(self.build_tasks('yellow_more'))
                self.game.clicked_more_yellow += 1
                self.yellow_value += 0.45
                self.game.total_spent += self.yellow_value_cost
                self.game.score -= self.yellow_value_cost                
                self.yellow_value_cost += 0.3
            if self.green_buy_value.collidepoint(event.pos) and self.game.score >= self.green_value_cost:
                pygame.mixer.Sound.play(self.game.buy_click_sound)
                self.game.task_list.append(self.build_tasks('green_more'))
                self.game.clicked_more_green += 1
                self.green_value += 0.60
                self.game.total_spent += self.green_value_cost
                self.game.score -= self.green_value_cost                
                self.green_value_cost += 0.4
            if self.blue_buy_value.collidepoint(event.pos) and self.game.score >= self.blue_value_cost:
                pygame.mixer.Sound.play(self.game.buy_click_sound)
                self.game.task_list.append(self.build_tasks('blue_more'))
                self.game.clicked_more_blue += 1
                self.blue_value += 0.75
                self.game.total_spent += self.blue_value_cost
                self.game.score -= self.blue_value_cost                
                self.blue_value_cost += 0.5            
            if self.gray_buy_value.collidepoint(event.pos) and self.game.score >= self.gray_value_cost:
                pygame.mixer.Sound.play(self.game.buy_click_sound)
                self.game.task_list.append(self.build_tasks('gray_more'))
                self.game.clicked_more_gray += 1
                self.gray_value += 0.90
                self.game.total_spent += self.gray_value_cost
                self.game.score -= self.gray_value_cost                
                self.gray_value_cost += 0.6            
            if self.violet_buy_value.collidepoint(event.pos) and self.game.score >= self.violet_value_cost:
                pygame.mixer.Sound.play(self.game.buy_click_sound)
                self.game.task_list.append(self.build_tasks('violet_more'))
                self.game.clicked_more_violet += 1
                self.violet_value += 1.05
                self.game.total_spent += self.violet_value_cost
                self.game.score -= self.violet_value_cost                
                self.violet_value_cost += 0.7

            if self.red_buy_manager.collidepoint(event.pos) and self.game.score >= self.red_manager_cost and not self.red_owned:
                pygame.mixer.Sound.play(self.game.buy_click_sound)
                self.game.task_list.append(self.build_tasks('red_manager'))
                self.red_owned = True
                self.game.clicked_red_manager += 1
                self.game.total_spent += self.red_manager_cost
                self.game.score -= self.red_manager_cost
            if self.orange_buy_manager.collidepoint(event.pos) and self.game.score >= self.orange_manager_cost and not self.orange_owned:
                pygame.mixer.Sound.play(self.game.buy_click_sound)
                self.game.task_list.append(self.build_tasks('orange_manager'))
                self.orange_owned = True
                self.game.clicked_orange_manager += 1
                self.game.total_spent += self.orange_manager_cost
                self.game.score -= self.orange_manager_cost
            if self.yellow_buy_manager.collidepoint(event.pos) and self.game.score >= self.yellow_manager_cost and not self.yellow_owned:
                pygame.mixer.Sound.play(self.game.buy_click_sound)
                self.game.task_list.append(self.build_tasks('yellow_manager'))
                self.yellow_owned = True
                self.game.clicked_yellow_manager += 1
                self.game.total_spent += self.yellow_manager_cost
                self.game.score -= self.yellow_manager_cost
            if self.green_buy_manager.collidepoint(event.pos) and self.game.score >= self.green_manager_cost and not self.green_owned:
                pygame.mixer.Sound.play(self.game.buy_click_sound)
                self.game.task_list.append(self.build_tasks('green_manager'))
                self.green_owned = True
                self.game.clicked_green_manager += 1
                self.game.total_spent += self.green_manager_cost
                self.game.score -= self.green_manager_cost
            if self.blue_buy_manager.collidepoint(event.pos) and self.game.score >= self.blue_manager_cost and not self.blue_owned:
                pygame.mixer.Sound.play(self.game.buy_click_sound)
                self.game.task_list.append(self.build_tasks('blue_manager'))
                self.blue_owned = True
                self.game.clicked_blue_manager += 1
                self.game.total_spent += self.blue_manager_cost
                self.game.score -= self.blue_manager_cost  
            if self.gray_buy_manager.collidepoint(event.pos) and self.game.score >= self.gray_manager_cost and not self.gray_owned:
                pygame.mixer.Sound.play(self.game.buy_click_sound)
                self.game.task_list.append(self.build_tasks('gray_manager'))
                self.gray_owned = True
                self.game.clicked_gray_manager += 1
                self.game.total_spent += self.gray_manager_cost
                self.game.score -= self.gray_manager_cost  
            if self.violet_buy_manager.collidepoint(event.pos) and self.game.score >= self.violet_manager_cost and not self.violet_owned:
                pygame.mixer.Sound.play(self.game.buy_click_sound)
                self.game.task_list.append(self.build_tasks('violet_manager'))
                self.violet_owned = True
                self.game.clicked_violet_manager += 1
                self.game.total_spent += self.violet_manager_cost
                self.game.score -= self.violet_manager_cost                
            
            if self.red_buy_multiplier.collidepoint(event.pos) and self.game.score >= self.red_multiplier_cost:
                pygame.mixer.Sound.play(self.game.buy_click_sound)
                self.game.task_list.append(self.build_tasks('red_multiply'))
                self.game.clicked_red_speed += 1
                self.red_speed += 1.1
                self.game.total_spent += self.red_multiplier_cost 
                self.game.score -= self.red_multiplier_cost    
                self.red_multiplier_cost += 100            
            if self.orange_buy_multiplier.collidepoint(event.pos) and self.game.score >= self.orange_multiplier_cost:
                pygame.mixer.Sound.play(self.game.buy_click_sound)
                self.game.task_list.append(self.build_tasks('orange_multiply'))
                self.game.clicked_orange_speed += 1
                self.orange_speed += 1.1
                self.game.total_spent += self.orange_multiplier_cost 
                self.game.score -= self.orange_multiplier_cost  
                self.orange_multiplier_cost += 200              
            if self.yellow_buy_multiplier.collidepoint(event.pos) and self.game.score >= self.yellow_multiplier_cost:
                pygame.mixer.Sound.play(self.game.buy_click_sound)
                self.game.task_list.append(self.build_tasks('yellow_multiply'))
                self.game.clicked_yellow_speed += 1
                self.yellow_speed += 1.1
                self.game.total_spent += self.yellow_multiplier_cost 
                self.game.score -= self.yellow_multiplier_cost     
                self.yellow_multiplier_cost += 300           
            if self.green_buy_multiplier.collidepoint(event.pos) and self.game.score >= self.green_multiplier_cost:
                pygame.mixer.Sound.play(self.game.buy_click_sound)
                self.game.task_list.append(self.build_tasks('green_multiply'))
                self.game.clicked_green_speed += 1
                self.green_speed += 1.1
                self.game.total_spent += self.green_multiplier_cost 
                self.game.score -= self.green_multiplier_cost        
                self.green_multiplier_cost += 400        
            if self.blue_buy_multiplier.collidepoint(event.pos) and self.game.score >= self.blue_multiplier_cost:
                pygame.mixer.Sound.play(self.game.buy_click_sound)
                self.game.task_list.append(self.build_tasks('blue_multiply'))
                self.game.clicked_blue_speed += 1
                self.blue_speed += 1.1
                self.game.total_spent += self.blue_multiplier_cost 
                self.game.score -= self.blue_multiplier_cost    
                self.blue_multiplier_cost += 500            
            if self.gray_buy_multiplier.collidepoint(event.pos) and self.game.score >= self.gray_multiplier_cost:
                pygame.mixer.Sound.play(self.game.buy_click_sound)
                self.game.task_list.append(self.build_tasks('gray_multiply'))
                self.game.clicked_gray_speed += 1
                self.gray_speed += 1.1
                self.game.total_spent += self.gray_multiplier_cost 
                self.game.score -= self.gray_multiplier_cost      
                self.gray_multiplier_cost += 600          
            if self.violet_buy_multiplier.collidepoint(event.pos) and self.game.score >= self.violet_multiplier_cost:
                pygame.mixer.Sound.play(self.game.buy_click_sound)
                self.game.task_list.append(self.build_tasks('violet_multiply'))
                self.game.clicked_violet_speed += 1
                self.violet_speed += 1.1
                self.game.total_spent += self.violet_multiplier_cost 
                self.game.score -= self.violet_multiplier_cost     
                self.violet_multiplier_cost += 700           
    
    def on_update(self):
        """The method to modify game objects.  """
        now = pygame.time.get_ticks()
        if now  >= self.game.elapsed_time:
            self.game.elapsed_time = now
            ms = int(self.game.elapsed_time)
            total_seconds = int(ms / 1000)
            minutes       = int(total_seconds / 60)
            seconds       = int(total_seconds - minutes * 60)
        self.game.clock_mins = "{}".format(minutes)
        self.game.clock_secs = "{:02}".format(seconds)

    def on_render(self):
        """The method to draw game objects to the screen. 

        """
        self.game.screen.blit(self.screen_action, (0, 0))

        self.task1, self.red_length,    self.drawing_red    = self.draw_task(color=red,      y_coord=60,     value=self.red_value,     draw=self.drawing_red,      owned=self.red_owned,      length=self.red_length,     speed=self.red_speed )
        self.task2, self.orange_length, self.drawing_orange = self.draw_task(color=orange,   y_coord=120,    value=self.orange_value,  draw=self.drawing_orange,   owned=self.orange_owned,   length=self.orange_length,  speed=self.orange_speed  )
        self.task3, self.yellow_length, self.drawing_yellow = self.draw_task(color=yellow,   y_coord=180,    value=self.yellow_value,  draw=self.drawing_yellow,   owned=self.yellow_owned,   length=self.yellow_length,  speed=self.yellow_speed  )
        self.task4, self.green_length,  self.drawing_green  = self.draw_task(color=green,    y_coord=240,    value=self.green_value,   draw=self.drawing_green,    owned=self.green_owned,    length=self.green_length,   speed=self.green_speed )
        self.task5, self.blue_length,   self.drawing_blue   = self.draw_task(color=blue,     y_coord=300,    value=self.blue_value,    draw=self.drawing_blue,     owned=self.blue_owned,     length=self.blue_length,    speed=self.blue_speed )
        self.task6, self.gray_length,   self.drawing_gray   = self.draw_task(color=gray,     y_coord=360,    value=self.gray_value,    draw=self.drawing_gray,     owned=self.gray_owned,     length=self.gray_length,    speed=self.gray_speed )
        self.task7, self.violet_length, self.drawing_violet = self.draw_task(color=violet,   y_coord=420,    value=self.violet_value,  draw=self.drawing_violet,   owned=self.violet_owned,   length=self.violet_length,  speed=self.violet_speed  )

             
        
        self.red_buy_value,    self.red_buy_manager,     self.red_buy_multiplier      = self.draw_buttons(red,     200,    self.red_value_cost,       self.red_owned,      self.red_manager_cost,       self.red_multiplier_cost   )
        self.orange_buy_value, self.orange_buy_manager,  self.orange_buy_multiplier   = self.draw_buttons(orange,  265,    self.orange_value_cost,    self.orange_owned,   self.orange_manager_cost,    self.orange_multiplier_cost)
        self.yellow_buy_value, self.yellow_buy_manager,  self.yellow_buy_multiplier   = self.draw_buttons(yellow,  330,    self.yellow_value_cost,    self.yellow_owned,   self.yellow_manager_cost,    self.yellow_multiplier_cost)
        self.green_buy_value,  self.green_buy_manager,   self.green_buy_multiplier    = self.draw_buttons(green,   395,    self.green_value_cost,     self.green_owned,    self.green_manager_cost,     self.green_multiplier_cost )
        self.blue_buy_value,   self.blue_buy_manager,    self.blue_buy_multiplier     = self.draw_buttons(blue,    460,    self.blue_value_cost,      self.blue_owned,     self.blue_manager_cost,      self.blue_multiplier_cost  )
        self.gray_buy_value,   self.gray_buy_manager,    self.gray_buy_multiplier     = self.draw_buttons(gray,    525,    self.gray_value_cost,      self.gray_owned,     self.gray_manager_cost,      self.gray_multiplier_cost  )    
        self.violet_buy_value, self.violet_buy_manager,  self.violet_buy_multiplier   = self.draw_buttons(violet,  590,    self.violet_value_cost,    self.violet_owned,   self.violet_manager_cost,    self.violet_multiplier_cost)

        display_score = self.game.font.render('Money: ${:,.2f}'.format(self.game.score), True, white, black)
        self.game.screen.blit(display_score, (10, 5))

        game_clock_text = self.game.font.render(f'Time: {self.game.clock_mins}:{self.game.clock_secs}', True, white)
        self.game.screen.blit(game_clock_text, (WIDTH - 105, 5))

        buy_more = self.game.font.render('Buy More Task Value:', True, white)
        self.game.screen.blit(buy_more, (200, 460))

        buy_managers = self.game.font.render('Buy Automation Managers:', True, white)
        self.game.screen.blit(buy_managers, (200, 520))

        buy_speed = self.game.font.render('Buy 10% Speed:', True, white)
        self.game.screen.blit(buy_speed, (200, 580))

        pygame.display.flip()  
    
    def run(self):
        """The method to control the action screen.  
        """
        if self.game.score >= 100000:
            self.game.task_list.append(self.build_tasks('game_over'))
            

            # determine if the elapsed time is eligible to save
            data = self.game.highscores
            if len(data) < 5:
                self.game.eligible_to_save = True
            elif len(data) > 0:
                for value in data.values():
                    if self.game.task_list[-1]['ticks'] - self.game.action_start_time < value['time']:
                        self.game.eligible_to_save = True                

            self.game.game_state = 'over'

            # reset variables
            self.red_value      = 1
            self.orange_value   = 2
            self.yellow_value   = 3
            self.green_value    = 4
            self.blue_value     = 5
            self.gray_value     = 6
            self.violet_value   = 7
            self.drawing_red    = False
            self.drawing_orange = False
            self.drawing_yellow = False
            self.drawing_green  = False
            self.drawing_blue   = False
            self.drawing_gray   = False
            self.drawing_violet = False
            self.red_length     = 0
            self.orange_length  = 0
            self.yellow_length  = 0
            self.green_length   = 0
            self.blue_length    = 0
            self.gray_length    = 0
            self.violet_length  = 0
            self.red_speed      = 7
            self.orange_speed   = 6
            self.yellow_speed   = 5
            self.green_speed    = 4
            self.blue_speed     = 3
            self.gray_speed     = 2
            self.violet_speed   = 1

            # draw buttons variables
            self.red_value_cost = 1   
            self.red_owned = False
            self.red_manager_cost = 100
            self.red_multiplier_cost = 500
            self.orange_value_cost = 2
            self.orange_owned = False
            self.orange_manager_cost = 500
            self.orange_multiplier_cost = 1800
            self.yellow_value_cost = 3
            self.yellow_owned = False
            self.yellow_manager_cost = 1800
            self.yellow_multiplier_cost = 4000
            self.green_value_cost = 4
            self.green_owned = False
            self.green_manager_cost = 4000
            self.green_multiplier_cost = 10000
            self.blue_value_cost = 5
            self.blue_owned = False
            self.blue_manager_cost = 10000
            self.blue_multiplier_cost = 25000
            self.gray_value_cost = 6
            self.gray_owned = False
            self.gray_manager_cost = 25000
            self.gray_multiplier_cost = 60000
            self.violet_value_cost = 7
            self.violet_owned = False
            self.violet_manager_cost = 60000
            self.violet_multiplier_cost = 120000
  
        if self.red_owned and not self.drawing_red:
            self.drawing_red = True        
        if self.orange_owned and not self.drawing_orange:
            self.drawing_orange = True
        if self.yellow_owned and not self.drawing_yellow:
            self.drawing_yellow = True        
        if self.green_owned and not self.drawing_green:
            self.drawing_green = True
        if self.blue_owned and not self.drawing_blue:
            self.drawing_blue = True
        if self.gray_owned and not self.drawing_gray:
            self.drawing_gray = True
        if self.violet_owned and not self.drawing_violet:
            self.drawing_violet = True

        for event in pygame.event.get():
            self.on_event(event)
        self.on_update()
        self.on_render()

class Leaderboard():
    """The leaderboard class handles writing highscores.json to the screen. 
    """
    def __init__(self, game):
        """The save class constructor

        Args:
            game (_type_): A reference to the game object. 
            
        """ 
        self.game = game
        self.screen_leaderboard = pygame.image.load('screen_leaderboard1.png').convert_alpha()
        self.hs = self.game.highscores # just to make it easier to type 
        self.continue_button = pygame.draw.rect(self.game.screen, gray, [(WIDTH // 2)-50, 550, 100, 40])
        self.exit_button = pygame.draw.rect(self.game.screen, gray, [(WIDTH // 2)-50, 610, 100, 40])
        self.stats_button_text = self.game.font.render("Stats", True, xxxblue)
        self.time = 0
        self.last_score = 0
        self.hs_0_stats_button = pygame.draw.rect(self.game.screen, gray,[(320, 298), (50, 30)])
        self.hs_1_stats_button = pygame.draw.rect(self.game.screen, gray,[(320, 352), (50, 30)])
        self.hs_2_stats_button = pygame.draw.rect(self.game.screen, gray,[(320, 407), (50, 30)])
        self.hs_3_stats_button = pygame.draw.rect(self.game.screen, gray,[(320, 461), (50, 30)])
        self.hs_4_stats_button = pygame.draw.rect(self.game.screen, gray,[(320, 514), (50, 30)])
        
    def tablecell(self, value, pos):
        """The method to draw a tablecell

        Args:
            value (str): The value to write in the cell. 
            pos (tuple): The x, y coordinates of the top left of the cell. 
        """
        cell_text = self.game.font.render(value, True, white)
        self.game.screen.blit(cell_text, (pos))
    
    def build_task_list(self, index):
        
        self.tasks = self.hs[index]['tasks']
        self.time = self.hs[index]['tasks'][-1]['ticks']

        stats_dict = {
            'ticks'   : [],
            'scores'  : [],
            'red' : {
                'tasks': [],
                'mores': [],
                'managers': [],
                'multiplys': []
            },
            'orange' : {
                'tasks': [],
                'mores': [],
                'managers': [],
                'multiplys': []
            },
            'yellow' : {
                'tasks': [],
                'mores': [],
                'managers': [],
                'multiplys': []
            },
            'green' : {
                'tasks': [],
                'mores': [],
                'managers': [],
                'multiplys': []
            },
            'blue' : {
                'tasks': [],
                'mores': [],
                'managers': [],
                'multiplys': []
            },
            'gray' : {
                'tasks': [],
                'mores': [],
                'managers': [],
                'multiplys': []
            },
            'violet' : {
                'tasks': [],
                'mores': [],
                'managers': [],
                'multiplys': []
            },   
        }

        kounter = 0
        last_score = 0
        list_ticks = []
        list_scores = []
        red_dict = {}
        red_tasks = []
        red_mores = []
        red_managers = []
        red_multiplys = []
        orange_dict = {}
        orange_tasks = []
        orange_mores = []
        orange_managers = []
        orange_multiplys = []
        yellow_dict = {}
        yellow_tasks = []
        yellow_mores = []
        yellow_managers = []
        yellow_multiplys = []
        green_dict = {}
        green_tasks = []
        green_mores = []
        green_managers = []
        green_multiplys = []
        blue_dict = {}
        blue_tasks = []
        blue_mores = []
        blue_managers = []
        blue_multiplys = []
        gray_dict = {}
        gray_tasks = []
        gray_mores = []
        gray_managers = []
        gray_multiplys = []
        violet_dict = {}
        violet_tasks = []
        violet_mores = []
        violet_managers = []
        violet_multiplys = []


        for tick in range(self.time + 1):

            if tick == self.tasks[kounter]['ticks']:

                if self.tasks[kounter]['score'] != last_score:
                    last_score = self.tasks[kounter]['score']

                if kounter < len(self.tasks)-1:
                    while self.tasks[kounter]['ticks'] == self.tasks[kounter + 1]['ticks']:
                        self.tasks.pop(kounter)
                    else:
                        # split the action into a color & an action
                        c, a = self.tasks[kounter]['action'].split('_')  
                        list_ticks.append(tick)
                        list_scores.append(last_score)
                        if c == 'red':
                            if a == 'task': 
                                red_tasks.append([tick, last_score])
                            if a == 'more':
                                red_mores.append([tick, last_score])
                            if a == 'manager':
                                red_managers.append([tick, last_score])
                            if a == 'multiply':
                                red_multiplys.append([tick, last_score])
                            red_dict['tasks'] = red_tasks
                            red_dict['mores'] = red_mores
                            red_dict['managers'] = red_managers
                            red_dict['multiplys'] = red_multiplys
                        
                        if c == 'orange':
                            if a == 'task': 
                                orange_tasks.append([tick, last_score])
                            if a == 'more':
                                orange_mores.append([tick, last_score])
                            if a == 'manager':
                                orange_managers.append([tick, last_score])
                            if a == 'multiply':
                                orange_multiplys.append([tick, last_score])
                            orange_dict['tasks'] = orange_tasks
                            orange_dict['mores'] = orange_mores
                            orange_dict['managers'] = orange_managers
                            orange_dict['multiplys'] = orange_multiplys
                        
                        if c == 'yellow':
                            if a == 'task': 
                                yellow_tasks.append([tick, last_score])
                            if a == 'more':
                                yellow_mores.append([tick, last_score])
                            if a == 'manager':
                                yellow_managers.append([tick, last_score])
                            if a == 'multiply':
                                yellow_multiplys.append([tick, last_score])

                            yellow_dict['tasks'] = yellow_tasks
                            yellow_dict['mores'] = yellow_mores
                            yellow_dict['managers'] = yellow_managers
                            yellow_dict['multiplys'] = yellow_multiplys

                        if c == 'green':
                            if a == 'task': 
                                green_tasks.append([tick, last_score])
                            if a == 'more':
                                green_mores.append([tick, last_score])
                            if a == 'manager':
                                green_managers.append([tick, last_score])
                            if a == 'multiply':
                                green_multiplys.append([tick, last_score])

                            green_dict['tasks'] = green_tasks
                            green_dict['mores'] = green_mores
                            green_dict['managers'] = green_managers
                            green_dict['multiplys'] = green_multiplys
    
                        if c == 'blue':
                            if a == 'task': 
                                blue_tasks.append([tick, last_score])
                            if a == 'more':
                                blue_mores.append([tick, last_score])
                            if a == 'manager':
                                blue_managers.append([tick, last_score])
                            if a == 'multiply':
                                blue_multiplys.append([tick, last_score])

                            blue_dict['tasks'] = blue_tasks
                            blue_dict['mores'] = blue_mores
                            blue_dict['managers'] = blue_managers
                            blue_dict['multiplys'] = blue_multiplys

                        if c == 'gray':
                            if a == 'task': 
                                gray_tasks.append([tick, last_score])
                            if a == 'more':
                                gray_mores.append([tick, last_score])
                            if a == 'manager':
                                gray_managers.append([tick, last_score])
                            if a == 'multiply':
                                gray_multiplys.append([tick, last_score])

                            gray_dict['tasks'] = gray_tasks
                            gray_dict['mores'] = gray_mores
                            gray_dict['managers'] = gray_managers
                            gray_dict['multiplys'] = gray_multiplys

                        if c == 'violet':
                            if a == 'task': 
                                violet_tasks.append([tick, last_score])
                            if a == 'more':
                                violet_mores.append([tick, last_score])
                            if a == 'manager':
                                violet_managers.append([tick, last_score])
                            if a == 'multiply':
                                violet_multiplys.append([tick, last_score])

                            violet_dict['tasks'] = violet_tasks
                            violet_dict['mores'] = violet_mores
                            violet_dict['managers'] = violet_managers
                            violet_dict['multiplys'] = violet_multiplys

                        kounter += 1
                else:
                    list_ticks.append(tick)
                    list_scores.append(last_score)
               
                    kounter += 1
            else:    
                list_ticks.append(tick)
                list_scores.append(last_score)
    
            
            stats_dict['ticks'] = list_ticks
            stats_dict['scores'] = list_scores
            stats_dict['red'] = red_dict
            stats_dict['orange'] = orange_dict
            stats_dict['yellow'] = yellow_dict
            stats_dict['green'] = green_dict
            stats_dict['blue'] = blue_dict
            stats_dict['gray'] = gray_dict
            stats_dict['violet'] = violet_dict
            

        self.game.game_state = 'stats'
        self.game.statistics = Statistics(self.game, stats_dict)

    def on_event(self, event):
        """The method to manage pygame events upon each cycle. 

        Args:
            event (_type_): _description_
        """
        if event.type == pygame.QUIT:
            self.game.is_running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.hs_0_stats_button.collidepoint(event.pos):
                self.build_task_list(0)
            if self.hs_1_stats_button.collidepoint(event.pos):
                self.build_task_list(1)
            if self.hs_2_stats_button.collidepoint(event.pos):
                self.build_task_list(2)
            if self.hs_3_stats_button.collidepoint(event.pos):
                self.build_task_list(3)
            if self.hs_4_stats_button.collidepoint(event.pos):
                self.build_task_list(4)
                    
            if self.continue_button.collidepoint(event.pos):
                # reset game variables

                self.game.action_starting = True
                self.game.eligible_to_save = False
                self.game.player_name = ''
                self.game.score =  0
                self.game.total_spent = 0
                self.game.clock_secs = 0
                self.game.clock_mins = 0
                self.game.clicked_red_task = 0
                self.game.clicked_orange_task    = 0
                self.game.clicked_yellow_task    = 0
                self.game.clicked_green_task     = 0
                self.game.clicked_blue_task      = 0
                self.game.clicked_gray_task      = 0
                self.game.clicked_violet_task    = 0
                self.game.clicked_more_red     = 0
                self.game.clicked_more_orange  = 0
                self.game.clicked_more_yellow  = 0
                self.game.clicked_more_green   = 0
                self.game.clicked_more_blue   = 0
                self.game.clicked_more_gray    = 0
                self.game.clicked_more_violet  = 0
                self.game.clicked_red_manager = 0
                self.game.clicked_orange_manager = 0
                self.game.clicked_yellow_manager = 0
                self.game.clicked_green_manager = 0
                self.game.clicked_blue_manager = 0
                self.game.clicked_gray_manager = 0
                self.game.clicked_violet_manager = 0
                self.game.clicked_red_speed = 0
                self.game.clicked_orange_speed = 0
                self.game.clicked_yellow_speed = 0
                self.game.clicked_green_speed = 0
                self.game.clicked_blue_speed = 0
                self.game.clicked_gray_speed = 0
                self.game.clicked_violet_speed = 0

                self.game.game_state = 'action'
            
            if self.exit_button.collidepoint(event.pos):
                self.game.is_running = False
         
    def on_update(self):
        """The method to modify game objects.  """
        pass

    def calculate_mins_secs(self, milliseconds):
        """The method to convert milliseconds to 00:00 format. 
        """
        ms = int(milliseconds)
        total_seconds = int(ms / 1000)
        minutes       = int(total_seconds / 60)
        seconds       = int(total_seconds - minutes * 60)
        return "{}:{:02}".format(minutes, seconds)

    def on_render(self):
        """The method to draw game objects to the screen. 
        """    
        self.game.screen.blit(self.screen_leaderboard, (0, 0))
        if self.hs:
            self.hs_0_name   = self.tablecell(self.hs[0]['player'],                          ( 18, 330))
            self.hs_0_date   = self.tablecell(self.hs[0]['date'],                            (210, 330))
            self.hs_0_spent  = self.tablecell("${:,.2f}".format(float(self.hs[0]['spent'])), (395, 330))
            self.hs_0_time   = self.tablecell(self.calculate_mins_secs(self.hs[0]['time']),  (590, 330))
            self.hs_0_stats_button = pygame.draw.rect(self.game.screen, gray,               [(685, 325), (50, 25)])
            self.game.screen.blit(self.stats_button_text,                                    (689, 330))

        if len(self.hs) > 1:
            self.hs_1_name   = self.tablecell(self.hs[1]['player'],                          ( 18, 370))
            self.hs_1_date   = self.tablecell(self.hs[1]['date'],                            (210, 370))
            self.hs_1_spent  = self.tablecell("${:,.2f}".format(float(self.hs[1]['spent'])), (395, 370))
            self.hs_1_time   = self.tablecell(self.calculate_mins_secs(self.hs[1]['time']),  (590, 370))
            self.hs_1_stats_button = pygame.draw.rect(self.game.screen, gray,               [(685, 365), (50, 25)])
            self.game.screen.blit(self.stats_button_text,                                    (689, 370))
        
        if len(self.hs) > 2:
            self.hs_2_name   = self.tablecell(self.hs[2]['player'],                          ( 18, 420))
            self.hs_2_date   = self.tablecell(self.hs[2]['date'],                            (210, 420))
            self.hs_2_spent  = self.tablecell("${:,.2f}".format(float(self.hs[2]['spent'])), (395, 420))
            self.hs_2_time   = self.tablecell(self.calculate_mins_secs(self.hs[2]['time']),  (590, 420))
            self.hs_2_stats_button = pygame.draw.rect(self.game.screen, gray,               [(685, 415), (50, 25)])
            self.game.screen.blit(self.stats_button_text,                                    (689, 420))

        if len(self.hs) > 3:
            self.hs_3_name   = self.tablecell(self.hs[3]['player'],                          ( 18, 470))
            self.hs_3_date   = self.tablecell(self.hs[3]['date'],                            (210, 470))
            self.hs_3_spent  = self.tablecell("${:,.2f}".format(float(self.hs[3]['spent'])), (395, 470))
            self.hs_3_time   = self.tablecell(self.calculate_mins_secs(self.hs[3]['time']),  (590, 470))
            self.hs_3_stats_button = pygame.draw.rect(self.game.screen, gray,               [(685, 465), (50, 25)])
            self.game.screen.blit(self.stats_button_text,                                    (689, 470))

        if len(self.hs) > 4:
            self.hs_4_name   = self.tablecell(self.hs[4]['player'],                          ( 18, 520))
            self.hs_4_date   = self.tablecell(self.hs[4]['date'],                            (210, 520))
            self.hs_4_spent  = self.tablecell("${:,.2f}".format(float(self.hs[4]['spent'])), (395, 520))
            self.hs_4_time   = self.tablecell(self.calculate_mins_secs(self.hs[4]['time']),  (590, 520))
            self.hs_4_stats_button = pygame.draw.rect(self.game.screen, gray,               [(685, 515), (50, 25)])
            self.game.screen.blit(self.stats_button_text,                                    (689, 520))
        
        self.continue_button = pygame.draw.rect(self.game.screen, gray, [int(WIDTH * 0.25)-50, 565, 100, 35])
        self.continue_text = self.game.font.render("Play?", True, black)
        self.game.screen.blit(self.continue_text, (int(WIDTH * 0.25) - 30, 574))
        self.exit_button = pygame.draw.rect(self.game.screen, gray, [int(WIDTH * 0.75)-50, 565, 100, 35])
        self.exit_text = self.game.font.render("Exit", True, red)
        self.game.screen.blit(self.exit_text, (int(WIDTH * 0.75) - 16, 574))

        
        pygame.display.flip()

    def run(self):
        """The method to control the leaderboard screen.  
        """
        for event in pygame.event.get():
            self.on_event(event)
        self.on_update()
        self.on_render()

class Save():
    """The Save class handles gathering the player name for and writing to 
    highscores.csv. 
    """
    def __init__(self, game):
        """The save class constructor

        Args:
            game (_type_): A reference to the game object. 
        """ 
        self.game = game
        self.screen_save = pygame.image.load('screen_save1.png').convert_alpha()
        self.continue_button = pygame.draw.rect(self.game.screen, gray, [(WIDTH // 2)-50, 380, 100, 40])
        self.player_name = ''
        self.typing = False
    
    def on_event(self, event):
        """The method to manage pygame events upon each cycle. 

        Args:
            event (_type_): _description_
        """
        if event.type == pygame.QUIT:
            self.game.is_running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.continue_button.collidepoint(event.pos):
                # write the data to the file. 
                date = datetime.datetime.now().strftime("%m/%d/%y %I:%M %p")
                milliseconds = self.game.task_list[-1]['ticks'] - self.game.action_start_time
                next_rec = len(self.game.highscores)
                self.game.highscores[str(next_rec)] = {'date': date, 'player': self.player_name, 'spent': self.game.total_spent, 'time': milliseconds, 'tasks': self.game.task_list}

                sorted_data = dict(sorted(self.game.highscores.items(), key=lambda x : [x[1]['time'], x[1]['spent']]))
                sorted_data = {index: value for index, value in enumerate(sorted_data.values())}
                if len(sorted_data) > 5:
                    del sorted_data[5]

                with open('highscores.json','w') as file:
                    file.write(json.dumps(sorted_data))
                        
                self.game.highscores = sorted_data
                self.player_name = ''
                self.game.eligible_to_save = False
                self.game.leaderboard = Leaderboard(self.game)
                self.game.game_state = 'leaderboard'
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.entry_rect.collidepoint(event.pos):
                    if self.typing:
                        self.typing = False
                    elif not self.typing:
                        self.typing = True

        if event.type == pygame.TEXTINPUT and self.typing:
            self.player_name += event.text 
            if len(self.player_name) > 12:
                pygame.mixer.Sound.play(self.game.buy_click_sound)
                self.player_name = self.player_name[:-1]

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE and len(self.player_name) > 0 and self.typing:                
                self.player_name = self.player_name[:-1]       

    def on_update(self):
        """The method to modify game objects.  """
        pass 
    def on_render(self):
        """The method to draw game objects to the screen. 
        """    
        self.game.screen.blit(self.screen_save, (0, 0))
        outome_text = self.game.font.render('WINNER!', True, gold)
        self.game.screen.blit(outome_text, (165, 217))
        # game_clock_text = self.game.font.render('{:02d}:{:02d}'.format(self.game.clock_mins, self.game.clock_secs), True, white)
        # self.game.screen.blit(game_clock_text, (280, 248))
        # total_score = self.game.font.render('${:,.2f}'.format(self.game.score), True, white)
        # self.game.screen.blit(total_score, (112, 278))
        # total_spent_text = self.game.font.render('${:,.2f}'.format(self.game.total_spent), True, white)
        # self.game.screen.blit(total_spent_text, (298, 278))
        if self.typing:
            pygame.draw.rect(self.game.screen, xxxgray, [(WIDTH // 2) - 63, 325, 130, 40], 0, 5)
        self.entry_rect = pygame.draw.rect(self.game.screen, gold, [(WIDTH // 2) - 63, 325, 130, 40], 5, 5)
        self.entry_text = self.game.font.render(f'{self.player_name}', True, white)
        self.game.screen.blit(self.entry_text, ((WIDTH // 2) - 55, 337))
        self.continue_button = pygame.draw.rect(self.game.screen, gray, [(WIDTH // 2)-50, 470, 100, 40])
        self.continue_text = self.game.font.render("Continue", True, black)
        self.game.screen.blit(self.continue_text, ((WIDTH // 2)-38, 482))
        pygame.display.flip()

    def run(self):
        """The method to control the leaderboard screen.  
        """
        for event in pygame.event.get():
            self.on_event(event)
        self.on_update()
        self.on_render()

class Over():
    """The game over screen. 
    """
    def __init__(self, game):
        """The Splash screen constructor

        Args:
            game (_type_): A reference to the game object. 
        """
        self.game = game
        self.screen_over = pygame.image.load('screen_over1.png')
        self.img_manager_owned = pygame.image.load('img_manager_owned.png')
        self.continue_button = pygame.draw.rect(self.game.screen, gray, [int(WIDTH * 0.25)-50, 550, 100, 40])
        self.stats_button    = pygame.draw.rect(self.game.screen, gray, [int(WIDTH * 0.75)-50, 610, 100, 40])
    
    def build_task_list(self):
        self.tasks = self.game.task_list
        self.time = self.tasks[-1]['ticks']

        stats_dict = {
            'ticks'   : [],
            'scores'  : [],
            'actions' : []
        }

        kounter = 0
        last_score = 0
        
        for tick in range(self.time + 1):
            list_ticks = []
            list_scores = []
            list_actions = []
            if tick == self.tasks[kounter]['ticks']:

                if self.tasks[kounter]['score'] != last_score:
                    last_score = self.tasks[kounter]['score']

                if kounter < len(self.tasks)-1:
                    while self.tasks[kounter]['ticks'] == self.tasks[kounter + 1]['ticks']:
                        self.tasks.pop(kounter)
                    else:
                        list_ticks.append(tick)
                        list_scores.append(last_score)
                        list_actions.append(self.tasks[kounter]['action'])
                        kounter += 1
                else:
                    list_ticks.append(tick)
                    list_scores.append(last_score)
                    list_actions.append(self.tasks[kounter]['action'])                 
                    kounter += 1
            else:    
                list_ticks.append(tick)
                list_scores.append(last_score)
                list_actions.append("")     
            
            stats_dict['ticks'] += list_ticks
            stats_dict['scores'] += list_scores
            stats_dict['actions'] += list_actions

        return stats_dict    

    def on_event(self, event):
        """The method to manage pygame events upon each cycle. 

        Args:
            event (_type_): _description_
        """
        if event.type == pygame.QUIT:
            self.game.is_running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.stats_button.collidepoint(event.pos):
                self.game.game_state = 'stats'
                current_tasks = self.build_task_list()
                self.game.statistics = Statistics(self.game, current_tasks)
            if self.continue_button.collidepoint(event.pos):
                if self.game.eligible_to_save:
                    self.game.game_state = 'save'
                else:
                    self.game.game_state = 'leaderboard'
                    
    def on_update(self):
        """The method to modify game objects.  """
        pass     
    def on_render(self):
        """The method to draw game objects to the screen. 
        """
        self.game.screen.blit(self.screen_over, (0, 0))
        if self.game.eligible_to_save:
            outome_text = self.game.font.render('WINNER!', True, (255, 215, 0))
            self.game.screen.blit(outome_text, (WIDTH//2, 225))
        else:
            outcome_text = self.game.font.render('Game Over', True, white)
            self.game.screen.blit(outcome_text, (WIDTH//2, 225))
        game_clock_text = self.game.font.render(f'{self.game.clock_mins}:{self.game.clock_secs}', True, white)
        self.game.screen.blit(game_clock_text, (475, 265))
        total_score = self.game.font.render('${:,.2f}'.format(self.game.score), True, white)
        self.game.screen.blit(total_score, (250, 300))        
        total_spent_text = self.game.font.render('${:,.2f}'.format(self.game.total_spent), True, white)
        self.game.screen.blit(total_spent_text, (490, 300))
        # tasks
        self.game.draw_text((165,  423), f'{self.game.clicked_red_task}', white )
        self.game.draw_text((260,  423), f'{self.game.clicked_orange_task}', white )
        self.game.draw_text((330,  423), f'{self.game.clicked_yellow_task}', white )
        self.game.draw_text((410,  423), f'{self.game.clicked_green_task}', white )
        self.game.draw_text((485,  423), f'{self.game.clicked_blue_task}', white )
        self.game.draw_text((575,  423), f'{self.game.clicked_gray_task}', white )
        self.game.draw_text((650,  423), f'{self.game.clicked_violet_task}', white )
        # more
        self.game.draw_text((165,  460), f'{self.game.clicked_more_red}', white )
        self.game.draw_text((260,  460), f'{self.game.clicked_more_orange}', white )
        self.game.draw_text((330,  460), f'{self.game.clicked_more_yellow}', white )
        self.game.draw_text((410,  460), f'{self.game.clicked_more_green}', white )
        self.game.draw_text((485,  460), f'{self.game.clicked_more_blue}', white )
        self.game.draw_text((575,  460), f'{self.game.clicked_more_gray}', white )
        self.game.draw_text((650,  460), f'{self.game.clicked_more_violet}', white )
        # speed
        self.game.draw_text((165,  540), f'{self.game.clicked_red_speed}', white )
        self.game.draw_text((260,  540), f'{self.game.clicked_orange_speed}', white )
        self.game.draw_text((330,  540), f'{self.game.clicked_yellow_speed}', white )
        self.game.draw_text((410,  540), f'{self.game.clicked_green_speed}', white )
        self.game.draw_text((485,  540), f'{self.game.clicked_blue_speed}', white )
        self.game.draw_text((575,  540), f'{self.game.clicked_gray_speed}', white )
        self.game.draw_text((650,  540), f'{self.game.clicked_violet_speed}', white )
        
        # manager
        if self.game.clicked_red_manager == 1:
            self.game.screen.blit(self.img_manager_owned, (165, 492))
        if self.game.clicked_orange_manager == 1:
            self.game.screen.blit(self.img_manager_owned, (260, 492))            
        if self.game.clicked_yellow_manager == 1:
            self.game.screen.blit(self.img_manager_owned, (330, 492))            
        if self.game.clicked_green_manager == 1:
            self.game.screen.blit(self.img_manager_owned, (410, 492))            
        if self.game.clicked_blue_manager == 1:
            self.game.screen.blit(self.img_manager_owned, (485, 492))            
        if self.game.clicked_gray_manager == 1:
            self.game.screen.blit(self.img_manager_owned, (575, 492))            
        if self.game.clicked_violet_manager == 1:
            self.game.screen.blit(self.img_manager_owned, (650, 492))            
        
        self.continue_button = pygame.draw.rect(self.game.screen, gray, [int(WIDTH * 0.25)-50, 600, 100, 40])
        self.continue_text = self.game.font.render("Continue", True, black)
        self.game.screen.blit(self.continue_text, (int(WIDTH * 0.25) - 38, 612))
        self.stats_button = pygame.draw.rect(self.game.screen, gray, [int(WIDTH * 0.75)-43, 600, 100, 40])
        self.stats_text = self.game.font.render("Stats", True, xxxblue)
        self.game.screen.blit(self.stats_text, (int(WIDTH * 0.75) - 16, 612))
        pygame.display.flip()

    def run(self):
        """The method to control the game over screen.  
        """
        for event in pygame.event.get():
            self.on_event(event)
        self.on_update()
        self.on_render()

class Statistics():
    """The stats screen for One Hundred Thousandaire
    """
    def __init__(self, game, stats):
        """The stats screen constructor

        Args:
            game (_type_): A reference to the game object. 
            stats (List): A dictionary of stats to graph [game.task_list]. 
        """
        self.game = game
        self.stats = stats
        self.screen_stats = pygame.image.load('screen_action1.png').convert_alpha()
   
    
    def on_event(self, event):
        """The method to manage pygame events upon each cycle. 

        Args:
            event (_type_): _description_
        """
        if event.type == pygame.QUIT:
            self.game.is_running = False
        if event.type == pygame.MOUSEBUTTONDOWN:


            if self.continue_button.collidepoint(event.pos):
                matplotlib.pyplot.close()
                if self.game.action_starting:   
                    self.game.game_state = 'splash'
                else:         
                    if self.game.eligible_to_save:
                        self.game.game_state = 'save'  
                    else:
                        self.game.leaderboard = Leaderboard(self.game)
                        self.game.game_state = 'leaderboard'
    def on_update(self):
        """The method to modify game objects.  """
        pass 
    
    def clock_converter(self, x):
        """The two arguments are the value and tick position"""
        mins = ""
        secs = ""
        if x % 60000 == 0:

            total_seconds = int(x / 1000)
            minutes       = int(total_seconds / 60)
            seconds       = int(total_seconds - minutes * 60)
            mins = "{}".format(minutes)
            secs = "{:02}".format(seconds)

        s = f"{mins}:{secs}"
        return s
    
    def on_render(self):
        """The method to draw game objects to the screen. 
        """
        self.game.screen.blit(self.screen_stats, (0, 0))
        
        plt.rcParams.update({'figure.autolayout': True})
        plt.rcParams['lines.markersize'] ** 4
        fig, ax = plt.subplots()
        fig.set_figwidth(7.6)
        fig.set_figheight(5.0)     

        plt.style.use('bmh')
        labels = ax.get_xticklabels()
        plt.setp(labels, rotation=45, horizontalalignment='right')
        ax.set(xlabel='Milliseconds', ylabel='Score', title='$ per Millisecond')

        ax.plot(self.stats['scores'], c='#0000ff')
       
        if len(self.stats['red']['managers']) > 0:
            red_managers = np.array(self.stats['red']['managers'][0])
            ax.scatter(red_managers[0], red_managers[1], marker='^', c='#ff0000', s=10**2)
        if len(self.stats['orange']['managers']) > 0:    
            orange_managers = np.array(self.stats['orange']['managers'][0])
            ax.scatter(orange_managers[0], orange_managers[1], marker='^', c='#ff7f00', s=10**2)
        if len(self.stats['yellow']['managers']) > 0:
            yellow_managers = np.array(self.stats['yellow']['managers'][0])
            ax.scatter(yellow_managers[0], yellow_managers[1], marker='^', c='#ffff00', s=10**2)
        if len(self.stats['green']['managers']) > 0:
            green_managers = np.array(self.stats['green']['managers'][0])
            ax.scatter(green_managers[0], green_managers[1], marker='^', c='#00ff00', s=10**2)
        if len(self.stats['blue']['managers']) > 0:
            blue_managers = np.array(self.stats['blue']['managers'][0])
            ax.scatter(blue_managers[0], blue_managers[1], marker='^', c='#1e90ff', s=10**2)
        if len(self.stats['gray']['managers']) > 0:
            gray_managers = np.array(self.stats['gray']['managers'][0])
            ax.scatter(gray_managers[0], gray_managers[1], marker='^', c='#d3d3d3', s=10**2)
        if len(self.stats['violet']['managers']) > 0:
            violet_managers = np.array(self.stats['violet']['managers'][0])
            ax.scatter(violet_managers[0], violet_managers[1], marker='^', c='#9400d3', s=10**2)

        canvas = agg.FigureCanvasAgg(fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb()
        size = canvas.get_width_height()
        surf = pygame.image.fromstring(raw_data, size, "RGB")
        self.game.screen.blit(surf, (0,0))
        plt.close()

        self.continue_button = pygame.draw.rect(self.game.screen, gray, [(WIDTH // 2)-50, 600, 100, 40])
        self.continue_text = self.game.font.render("Continue", True, black)
        self.game.screen.blit(self.continue_text, ((WIDTH // 2)-38, 612))
        pygame.display.flip()
    def run(self):
        """The method to control the splash screen.  
        """
        for event in pygame.event.get():
            self.on_event(event)
        self.on_update()
        self.on_render()
           
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
        game_icon = pygame.image.load('img_gold_pile.png')
        pygame.display.set_icon(game_icon)
        self.screen = pygame.display.set_mode((self.width, self.height))   
        pygame.display.set_caption("One Hundred Thousandaire")
        self.fps = 60
        self.game_clock = pygame.time.Clock()  
        self.font = pygame.font.SysFont('Segoe UI Bold', 24)
        self.background_sound = pygame.mixer.music.load('snd_background_loop.ogg')
        self.task_click_sound = pygame.mixer.Sound('snd_task_click.wav')
        self.buy_click_sound = pygame.mixer.Sound('snd_buy_click.ogg')
        self.is_running = True
        self.highscores = {}
        self.task_list = []

        with open('highscores.json') as file:
            try:
                data = json.load(file)
                if isinstance(data, dict):
                    self.highscores =  {int(k):v for k,v in data.items()}

            except Exception:
                # file is empty
                self.highscores = {}

        
        self.game_state = 'splash'
        self.action_starting = True
        self.eligible_to_save = False  

        self.score = 0    #      99900     #  99999    #      10000  #      
        self.total_spent = 0
        self.clock_secs = 0
        self.clock_mins = 0
        self.clicked_red_task = 0
        self.clicked_orange_task    = 0
        self.clicked_yellow_task    = 0
        self.clicked_green_task     = 0
        self.clicked_blue_task      = 0
        self.clicked_gray_task      = 0
        self.clicked_violet_task    = 0
        self.clicked_more_red     = 0
        self.clicked_more_orange  = 0
        self.clicked_more_yellow  = 0
        self.clicked_more_green   = 0
        self.clicked_more_blue   = 0
        self.clicked_more_gray    = 0
        self.clicked_more_violet  = 0
        self.clicked_red_manager = 0
        self.clicked_orange_manager = 0
        self.clicked_yellow_manager = 0
        self.clicked_green_manager = 0
        self.clicked_blue_manager = 0
        self.clicked_gray_manager = 0
        self.clicked_violet_manager = 0
        self.clicked_red_speed = 0
        self.clicked_orange_speed = 0
        self.clicked_yellow_speed = 0
        self.clicked_green_speed = 0
        self.clicked_blue_speed = 0
        self.clicked_gray_speed = 0
        self.clicked_violet_speed = 0

        
   
        self.splash = Splash(self)
        self.action = Action(self)
        self.save = Save(self)
        self.leaderboard = Leaderboard(self)
        self.over = Over(self)     
        self.statistics = Statistics(self, self.task_list)   

    def draw_text(self, coords=(0,0), text="None", color=(255,0,255)):
        textCanvas = self.font.render( str( text ), True, color )
        self.screen.blit( textCanvas, coords )

    def run(self):
        """The method to loop through the game states. 
        """
        pygame.mixer.music.play(loops=-1)
        
        while(self.is_running):
            if self.game_state == 'splash':
                self.splash.run()
            elif self.game_state == 'action':
                if self.action_starting:
                    self.action_starting = False
                    self.elapsed_time = pygame.time.get_ticks()
                    self.action_start_time = self.elapsed_time
                self.action.run()
            elif self.game_state == 'save':
                self.save.run()
            elif self.game_state == 'leaderboard':
                self.leaderboard.run()
            elif self.game_state == 'over':
                self.over.run()
            elif self.game_state == 'stats':
                self.statistics.run()

            self.game_clock.tick(FPS)
        
        pygame.quit()
        sys.exit(0)
        
if __name__ == "__main__":
    game = Game()
    game.run()

