from image import Image
import pygame
from img_n_sound import *

class Status(Image):
    
    def __init__(self,image,color,y):
        #Image.__init__(self,40,y,'status_bar.png',folder = 'status')
        self.value = pygame.Surface((30,25))
        self.value.fill(color)
        self.value = self.value.convert()
        self.container = pygame.Surface((34,29))
        self.container.fill((255,255,255))
        self.container = self.container.convert()
        self.x = 40
        self.y = y
        
        self.symbol = load_image(image + '.png',folder = 'status')[0]
        #self.status_bar_rect = self.box.get_rect()
      
        self.current = 40
        self.maximum = 40

    def low(self):
        return self.current <= self.max * 0.2
    
    def update(self):
        if self.current > self.maximum:
            self.current = self.maximum
        elif self.current < 0 :
            self.current = 0.0
            
    def reset(self):
        self.current = self.maximum

    def render(self,screen):
        screen.blit(self.symbol,(self.x-35,self.y+2))
        #screen.blit(self.image,(x,y))
        for v in range(self.maximum//20):
            screen.blit(self.container,(v*34 + self.x, self.y))
        for v in range(int(self.current//20)):
            screen.blit(self.value,(v*34 + self.x+2, self.y+2))
            
    def set(self,value):
        self.current = value
        
    def upgrade(self):
        self.maximum += 20    
    
class Stamina(Status):
    
    def __init__(self):
        Status.__init__(self,'stamina',(100,149,247),45)
        self.state = True
        self.recharge_speed = 1
        
        self.current = 80
        self.maximum = 80
        
    def update(self):
        Status.update(self)
        #self.exhaust()
        #if not self.state:
        #    self.current += 1
        if self.current == self.maximum:
            self.state = True
            
        
    def cost(self,value):
        self.current = self.current//20 * 20
        
        if self.current - value < 0 or not self.state:
            return False
        else:
            self.current -= value
            return True
        
    def exhaust(self):
        if self.current == 0:
            self.state = False
    
    def recover(self,value):
        if self.state:
            self.current += value
        
    
class Health(Status):
    
    def __init__(self):
        Status.__init__(self,'health',(124,252,0),10)
        

