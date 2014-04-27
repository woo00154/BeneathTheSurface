import pygame

class Button:
    
    def __init__(self,text,size):
        self.size = size
        self.text = text
        
        font = pygame.font.Font('data/fonts/freesansbold.ttf',size)
        self.name = font.render(text, 1, (100,100,100))
        self.rect = self.name.get_rect()
        
        self.selected = pygame.Surface((self.rect.w,self.rect.h))
        self.selected.fill((255,255,255))
        
    def set_pos(self,x,y):
        self.rect.left = x
        self.rect.top = y
        
    def get_pos(self):
        return self.rect.left,self.rect.top
        

    

        
    def __str__(self):
        return self.text