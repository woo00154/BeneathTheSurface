import pygame,sys,os
from img_n_sound import *

class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, image,colorkey=-1,folder=None):
        pygame.sprite.Sprite.__init__(self)
        self.image,self.rect = load_image(image,colorkey,folder)
        self.rect = Rect(x,y,*self.image.get_size())
        self.interact = False
        self.message = "..."
    
    def interacted(self,interact):
        if not self.interact and interact:
            self.interact = True
            self.talk()
        if self.interact and not interact:
            self.interact = False
            
    def set_message(self,message):
        self.message = message
        
    def talk(self):
        print(self.message)