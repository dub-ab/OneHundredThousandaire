"""
One Hundred Thousandaire - An Idle Clicker
This application was inspired by:
    Create an Idle Clicker Adventure Capitalist Style Game in Python Using Pygame! Full Game In An HOUR!
    https://www.youtube.com/watch?v=qCA7FBwKOgI
"""
__author__      = "Anthony B. Washington"
__license__     = 'MIT'  # https://mit-license.org/

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
blue    = (000, 000, 255)
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
        self.splash_screen = pygame.image.load('splash_screen.png').convert_alpha()
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
        self.game.screen.blit(self.splash_screen, (0, 0))

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
    """The class to handle all in gameaction. 

    Returns:
        _type_: _description_
    """
    def __init__(self, game):
        """The Action screen constructor

        Args:
            game (_type_): A reference to the game object. 
        """

        self.game = game          

        self.task_color = (0, 0, 0)
        self.task_length = 330
        self.x_coord = 0
        #self.y_coord = 0
        self.value = 0
        self.value_text = ''
        self.draw = False
        #self.length = 0
        self.speed = 0.0
        self.cost = 0
        self.owned = False
        self.manager_cost = 0
        self.speed_multiplier = 0.0
        
        # game variables
        self.background = black 
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
        self.red_cost = 1   
        self.red_owned = False
        self.red_manager_cost = 100
        self.red_multiplier_cost = 500
        self.orange_cost = 2
        self.orange_owned = False
        self.orange_manager_cost = 500
        self.orange_multiplier_cost = 1800
        self.yellow_cost = 3
        self.yellow_owned = False
        self.yellow_manager_cost = 1800
        self.yellow_multiplier_cost = 4000
        self.green_cost = 4
        self.green_owned = False
        self.green_manager_cost = 4000
        self.green_multiplier_cost = 10000
        self.blue_cost = 5
        self.blue_owned = False
        self.blue_manager_cost = 10000
        self.blue_multiplier_cost = 25000
        self.gray_cost = 6
        self.gray_owned = False
        self.gray_manager_cost = 25000
        self.gray_multiplier_cost = 60000
        self.violet_cost = 7
        self.violet_owned = False
        self.violet_manager_cost = 60000
        self.violet_multiplier_cost = 120000

    def draw_task(self, color, y_coord, value, draw, length, speed):
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
        if draw and length == self.task_length:
            draw = False
            length = 0
            self.game.score += value
        elif draw and self.task_length - length >= speed: # if the task button has been clicked and the task is not complete
            length += speed        
        elif draw and self.task_length - length < speed:
            length = self.task_length
        elif draw and length == self.task_length:
            draw = False
            length = 0
            game.score += self.value       
        self.task = pygame.draw.circle(self.game.screen, color, (30, y_coord), 22)
        pygame.draw.rect(self.game.screen, color, [70, y_coord - 20, self.task_length, 40])
        pygame.draw.rect(self.game.screen, black, [75 , y_coord - 15, self.task_length - 10, 30])
        pygame.draw.rect(self.game.screen, color, [70, y_coord - 20, length, 40])
        
        self.value_text = self.game.font.render("{:.2f}".format(value), True, black)
        self.game.screen.blit(self.value_text, (11, y_coord - 6))

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

            if self.red_manager_buy.collidepoint(event.pos) and self.game.score >= self.red_manager_cost and not self.red_owned:
                pygame.mixer.Sound.play(self.game.buy_click_sound)
                self.red_owned = True
                self.game.clicked_red_manager += 1
                self.game.score -= self.red_manager_cost
            if self.orange_manager_buy.collidepoint(event.pos) and self.game.score >= self.orange_manager_cost and not self.orange_owned:
                pygame.mixer.Sound.play(self.game.buy_click_sound)
                self.orange_owned = True
                self.game.clicked_orange_manager += 1
                self.game.score -= self.orange_manager_cost
            if self.yellow_manager_buy.collidepoint(event.pos) and self.game.score >= self.yellow_manager_cost and not self.yellow_owned:
                pygame.mixer.Sound.play(self.game.buy_click_sound)
                self.yellow_owned = True
                self.game.clicked_yellow_manager += 1
                self.game.score -= self.yellow_manager_cost
            if self.green_manager_buy.collidepoint(event.pos) and self.game.score >= self.green_manager_cost and not self.green_owned:
                pygame.mixer.Sound.play(self.game.buy_click_sound)
                self.green_owned = True
                self.game.clicked_green_manager += 1
                self.game.score -= self.green_manager_cost
            if self.blue_manager_buy.collidepoint(event.pos) and self.game.score >= self.blue_manager_cost and not self.blue_owned:
                pygame.mixer.Sound.play(self.game.buy_click_sound)
                self.blue_owned = True
                self.game.clicked_blue_manager += 1
                self.game.score -= self.blue_manager_cost  
            if self.gray_manager_buy.collidepoint(event.pos) and self.game.score >= self.gray_manager_cost and not self.gray_owned:
                pygame.mixer.Sound.play(self.game.buy_click_sound)
                self.gray_owned = True
                self.game.clicked_gray_manager += 1
                self.game.score -= self.gray_manager_cost  
            if self.violet_manager_buy.collidepoint(event.pos) and self.game.score >= self.violet_manager_cost and not self.violet_owned:
                pygame.mixer.Sound.play(self.game.buy_click_sound)
                self.violet_owned = True
                self.game.clicked_violet_manager += 1
                self.game.score -= self.violet_manager_cost                
            
            if self.red_buy.collidepoint(event.pos) and self.game.score >= self.red_cost:
                pygame.mixer.Sound.play(self.game.buy_click_sound)
                self.game.clicked_more_red += 1
                self.red_value += 0.15
                self.game.score -= self.red_cost                
                self.red_cost += 0.1
            if self.orange_buy.collidepoint(event.pos) and self.game.score >= self.orange_cost:
                pygame.mixer.Sound.play(self.game.buy_click_sound)
                self.game.clicked_more_orange += 1
                self.orange_value += 0.3
                self.game.score -= self.orange_cost                
                self.orange_cost += 0.2
            if self.yellow_buy.collidepoint(event.pos) and self.game.score >= self.yellow_cost:
                pygame.mixer.Sound.play(self.game.buy_click_sound)
                self.game.clicked_more_yellow += 1
                self.yellow_value += 0.45
                self.game.score -= self.yellow_cost                
                self.yellow_cost += 0.3
            if self.green_buy.collidepoint(event.pos) and self.game.score >= self.green_cost:
                pygame.mixer.Sound.play(self.game.buy_click_sound)
                self.game.clicked_more_green += 1
                self.green_value += 0.60
                self.game.score -= self.green_cost                
                self.green_cost += 0.4
            if self.blue_buy.collidepoint(event.pos) and self.game.score >= self.blue_cost:
                pygame.mixer.Sound.play(self.game.buy_click_sound)
                self.game.clicked_more_blue += 1
                self.blue_value += 0.75
                self.game.score -= self.blue_cost                
                self.blue_cost += 0.5            
            if self.gray_buy.collidepoint(event.pos) and self.game.score >= self.gray_cost:
                pygame.mixer.Sound.play(self.game.buy_click_sound)
                self.game.clicked_more_gray += 1
                self.gray_value += 0.90
                self.game.score -= self.gray_cost                
                self.gray_cost += 0.6            
            if self.violet_buy.collidepoint(event.pos) and self.game.score >= self.violet_cost:
                pygame.mixer.Sound.play(self.game.buy_click_sound)
                self.game.clicked_more_violet += 1
                self.violet_value += 1.05
                self.game.score -= self.violet_cost                
                self.violet_cost += 0.7

            if self.red_multiplier.collidepoint(event.pos) and self.game.score >= self.red_multiplier_cost:
                pygame.mixer.Sound.play(self.game.buy_click_sound)
                self.game.clicked_red_speed += 1
                self.red_speed += 1.1
                self.game.score -= self.red_multiplier_cost    
                self.red_multiplier_cost += 100            
            if self.orange_multiplier.collidepoint(event.pos) and self.game.score >= self.orange_multiplier_cost:
                pygame.mixer.Sound.play(self.game.buy_click_sound)
                self.game.clicked_orange_speed += 1
                self.orange_speed += 1.1
                self.game.score -= self.orange_multiplier_cost  
                self.orange_multiplier_cost += 200              
            if self.yellow_multiplier.collidepoint(event.pos) and self.game.score >= self.yellow_multiplier_cost:
                pygame.mixer.Sound.play(self.game.buy_click_sound)
                self.game.clicked_yellow_speed += 1
                self.yellow_speed += 1.1
                self.game.score -= self.yellow_multiplier_cost     
                self.yellow_multiplier_cost += 300           
            if self.green_multiplier.collidepoint(event.pos) and self.game.score >= self.green_multiplier_cost:
                pygame.mixer.Sound.play(self.game.buy_click_sound)
                self.game.clicked_green_speed += 1
                self.green_speed += 1.1
                self.game.score -= self.green_multiplier_cost        
                self.green_multiplier_cost += 400        
            if self.blue_multiplier.collidepoint(event.pos) and self.game.score >= self.blue_multiplier_cost:
                pygame.mixer.Sound.play(self.game.buy_click_sound)
                self.game.clicked_blue_speed += 1
                self.blue_speed += 1.1
                self.game.score -= self.blue_multiplier_cost    
                self.blue_multiplier_cost += 500            
            if self.gray_multiplier.collidepoint(event.pos) and self.game.score >= self.gray_multiplier_cost:
                pygame.mixer.Sound.play(self.game.buy_click_sound)
                self.game.clicked_gray_speed += 1
                self.gray_speed += 1.1
                self.game.score -= self.gray_multiplier_cost      
                self.gray_multiplier_cost += 600          
            if self.violet_multiplier.collidepoint(event.pos) and self.game.score >= self.violet_multiplier_cost:
                pygame.mixer.Sound.play(self.game.buy_click_sound)
                self.game.clicked_violet_speed += 1
                self.violet_speed += 1.1
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
        self.game.screen.fill(black)

        self.task1, self.red_length,    self.drawing_red    = self.draw_task(color=red,      y_coord=50,     value=self.red_value,     draw=self.drawing_red,      length=self.red_length,     speed=self.red_speed )
        self.task2, self.orange_length, self.drawing_orange = self.draw_task(color=orange,   y_coord=110,    value=self.orange_value,  draw=self.drawing_orange,   length=self.orange_length,  speed=self.orange_speed  )
        self.task3, self.yellow_length, self.drawing_yellow = self.draw_task(color=yellow,   y_coord=170,    value=self.yellow_value,  draw=self.drawing_yellow,   length=self.yellow_length,  speed=self.yellow_speed  )
        self.task4, self.green_length,  self.drawing_green  = self.draw_task(color=green,    y_coord=230,    value=self.green_value,   draw=self.drawing_green,    length=self.green_length,   speed=self.green_speed )
        self.task5, self.blue_length,   self.drawing_blue   = self.draw_task(color=blue,     y_coord=290,    value=self.blue_value,    draw=self.drawing_blue,     length=self.blue_length,    speed=self.blue_speed )
        self.task6, self.gray_length,   self.drawing_gray   = self.draw_task(color=gray,     y_coord=350,    value=self.gray_value,    draw=self.drawing_gray,     length=self.gray_length,    speed=self.gray_speed )
        self.task7, self.violet_length, self.drawing_violet = self.draw_task(color=violet,   y_coord=410,    value=self.violet_value,  draw=self.drawing_violet,   length=self.violet_length,  speed=self.violet_speed  )

             
        
        self.red_buy,    self.red_manager_buy,     self.red_multiplier      = self.draw_buttons(red,      10,    self.red_cost,       self.red_owned,      self.red_manager_cost,       self.red_multiplier_cost   )
        self.orange_buy, self.orange_manager_buy,  self.orange_multiplier   = self.draw_buttons(orange,   66,    self.orange_cost,    self.orange_owned,   self.orange_manager_cost,    self.orange_multiplier_cost)
        self.yellow_buy, self.yellow_manager_buy,  self.yellow_multiplier   = self.draw_buttons(yellow,  122,    self.yellow_cost,    self.yellow_owned,   self.yellow_manager_cost,    self.yellow_multiplier_cost)
        self.green_buy,  self.green_manager_buy,   self.green_multiplier    = self.draw_buttons(green,   178,    self.green_cost,     self.green_owned,    self.green_manager_cost,     self.green_multiplier_cost )
        self.blue_buy,   self.blue_manager_buy,    self.blue_multiplier     = self.draw_buttons(blue,    234,    self.blue_cost,      self.blue_owned,     self.blue_manager_cost,      self.blue_multiplier_cost  )
        self.gray_buy,   self.gray_manager_buy,    self.gray_multiplier     = self.draw_buttons(gray,    290,    self.gray_cost,      self.gray_owned,     self.gray_manager_cost,      self.gray_multiplier_cost  )    
        self.violet_buy, self.violet_manager_buy,  self.violet_multiplier   = self.draw_buttons(violet,  346,    self.violet_cost,    self.violet_owned,   self.violet_manager_cost,    self.violet_multiplier_cost)

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
            self.red_cost = 1   
            self.red_owned = False
            self.red_manager_cost = 100
            self.red_multiplier_cost = 500
            self.orange_cost = 2
            self.orange_owned = False
            self.orange_manager_cost = 500
            self.orange_multiplier_cost = 1800
            self.yellow_cost = 3
            self.yellow_owned = False
            self.yellow_manager_cost = 1800
            self.yellow_multiplier_cost = 4000
            self.green_cost = 4
            self.green_owned = False
            self.green_manager_cost = 4000
            self.green_multiplier_cost = 10000
            self.blue_cost = 5
            self.blue_owned = False
            self.blue_manager_cost = 10000
            self.blue_multiplier_cost = 25000
            self.gray_cost = 6
            self.gray_owned = False
            self.gray_manager_cost = 25000
            self.gray_multiplier_cost = 60000
            self.violet_cost = 7
            self.violet_owned = False
            self.violet_manager_cost = 60000
            self.violet_multiplier_cost = 120000
            
            
            
            self.game.game_state = 'over'

  
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

