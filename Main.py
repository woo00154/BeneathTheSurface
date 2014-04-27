import pygame,sys,os
from pygame.locals import *
from menu import Menu 
from img_n_sound import *
from game import Game
#must import this to not make error for cx_Freeze. Reason unknown
import re
class Main:
    def __init__(self):
        #pygame setup
        pygame.init()
        
        #set resolution and screen size
        resolution = (800, 800)
        self.screen = pygame.display.set_mode(resolution)
        #create main surface to draw everything on.
        self.surface = pygame.Surface(self.screen.get_size())
        pygame.display.set_caption('Parkour Simulator')
        
        
        #background surface setting
        bg = pygame.Surface(resolution)
        bg.convert()
        bg.fill(Color("#FFFFFF"))
        
        #draw the initial background
        pygame.display.flip()
        
        #clock is set to choose the fps
        self.clock = pygame.time.Clock()
        
        #Any intro cinematics go here
        pass
        #Then it sets the mode to menu
        self.selected_mode = 'Menu'
        self.current_mode = None
        #Finally, the mainloop starts
        self.main_loop()

    def main_loop(self):
        
        while 1:
            #set fps
            self.clock.tick(60)
            #if the desired mode is changed, then change the program to that mode.
            if self.selected_mode != str(self.current_mode):                
                if self.selected_mode == 'Start':
                    self.current_mode = Game(self.screen)
                elif self.selected_mode == 'Menu':
                    self.current_mode = Menu(['Start','Quit'],self.screen)

                elif self.selected_mode == 'Quit':
                    raise SystemExit
            #if the current_mode exist, run its loop    
            if self.current_mode != None:
                #the loop usually returns a str(self), so when it is not the case, the mode changes
                self.selected_mode = self.current_mode.loop(pygame.event.get(),self.screen)
                pygame.display.flip()

if __name__ == '__main__':
    Main()