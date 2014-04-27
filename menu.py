#A basic menu before the game starts
#There should be another menu that pops up when ESC is pressed.

import pygame,sys
from pygame.locals import *
from button import Button
from mode import Mode

class Menu(Mode):
    def __init__(self,buttons,screen):
        Mode.__init__(self,screen)
        
        self.buttons = self.create_buttons(buttons)
        #the first button is chosen by default
        self.cursor = 0
        self.current_button = self.buttons[self.cursor]
        
    def create_buttons(self,buttons) -> list:
        #make an empty list and choose a font size
        button_list = []
        button_size = 36
        #create basic buttons
        for b in buttons:
            button_list.append(Button(b,button_size))
        #out of all buttons, choose the longest button and save its width
        for b in button_list:
            if max(buttons,key=len) == str(b):
                w = b.rect.w
                h = b.rect.h
                x = self.surface.get_rect().centerx - w/2
                y = self.surface.get_rect().centery - len(buttons) * h / 2
        #now place all the buttons at designated position
        for b in button_list:
            b.set_pos(x,y)
            y += b.rect.h
        #put the buttons on the surface
        for b in button_list:
            self.surface.blit(b.name,b.rect) 
        #create another surface to show the rectangle (the chosen button)
        self.selected = pygame.Surface((w,h))

        #return button_list so we can save to self.buttons 
        return button_list

            
    def __str__(self):
        #used to easily call or reference the class
        return 'Menu'
    
    def tick(self,events):
        #key inputs
        for e in events:
            if e.type == KEYDOWN:
                if e.key == K_UP:
                    self.cursor -= 1
                if e.key == K_DOWN:
                    self.cursor += 1
                if e.key == K_RETURN:
                    return str(self.current_button)
                if e.key == K_ESCAPE:
                    return 'Quit'
            elif e.type == QUIT:
                pygame.display.quit()
                sys.exit()
        #if self.cursor goes out of list boundary, loops back      
        if self.cursor <= -1:
            self.cursor = len(self.buttons)-1
        elif self.cursor >= len(self.buttons):
            self.cursor = 0
        self.current_button = self.buttons[self.cursor]
        
        return str(self)
    
    def render(self,screen):      
        Mode.render(self,screen)
        #display rectangle to show chosen menu
        self.selected.fill((255,255,255))
        self.selected.set_alpha(80)
        screen.blit(self.selected,self.current_button.get_pos())
        
            

