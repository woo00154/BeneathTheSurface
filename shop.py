#A basic menu before the game starts
#There should be another menu that pops up when ESC is pressed.

import pygame,sys
from pygame.locals import *
from button import Button
from mode import Mode
from collections import OrderedDict

class Shop(Mode):
    def __init__(self,screen,player):
        self.player = player
        Mode.__init__(self,screen)

        buttons = OrderedDict()

        buttons.update({'health upgrade':self.player.status['health'].maximum})
        buttons.update({'stamina upgrade':self.player.status['stamina'].maximum})
        buttons.update({'brightness upgrade':self.player.brightness})
        buttons.update({'stamina regeneration': ''})
        buttons.update({'climbing upgrade':''})
        buttons.update({ 'Exit':''})
#         buttons = OrderedDict({
#                                
#                                'stamina regeneration': '', \
#                                'climbing upgrade':'', \
#                                'Exit':'', \
#                                'brightness upgrade':self.player.brightness,\
#                                'stamina_upgrade':self.player.status['stamina'].maximum, \
#                                'health upgrade':self.player.status['health'].maximum})
        buttons = self.check_buttons(buttons)
        
        self.buttons = self.create_buttons(buttons)
        #the first button is chosen by default
        self.cursor = 0
        self.current_button = self.buttons[self.cursor]
        
        
    def check_buttons(self,buttons):
        hp = self.player.status['health']
        sp = self.player.status['stamina']
        b = self.player.brightness
        if hp.maximum == hp.true_maximum:
            del buttons['health upgrade']
        if sp.maximum == sp.true_maximum:
            del buttons['stamina upgrade']
        if self.player.stamina_regen:
            del buttons['stamina regeneration'] 
        if b <= 0:
            del buttons['brightness upgrade']
        if self.player.parkour:
            del buttons['climbing upgrade']
        return buttons
        
    def create_buttons(self,buttons) -> list:
        #make an empty list and choose a font size
        button_list = []
        description_list = []
        button_size = 36
        #create basic buttons
        for a in buttons:
            button_list.append(Button(a,button_size))
            description_list.append(Button(str(buttons[a]),button_size))
        #out of all buttons, choose the longest button and save its width
        for b in button_list:
            if max(buttons,key=len) == str(b):
                w = b.rect.w
                h = b.rect.h
                x = self.surface.get_rect().centerx - w
                y = self.surface.get_rect().centery - len(buttons) * h / 2
        #now place all the buttons at designated position
        temp = y
        for b in button_list:
            b.set_pos(x,y)
            y += b.rect.h
            
        for b in description_list:
            b.set_pos(x+400,temp)
            temp += b.rect.h
        #put the buttons on the surface
        for b in button_list:
            self.surface.blit(b.name,b.rect)
            
        for b in description_list:
            self.surface.blit(b.name,b.rect) 
        #create another surface to show the rectangle (the chosen button)
        self.selected = pygame.Surface((w,h))

        #return button_list so we can save to self.buttons 
        return button_list

            
    def __str__(self):
        #used to easily call or reference the class
        return 'Shop'
    
    def tick(self,events):
        #key inputs
        for e in events:
            if e.type == KEYDOWN:
                if e.key == K_UP:
                    self.cursor -= 1
                if e.key == K_DOWN:
                    self.cursor += 1
                if e.key == K_RETURN:
                    s = str(self.current_button)
                    cost = 0
                    if s == 'health upgrade':
                        if self.health_upgrade_cost(self.player.status['health'].maximum) != -1:
                            cost = self.health_upgrade_cost(self.player.status['health'].maximum)
                            self.player.status['health'].maximum = self.health_upgrade(self.player.status['health'].maximum)
                    if s == 'stamina upgrade':
                        if self.stamina_upgrade_cost(self.player.status['stamina'].maximum) != -1:
                            cost = self.stamina_upgrade_cost(self.player.status['stamina'].maximum)
                            self.player.status['stamina'].maximum = self.stamina_upgrade(self.player.status['stamina'].maximum)
                    if s == 'lighting upgrade':
                        if self.lighting_upgrade_cost(self.player.brightness) != -1:
                            cost = self.lighting_upgrade_cost(self.player.brightness)
                            self.player.brightness = self.lighting_upgrade(self.player.brightness)
                    if s == 'stamina regeneration':
                        if self.stamina_regen_upgrade_cost(self.player.stamina_regen) != -1:
                            cost = self.stamina_regen_upgrade_cost(self.player.stamina_regen)
                    if s == 'climbing gear':
                        if self.climbing_gear_cost(self.player.status['health'].maximum) != -1:
                            cost = self.climbing_gear_cost(self.player.status['health'].maximum)
                            
                    self.player.status['money'].lose(cost)
                    
                    if s == 'Exit':
                        return 'Continue'
                    
                if e.key == K_ESCAPE:
                    return 'Continue'
            elif e.type == QUIT:
                pygame.display.quit()
                sys.exit()
        #if self.cursor goes out of list boundary, loops back      
        if self.cursor <= -1:
            self.cursor = len(self.buttons)-1
        elif self.cursor >= len(self.buttons):
            self.cursor = 0
        self.current_button = self.buttons[self.cursor]
        print(self.current_button)
        
        return str(self)
    
    def render(self,screen):      
        Mode.render(self,screen)
        #display rectangle to show chosen menu
        self.selected.fill((255,255,255))
        self.selected.set_alpha(80)
        screen.blit(self.selected,self.current_button.get_pos())
        
            




    def health_upgrade_cost(self,max_health):
        if max_health == 100:
            return -1
        return max_health * 20
    
    def health_upgrade(self, max_health):
        return max_health + 20
    
    def stamina_upgrade_cost(self,max_stamina):
        if max_stamina == 200:
            return -1
        return max_stamina * 10
    
    def stamina_upgrade(self, max_stamina):
        return max_stamina + 20
    
    def lighting_upgrade_cost(self, lighting):
        if lighting == 0:
            return -1
        return (100 - lighting) * 20
    
    def lighting_upgrade(self,lighting):
        return lighting - 10
    
    def stamina_regen_upgrade_cost(self, regen_state):
        if regen_state:
            return -1
        else:
            return 200
        
    def climbing_gear_cost(self, gear_state):
        if gear_state:
            self.buttons.remove()
            return -1
        else:
            return 1000      
            
        
        
        
        
        
        