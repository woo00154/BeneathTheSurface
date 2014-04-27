import pygame
from entity import Entity
from img_n_sound import *

class Platform(Entity):
    
    def __init__(self,x,y,tx,ty,size):
        Entity.__init__(self,x,y,size,size)
        pygame.sprite.Sprite.__init__(self)
        self.image = load_tileset(size,size,tx,ty)
        self.rect = Rect(x,y,size,size)
        self.type = tx,ty
        