class Over():
    """The game over screen. 
    """
    def __init__(self, game):
        """The Splash screen constructor

        Args:
            game (_type_): A reference to the game object. 
        """
        self.game = game
        self.game_over_screen = pygame.image.load('game_over_screen.png')
        self.manager_owned_img = pygame.image.load('manager_owned.png')
        self.continue_button = pygame.draw.rect(self.game.screen, gray, [(WIDTH // 2)-50, 550, 100, 40])
        self.exit_button = pygame.draw.rect(self.game.screen, gray, [(WIDTH // 2)-50, 610, 100, 40])
    
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
    def on_render(self):
        """The method to draw game objects to the screen. 
        """

        self.game.screen.blit(self.game_over_screen, (0, 0))
        game_clock_text = self.game.font.render('{:02d}:{:02d}'.format(self.game.clock_mins, self.game.clock_secs), True, white)
        self.game.screen.blit(game_clock_text, (162, 310))
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
            self.game.screen.blit(self.manager_owned_img, ( 55, 462))
        if self.game.clicked_orange_manager == 1:
            self.game.screen.blit(self.manager_owned_img, (115, 462))            
        if self.game.clicked_yellow_manager == 1:
            self.game.screen.blit(self.manager_owned_img, (165, 462))            
        if self.game.clicked_green_manager == 1:
            self.game.screen.blit(self.manager_owned_img, (215, 462))            
        if self.game.clicked_blue_manager == 1:
            self.game.screen.blit(self.manager_owned_img, (265, 462))            
        if self.game.clicked_gray_manager == 1:
            self.game.screen.blit(self.manager_owned_img, (315, 462))            
        if self.game.clicked_violet_manager == 1:
            self.game.screen.blit(self.manager_owned_img, (365, 462))            
        
        # speed
        self.game.draw_text(( 75,  500), f'{self.game.clicked_red_speed}', white )
        self.game.draw_text((125,  500), f'{self.game.clicked_orange_speed}', white )
        self.game.draw_text((175,  500), f'{self.game.clicked_yellow_speed}', white )
        self.game.draw_text((225,  500), f'{self.game.clicked_green_speed}', white )
        self.game.draw_text((280,  500), f'{self.game.clicked_blue_speed}', white )
        self.game.draw_text((330,  500), f'{self.game.clicked_gray_speed}', white )
        self.game.draw_text((385,  500), f'{self.game.clicked_violet_speed}', white )
        
        self.continue_button = pygame.draw.rect(self.game.screen, gray, [int(WIDTH * 0.25)-50, 550, 100, 40])
        self.continue_text = self.game.font.render("Continue", True, black)
        self.game.screen.blit(self.continue_text, (int(WIDTH * 0.25) - 38, 562))
        self.exit_button = pygame.draw.rect(self.game.screen, gray, [int(WIDTH * 0.75)-50, 550, 100, 40])
        self.exit_text = self.game.font.render("Exit", True, red)
        self.game.screen.blit(self.exit_text, (int(WIDTH * 0.75) - 16, 562))
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
        self.GAME_START_TIME = pygame.time.get_ticks()
        self.pygame_time = self.GAME_START_TIME
        self.width, self.height = WIDTH, HEIGHT  
        # dev_pos_x = MONITOR_WIDTH - WIDTH 
        # dev_pos_y = 133 
        # os.environ['SDL_VIDEO_WINDOW_POS'] = '%i,%i' % (dev_pos_x,dev_pos_y)
        self.screen = pygame.display.set_mode((self.width, self.height))   
        pygame.display.set_caption("One Hundred Thousandaire")
        self.fps = 60
        self.game_clock = pygame.time.Clock()  
        self.font = pygame.font.Font('freesansbold.ttf', 16)
        self.background_sound = pygame.mixer.music.load('snd_background_loop.ogg')
        self.task_click_sound = pygame.mixer.Sound('snd_task_click.wav')
        self.buy_click_sound = pygame.mixer.Sound('snd_buy_click.wav')
        self.is_running = True
   
        self.splash = Splash(self)
        self.action = Action(self)
        self.over = Over(self)
        self.game_state = 'splash'
        self.score =  0 #  99999   #  
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
                self.action.run()
            elif self.game_state == 'over':
                self.over.run()

            self.game_clock.tick(FPS)
        
        pygame.quit()
        sys.exit(0)
        
if __name__ == "__main__":
    game = Game()
    game.run()

