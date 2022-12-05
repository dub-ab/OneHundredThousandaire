"""
One Hundred Thousandaire - An Idle Clicker
This application was inspired by:
    Create an Idle Clicker Adventure Capitalist Style Game in Python Using Pygame! Full Game In An HOUR!
    https://www.youtube.com/watch?v=qCA7FBwKOgI
"""
__author__      = "Anthony B. Washington"
__license__     = 'MIT'  # https://mit-license.org/

import csv
import datetime
import os
import sys
import time

import pygame
BUFFER = 200
MONITOR_WIDTH = 1920 - BUFFER
WIDTH = 415
HEIGHT = 620
FPS = 120

# colors
red     = (255, 000, 000)
orange  = (255, 127, 000)
yellow  = (255, 255, 000)
green   = (000, 255, 000)
xxxblue = (000, 000, 255)
blue    = ( 30, 144, 255)
violet  = (148, 000, 211)
gray    = (211, 211, 211)
black   = (  0,   0,   0)
white   = (255, 255, 255)



class Splash():
    """The introductory splash screen for One Hundred Thousandaire
    """
    def __init__(self, game):
        """The Splash screen constructor

        Args:
            game (_type_): A reference to the game object. 
        """
        self.game = game
        self.screen_splash = pygame.image.load('screen_splash.png').convert_alpha()
        self.continue_button = pygame.draw.rect(self.game.screen, gray, [(WIDTH // 2)-50, 380, 100, 40])
    def on_event(self, event):
        """The method to manage pygame events upon each cycle. 

        Args:
            event (_type_): _description_
        """
        if event.type == pygame.QUIT:
            self.game.is_running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.continue_button.collidepoint(event.pos):
                self.game.game_state = 'action'
    def on_update(self):
        """The method to modify game objects.  """
        pass 
    def on_render(self):
        """The method to draw game objects to the screen. 
        """
        self.game.screen.blit(self.screen_splash, (0, 0))

        self.continue_button = pygame.draw.rect(self.game.screen, gray, [(WIDTH // 2)-50, 470, 100, 40])
        self.continue_text = self.game.font.render("Continue", True, black)
        self.game.screen.blit(self.continue_text, ((WIDTH // 2)-38, 482))
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
        self.screen_action = pygame.image.load('screen_action.png').convert_alpha()
        self.TASK_LENGTH = 330
       
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
        self.task = pygame.draw.circle(self.game.screen, color, (30, y_coord), 22)
        value_text_color = black
        pygame.draw.rect(self.game.screen, color, [70, y_coord - 20, self.TASK_LENGTH, 40])
        pygame.draw.rect(self.game.screen, black, [75 , y_coord - 15, self.TASK_LENGTH - 10, 30])
        pygame.draw.rect(self.game.screen, color, [70, y_coord - 20, length, 40])
        
        value_text = self.game.font.render("{:.2f}".format(value), True, value_text_color)
        self.game.screen.blit(value_text, (10, y_coord - 6))

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
        color_button = pygame.draw.rect(self.game.screen, color, [x_coord, 455, 52, 30])
        color_cost = self.game.font.render(str(round(cost, 2)), True, black)
        self.game.screen.blit(color_cost, (x_coord + 9, 463))
        if not owned:
            manager_button = pygame.draw.rect(self.game.screen, color, [x_coord, 515, 52, 30])
            manager_text = self.game.font.render(str(round(manager_cost, 2)), True, black)
        else:
            manager_button = pygame.draw.rect(self.game.screen, color, [x_coord, 515, 52, 30], 1, 1)
            manager_text = self.game.font.render('', True, black)
        self.game.screen.blit(manager_text, (x_coord + 3, 520))
        speed_button = pygame.draw.rect(self.game.screen, color, [x_coord, 575, 52, 30])
        speed_text = self.game.font.render(f'{speed_multiplier/1000}K', True, black)
        self.game.screen.blit(speed_text, (x_coord + 2, 582))
        return color_button, manager_button, speed_button    
    
    def on_event(self, event):
        """The method to manage pygame events upon each cycle. 

        Args:
            event (_type_): _description_
        """
        if event.type == pygame.QUIT:
            self.game.is_running = False
        if event.type == pygame.MOUSEBUTTONDOWN: # and pygame.time.get_ticks() - self.last_mouse_click >= 1000:
            #self.last_mouse_click = pygame.time.get_ticks()
            if self.task1.collidepoint(event.pos) and self.drawing_red == False:
                pygame.mixer.Sound.play(self.game.task_click_sound)
                self.game.clicked_red_task += 1
                self.drawing_red = True
            if self.task2.collidepoint(event.pos) and self.drawing_orange == False:
                pygame.mixer.Sound.play(self.game.task_click_sound)
                self.game.clicked_orange_task += 1
                self.drawing_orange = True
            if self.task3.collidepoint(event.pos) and self.drawing_yellow == False:
                pygame.mixer.Sound.play(self.game.task_click_sound)
                self.game.clicked_yellow_task += 1
                self.drawing_yellow = True
            if self.task4.collidepoint(event.pos) and self.drawing_green == False:
                pygame.mixer.Sound.play(self.game.task_click_sound)
                self.game.clicked_green_task += 1
                self.drawing_green = True
            if self.task5.collidepoint(event.pos) and self.drawing_blue == False:
                pygame.mixer.Sound.play(self.game.task_click_sound)
                self.game.clicked_blue_task += 1
                self.drawing_blue = True
            if self.task6.collidepoint(event.pos) and self.drawing_gray == False:
                pygame.mixer.Sound.play(self.game.task_click_sound)
                self.game.clicked_gray_task += 1
                self.drawing_gray = True
            if self.task7.collidepoint(event.pos) and self.drawing_violet == False:
                pygame.mixer.Sound.play(self.game.task_click_sound)
                self.game.clicked_violet_task += 1
                self.drawing_violet = True

            if self.red_buy_value.collidepoint(event.pos) and self.game.score >= self.red_value_cost:
                pygame.mixer.Sound.play(self.game.buy_click_sound)
                self.game.clicked_more_red += 1
                self.red_value += 0.15
                self.game.total_spent += self.red_value_cost
                self.game.score -= self.red_value_cost                
                self.red_value_cost += 0.1
            if self.orange_buy_value.collidepoint(event.pos) and self.game.score >= self.orange_value_cost:
                pygame.mixer.Sound.play(self.game.buy_click_sound)
                self.game.clicked_more_orange += 1
                self.orange_value += 0.3
                self.game.total_spent += self.orange_value_cost
                self.game.score -= self.orange_value_cost                
                self.orange_value_cost += 0.2
            if self.yellow_buy_value.collidepoint(event.pos) and self.game.score >= self.yellow_value_cost:
                pygame.mixer.Sound.play(self.game.buy_click_sound)
                self.game.clicked_more_yellow += 1
                self.yellow_value += 0.45
                self.game.total_spent += self.yellow_value_cost
                self.game.score -= self.yellow_value_cost                
                self.yellow_value_cost += 0.3
            if self.green_buy_value.collidepoint(event.pos) and self.game.score >= self.green_value_cost:
                pygame.mixer.Sound.play(self.game.buy_click_sound)
                self.game.clicked_more_green += 1
                self.green_value += 0.60
                self.game.total_spent += self.green_value_cost
                self.game.score -= self.green_value_cost                
                self.green_value_cost += 0.4
            if self.blue_buy_value.collidepoint(event.pos) and self.game.score >= self.blue_value_cost:
                pygame.mixer.Sound.play(self.game.buy_click_sound)
                self.game.clicked_more_blue += 1
                self.blue_value += 0.75
                self.game.total_spent += self.blue_value_cost
                self.game.score -= self.blue_value_cost                
                self.blue_value_cost += 0.5            
            if self.gray_buy_value.collidepoint(event.pos) and self.game.score >= self.gray_value_cost:
                pygame.mixer.Sound.play(self.game.buy_click_sound)
                self.game.clicked_more_gray += 1
                self.gray_value += 0.90
                self.game.total_spent += self.gray_value_cost
                self.game.score -= self.gray_value_cost                
                self.gray_value_cost += 0.6            
            if self.violet_buy_value.collidepoint(event.pos) and self.game.score >= self.violet_value_cost:
                pygame.mixer.Sound.play(self.game.buy_click_sound)
                self.game.clicked_more_violet += 1
                self.violet_value += 1.05
                self.game.total_spent += self.violet_value_cost
                self.game.score -= self.violet_value_cost                
                self.violet_value_cost += 0.7

            if self.red_buy_manager.collidepoint(event.pos) and self.game.score >= self.red_manager_cost and not self.red_owned:
                pygame.mixer.Sound.play(self.game.buy_click_sound)
                self.red_owned = True
                self.game.clicked_red_manager += 1
                self.game.total_spent += self.red_manager_cost
                self.game.score -= self.red_manager_cost
            if self.orange_buy_manager.collidepoint(event.pos) and self.game.score >= self.orange_manager_cost and not self.orange_owned:
                pygame.mixer.Sound.play(self.game.buy_click_sound)
                self.orange_owned = True
                self.game.clicked_orange_manager += 1
                self.game.total_spent += self.orange_manager_cost
                self.game.score -= self.orange_manager_cost
            if self.yellow_buy_manager.collidepoint(event.pos) and self.game.score >= self.yellow_manager_cost and not self.yellow_owned:
                pygame.mixer.Sound.play(self.game.buy_click_sound)
                self.yellow_owned = True
                self.game.clicked_yellow_manager += 1
                self.game.total_spent += self.yellow_manager_cost
                self.game.score -= self.yellow_manager_cost
            if self.green_buy_manager.collidepoint(event.pos) and self.game.score >= self.green_manager_cost and not self.green_owned:
                pygame.mixer.Sound.play(self.game.buy_click_sound)
                self.green_owned = True
                self.game.clicked_green_manager += 1
                self.game.total_spent += self.green_manager_cost
                self.game.score -= self.green_manager_cost
            if self.blue_buy_manager.collidepoint(event.pos) and self.game.score >= self.blue_manager_cost and not self.blue_owned:
                pygame.mixer.Sound.play(self.game.buy_click_sound)
                self.blue_owned = True
                self.game.clicked_blue_manager += 1
                self.game.total_spent += self.blue_manager_cost
                self.game.score -= self.blue_manager_cost  
            if self.gray_buy_manager.collidepoint(event.pos) and self.game.score >= self.gray_manager_cost and not self.gray_owned:
                pygame.mixer.Sound.play(self.game.buy_click_sound)
                self.gray_owned = True
                self.game.clicked_gray_manager += 1
                self.game.total_spent += self.gray_manager_cost
                self.game.score -= self.gray_manager_cost  
            if self.violet_buy_manager.collidepoint(event.pos) and self.game.score >= self.violet_manager_cost and not self.violet_owned:
                pygame.mixer.Sound.play(self.game.buy_click_sound)
                self.violet_owned = True
                self.game.clicked_violet_manager += 1
                self.game.total_spent += self.violet_manager_cost
                self.game.score -= self.violet_manager_cost                
            
            if self.red_buy_multiplier.collidepoint(event.pos) and self.game.score >= self.red_multiplier_cost:
                pygame.mixer.Sound.play(self.game.buy_click_sound)
                self.game.clicked_red_speed += 1
                self.red_speed += 1.1
                self.game.total_spent += self.red_multiplier_cost 
                self.game.score -= self.red_multiplier_cost    
                self.red_multiplier_cost += 100            
            if self.orange_buy_multiplier.collidepoint(event.pos) and self.game.score >= self.orange_multiplier_cost:
                pygame.mixer.Sound.play(self.game.buy_click_sound)
                self.game.clicked_orange_speed += 1
                self.orange_speed += 1.1
                self.game.total_spent += self.orange_multiplier_cost 
                self.game.score -= self.orange_multiplier_cost  
                self.orange_multiplier_cost += 200              
            if self.yellow_buy_multiplier.collidepoint(event.pos) and self.game.score >= self.yellow_multiplier_cost:
                pygame.mixer.Sound.play(self.game.buy_click_sound)
                self.game.clicked_yellow_speed += 1
                self.yellow_speed += 1.1
                self.game.total_spent += self.yellow_multiplier_cost 
                self.game.score -= self.yellow_multiplier_cost     
                self.yellow_multiplier_cost += 300           
            if self.green_buy_multiplier.collidepoint(event.pos) and self.game.score >= self.green_multiplier_cost:
                pygame.mixer.Sound.play(self.game.buy_click_sound)
                self.game.clicked_green_speed += 1
                self.green_speed += 1.1
                self.game.total_spent += self.green_multiplier_cost 
                self.game.score -= self.green_multiplier_cost        
                self.green_multiplier_cost += 400        
            if self.blue_buy_multiplier.collidepoint(event.pos) and self.game.score >= self.blue_multiplier_cost:
                pygame.mixer.Sound.play(self.game.buy_click_sound)
                self.game.clicked_blue_speed += 1
                self.blue_speed += 1.1
                self.game.total_spent += self.blue_multiplier_cost 
                self.game.score -= self.blue_multiplier_cost    
                self.blue_multiplier_cost += 500            
            if self.gray_buy_multiplier.collidepoint(event.pos) and self.game.score >= self.gray_multiplier_cost:
                pygame.mixer.Sound.play(self.game.buy_click_sound)
                self.game.clicked_gray_speed += 1
                self.gray_speed += 1.1
                self.game.total_spent += self.gray_multiplier_cost 
                self.game.score -= self.gray_multiplier_cost      
                self.gray_multiplier_cost += 600          
            if self.violet_buy_multiplier.collidepoint(event.pos) and self.game.score >= self.violet_multiplier_cost:
                pygame.mixer.Sound.play(self.game.buy_click_sound)
                self.game.clicked_violet_speed += 1
                self.violet_speed += 1.1
                self.game.total_spent += self.violet_multiplier_cost 
                self.game.score -= self.violet_multiplier_cost     
                self.violet_multiplier_cost += 700           
    
    def on_update(self):
        """The method to modify game objects.  """

        now = pygame.time.get_ticks()
        if now - self.game.pygame_time > 1000 and self.game.clock_secs > 58:
            self.game.clock_secs = 0
            self.game.clock_mins += 1
            self.pygame_time = now
        elif now - self.game.pygame_time > 1000:
            self.game.clock_secs += 1
            self.game.pygame_time = now
        if self.game.clock_mins > 58:
            self.game.clock_min = 59            

    def on_render(self):
        """The method to draw game objects to the screen. 

        """
        self.game.screen.blit(self.screen_action, (0, 0))

        self.task1, self.red_length,    self.drawing_red    = self.draw_task(color=red,      y_coord=50,     value=self.red_value,     draw=self.drawing_red,      owned=self.red_owned,      length=self.red_length,     speed=self.red_speed )
        self.task2, self.orange_length, self.drawing_orange = self.draw_task(color=orange,   y_coord=110,    value=self.orange_value,  draw=self.drawing_orange,   owned=self.orange_owned,   length=self.orange_length,  speed=self.orange_speed  )
        self.task3, self.yellow_length, self.drawing_yellow = self.draw_task(color=yellow,   y_coord=170,    value=self.yellow_value,  draw=self.drawing_yellow,   owned=self.yellow_owned,   length=self.yellow_length,  speed=self.yellow_speed  )
        self.task4, self.green_length,  self.drawing_green  = self.draw_task(color=green,    y_coord=230,    value=self.green_value,   draw=self.drawing_green,    owned=self.green_owned,    length=self.green_length,   speed=self.green_speed )
        self.task5, self.blue_length,   self.drawing_blue   = self.draw_task(color=blue,     y_coord=290,    value=self.blue_value,    draw=self.drawing_blue,     owned=self.blue_owned,     length=self.blue_length,    speed=self.blue_speed )
        self.task6, self.gray_length,   self.drawing_gray   = self.draw_task(color=gray,     y_coord=350,    value=self.gray_value,    draw=self.drawing_gray,     owned=self.gray_owned,     length=self.gray_length,    speed=self.gray_speed )
        self.task7, self.violet_length, self.drawing_violet = self.draw_task(color=violet,   y_coord=410,    value=self.violet_value,  draw=self.drawing_violet,   owned=self.violet_owned,   length=self.violet_length,  speed=self.violet_speed  )

             
        
        self.red_buy_value,    self.red_buy_manager,     self.red_buy_multiplier      = self.draw_buttons(red,      10,    self.red_value_cost,       self.red_owned,      self.red_manager_cost,       self.red_multiplier_cost   )
        self.orange_buy_value, self.orange_buy_manager,  self.orange_buy_multiplier   = self.draw_buttons(orange,   66,    self.orange_value_cost,    self.orange_owned,   self.orange_manager_cost,    self.orange_multiplier_cost)
        self.yellow_buy_value, self.yellow_buy_manager,  self.yellow_buy_multiplier   = self.draw_buttons(yellow,  122,    self.yellow_value_cost,    self.yellow_owned,   self.yellow_manager_cost,    self.yellow_multiplier_cost)
        self.green_buy_value,  self.green_buy_manager,   self.green_buy_multiplier    = self.draw_buttons(green,   178,    self.green_value_cost,     self.green_owned,    self.green_manager_cost,     self.green_multiplier_cost )
        self.blue_buy_value,   self.blue_buy_manager,    self.blue_buy_multiplier     = self.draw_buttons(blue,    234,    self.blue_value_cost,      self.blue_owned,     self.blue_manager_cost,      self.blue_multiplier_cost  )
        self.gray_buy_value,   self.gray_buy_manager,    self.gray_buy_multiplier     = self.draw_buttons(gray,    290,    self.gray_value_cost,      self.gray_owned,     self.gray_manager_cost,      self.gray_multiplier_cost  )    
        self.violet_buy_value, self.violet_buy_manager,  self.violet_buy_multiplier   = self.draw_buttons(violet,  346,    self.violet_value_cost,    self.violet_owned,   self.violet_manager_cost,    self.violet_multiplier_cost)

        display_score = self.game.font.render('Money: ${:,.2f}'.format(self.game.score), True, white, black)
        self.game.screen.blit(display_score, (10, 5))

        game_clock_text = self.game.font.render('Time: {:02d}:{:02d}'.format(self.game.clock_mins, self.game.clock_secs), True, white)
        self.game.screen.blit(game_clock_text, (WIDTH - 105, 5))

        buy_more = self.game.font.render('Buy More Task Value:', True, white)
        self.game.screen.blit(buy_more, (10, 437))

        buy_managers = self.game.font.render('Buy Automation Managers:', True, white)
        self.game.screen.blit(buy_managers, (10, 500))

        buy_speed = self.game.font.render('Buy 10% Speed:', True, white)
        self.game.screen.blit(buy_speed, (10, 560))

        pygame.display.flip()  
    
    def run(self):
        """The method to control the action screen.  
        """
        if self.game.score >= 100000:
            self.game.action_end_time = pygame.time.get_ticks()
            # determine if the elapsed time is eligible to save
            data = list(self.game.highscores) # copy the game highscores
            for record in data:
                if self.game.action_end_time - self.game.action_start_time < int(record[2]):
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
    """The leaderboard class handles writing highscores.csv to the screen. 
    """
    def __init__(self, game):
        """The save class constructor

        Args:
            game (_type_): A reference to the game object. 
        """ 
        self.game = game
        self.screen_leaderboard = pygame.image.load('screen_leaderboard.png').convert_alpha()
        self.hs = self.game.highscores # just to make it easier to write
        self.continue_button = pygame.draw.rect(self.game.screen, gray, [(WIDTH // 2)-50, 550, 100, 40])
        self.exit_button = pygame.draw.rect(self.game.screen, gray, [(WIDTH // 2)-50, 610, 100, 40])
    
    def tablecell(self, value, pos):
        """The method to draw a tablecell

        Args:
            value (str): The value to write in the cell. 
            pos (tuple): The x, y coordinates of the top left of the cell. 
        """
        cell_text = self.game.font.render(value, True, white)
        self.game.screen.blit(cell_text, (pos))
    
    def on_event(self, event):
        """The method to manage pygame events upon each cycle. 

        Args:
            event (_type_): _description_
        """
        if event.type == pygame.QUIT:
            self.game.is_running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.continue_button.collidepoint(event.pos):
                # reset game variables

                self.game.action_starting = True
                self.game.eligible_to_save = False
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
        self.hs = self.game.highscores 

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
            self.hs_0_name   = self.tablecell(self.hs[0][0],                            ( 18, 290))
            self.hs_0_spent  = self.tablecell("${:,.2f}".format(float(self.hs[0][2])),  (180, 290))
            self.hs_0_time   = self.tablecell(self.calculate_mins_secs(self.hs[0][1]),  (345, 290))

            self.hs_1_name   = self.tablecell(self.hs[1][0],                            ( 18, 310))
            self.hs_1_spent  = self.tablecell("${:,.2f}".format(float(self.hs[1][2])),  (180, 310))
            self.hs_1_time   = self.tablecell(self.calculate_mins_secs(self.hs[1][1]),  (345, 310))

            self.hs_2_name   = self.tablecell(self.hs[2][0],                            ( 18, 330))
            self.hs_2_spent  = self.tablecell("${:,.2f}".format(float(self.hs[2][2])),  (180, 330))
            self.hs_2_time   = self.tablecell(self.calculate_mins_secs(self.hs[2][1]),  (345, 330))

            self.hs_3_name   = self.tablecell(self.hs[3][0],                            ( 18, 350))
            self.hs_3_spent  = self.tablecell("${:,.2f}".format(float(self.hs[3][2])),  (180, 350))
            self.hs_3_time   = self.tablecell(self.calculate_mins_secs(self.hs[3][1]),  (345, 350))

            self.hs_4_name   = self.tablecell(self.hs[4][0],                            ( 18, 370))
            self.hs_4_spent  = self.tablecell("${:,.2f}".format(float(self.hs[4][2])),  (180, 370))
            self.hs_4_time   = self.tablecell(self.calculate_mins_secs(self.hs[4][1]),  (345, 370))

        self.continue_button = pygame.draw.rect(self.game.screen, gray, [int(WIDTH * 0.25)-50, 550, 100, 40])
        self.continue_text = self.game.font.render("Continue", True, black)
        self.game.screen.blit(self.continue_text, (int(WIDTH * 0.25) - 38, 562))
        self.exit_button = pygame.draw.rect(self.game.screen, gray, [int(WIDTH * 0.75)-50, 550, 100, 40])
        self.exit_text = self.game.font.render("Exit", True, red)
        self.game.screen.blit(self.exit_text, (int(WIDTH * 0.75) - 16, 562))

        
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
        self.screen_save = pygame.image.load('screen_save.png').convert_alpha()
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
                data = list(self.game.highscores)
                milliseconds = self.game.action_end_time - self.game.action_start_time
                data.append([self.player_name, self.game.total_spent, str(milliseconds)])

                sorted_data = list(sorted(data, key=lambda x: [int(x[2]), float(x[1])]))
                top_5_scores = list(sorted_data[0:5])

                with open('highscores.csv','w', newline='', encoding='utf-8') as file:
                    wr = csv.writer(file)
                    wr.writerows(top_5_scores)
                        
                self.game.highscores = list(top_5_scores)
                self.game.game_state = 'leaderboard'
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.entry_rect.collidepoint(event.pos):
                    if self.typing:
                        self.typing = False
                    elif not self.typing:
                        self.typing = True

        if event.type == pygame.TEXTINPUT and self.typing:
            self.player_name += event.text 
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
        outome_text = self.game.font.render('WINNER!', True, (255, 215, 0))
        self.game.screen.blit(outome_text, (165, 217))
        # game_clock_text = self.game.font.render('{:02d}:{:02d}'.format(self.game.clock_mins, self.game.clock_secs), True, white)
        # self.game.screen.blit(game_clock_text, (280, 248))
        # total_score = self.game.font.render('${:,.2f}'.format(self.game.score), True, white)
        # self.game.screen.blit(total_score, (112, 278))
        # total_spent_text = self.game.font.render('${:,.2f}'.format(self.game.total_spent), True, white)
        # self.game.screen.blit(total_spent_text, (298, 278))
        if self.typing:
            pygame.draw.rect(self.game.screen, (50, 50, 50), [(WIDTH // 2) - 100, 325, 210, 40], 0, 5)
        self.entry_rect = pygame.draw.rect(self.game.screen, gray, [(WIDTH // 2) - 100, 325, 210, 40], 5, 5)
        self.entry_text = self.game.font.render(f'{self.player_name}', True, white)
        self.game.screen.blit(self.entry_text, ((WIDTH // 2) - 92, 337))
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
        self.screen_over = pygame.image.load('screen_over.png')
        self.img_manager_owned = pygame.image.load('img_manager_owned.png')
        self.continue_button = pygame.draw.rect(self.game.screen, gray, [(WIDTH // 2)-50, 550, 100, 40])
        # self.exit_button = pygame.draw.rect(self.game.screen, gray, [(WIDTH // 2)-50, 610, 100, 40])
    
    def on_event(self, event):
        """The method to manage pygame events upon each cycle. 

        Args:
            event (_type_): _description_
        """
        if event.type == pygame.QUIT:
            self.game.is_running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.continue_button.collidepoint(event.pos):
                # reset game variables
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
            if self.game.eligible_to_save:
                self.game.game_state = 'save'
            else:
                self.game.game_state = 'action'
            # if self.exit_button.collidepoint(event.pos):
            #     self.game.is_running = False
    
    def on_update(self):
        """The method to modify game objects.  """
        pass 
    def on_render(self):
        """The method to draw game objects to the screen. 
        """
        self.game.screen.blit(self.screen_over, (0, 0))
        if self.game.eligible_to_save:
            outome_text = self.game.font.render('WINNER!', True, (255, 215, 0))
            self.game.screen.blit(outome_text, (165, 217))
        else:
            outcome_text = self.game.font.render('Game Over', True, white)
            self.game.screen.blit(outcome_text, (155, 217))
        game_clock_text = self.game.font.render('{:02d}:{:02d}'.format(self.game.clock_mins, self.game.clock_secs), True, white)
        self.game.screen.blit(game_clock_text, (280, 248))
        total_score = self.game.font.render('${:,.2f}'.format(self.game.score), True, white)
        self.game.screen.blit(total_score, (109, 280))        
        total_spent_text = self.game.font.render('${:,.2f}'.format(self.game.total_spent), True, white)
        self.game.screen.blit(total_spent_text, (298, 280))
        # tasks
        self.game.draw_text(( 75,  403), f'{self.game.clicked_red_task}', white )
        self.game.draw_text((125,  403), f'{self.game.clicked_orange_task}', white )
        self.game.draw_text((175,  403), f'{self.game.clicked_yellow_task}', white )
        self.game.draw_text((225,  403), f'{self.game.clicked_green_task}', white )
        self.game.draw_text((272,  403), f'{self.game.clicked_blue_task}', white )
        self.game.draw_text((322,  403), f'{self.game.clicked_gray_task}', white )
        self.game.draw_text((377,  403), f'{self.game.clicked_violet_task}', white )
        # more
        self.game.draw_text(( 75,  435), f'{self.game.clicked_more_red}', white )
        self.game.draw_text((125,  435), f'{self.game.clicked_more_orange}', white )
        self.game.draw_text((175,  435), f'{self.game.clicked_more_yellow}', white )
        self.game.draw_text((225,  435), f'{self.game.clicked_more_green}', white )
        self.game.draw_text((272,  435), f'{self.game.clicked_more_blue}', white )
        self.game.draw_text((322,  435), f'{self.game.clicked_more_gray}', white )
        self.game.draw_text((377,  435), f'{self.game.clicked_more_violet}', white )
        # manager
        if self.game.clicked_red_manager == 1:
            self.game.screen.blit(self.img_manager_owned, ( 55, 462))
        if self.game.clicked_orange_manager == 1:
            self.game.screen.blit(self.img_manager_owned, (115, 462))            
        if self.game.clicked_yellow_manager == 1:
            self.game.screen.blit(self.img_manager_owned, (165, 462))            
        if self.game.clicked_green_manager == 1:
            self.game.screen.blit(self.img_manager_owned, (215, 462))            
        if self.game.clicked_blue_manager == 1:
            self.game.screen.blit(self.img_manager_owned, (265, 462))            
        if self.game.clicked_gray_manager == 1:
            self.game.screen.blit(self.img_manager_owned, (315, 462))            
        if self.game.clicked_violet_manager == 1:
            self.game.screen.blit(self.img_manager_owned, (365, 462))            
        
        # speed
        self.game.draw_text(( 75,  500), f'{self.game.clicked_red_speed}', white )
        self.game.draw_text((125,  500), f'{self.game.clicked_orange_speed}', white )
        self.game.draw_text((175,  500), f'{self.game.clicked_yellow_speed}', white )
        self.game.draw_text((225,  500), f'{self.game.clicked_green_speed}', white )
        self.game.draw_text((272,  500), f'{self.game.clicked_blue_speed}', white )
        self.game.draw_text((322,  500), f'{self.game.clicked_gray_speed}', white )
        self.game.draw_text((377,  500), f'{self.game.clicked_violet_speed}', white )
        
        self.continue_button = pygame.draw.rect(self.game.screen, gray, [(WIDTH // 2)-50, 550, 100, 40])
        self.continue_text = self.game.font.render("Continue", True, black)
        self.game.screen.blit(self.continue_text, ((WIDTH // 2) - 38, 562))
        # self.exit_button = pygame.draw.rect(self.game.screen, gray, [int(WIDTH * 0.75)-50, 550, 100, 40])
        # self.exit_text = self.game.font.render("Exit", True, red)
        # self.game.screen.blit(self.exit_text, (int(WIDTH * 0.75) - 16, 562))
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
        # region setup
        pygame.init()
        pygame.mixer.init()
        self.pygame_time = pygame.time.get_ticks()
        self.action_start_time = self.pygame_time
        self.action_end_time = self.pygame_time
        self.width, self.height = WIDTH, HEIGHT  
        # dev_pos_x = MONITOR_WIDTH - WIDTH 
        # dev_pos_y = 133 
        # os.environ['SDL_VIDEO_WINDOW_POS'] = '%i,%i' % (dev_pos_x,dev_pos_y)
        self.screen = pygame.display.set_mode((self.width, self.height))   
        pygame.display.set_caption("One Hundred Thousandaire")
        self.fps = 60
        self.game_clock = pygame.time.Clock()  
        self.font = pygame.font.SysFont('Segoe UI Bold', 24)
        self.background_sound = pygame.mixer.music.load('snd_background_loop.ogg')
        self.task_click_sound = pygame.mixer.Sound('snd_task_click.wav')
        self.buy_click_sound = pygame.mixer.Sound('snd_buy_click.ogg')
        self.is_running = True
        self.highscores = []
        with open('highscores.csv', 'r') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                self.highscores.append(row)
        
        self.game_state = 'splash'
        self.action_starting = True
        self.eligible_to_save = False        
        self.score = 0    #    99999    #      10000  #       80000     #  
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

    def draw_text(self, coords=(0,0), text="None", color=(255,0,255)):
        textCanvas = self.font.render( str( text ), True, color )
        self.screen.blit( textCanvas, coords )

    def run(self):
        """The method to loop through the game states. 
        """
        pygame.mixer.music.play(loops=-1)
        self.pygame_time = pygame.time.get_ticks()
        while(self.is_running):
            if self.game_state == 'splash':
                self.splash.run()
            elif self.game_state == 'action':
                if self.action_starting:
                    self.action_starting = False
                    self.action_start_time = pygame.time.get_ticks()
                self.action.run()
            elif self.game_state == 'save':
                self.save.run()
            elif self.game_state == 'leaderboard':
                self.leaderboard.run()
            elif self.game_state == 'over':
                self.over.run()

            self.game_clock.tick(FPS)
        
        pygame.quit()
        sys.exit(0)
        
if __name__ == "__main__":
    game = Game()
    game.run()

