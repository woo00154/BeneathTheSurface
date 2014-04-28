import pygame
from image import Image

class Shade:
    
    def __init__(self, player, strength,screen):
        
        self.surface = pygame.Surface(screen.get_size())
        x,y = player.rect.x,player.rect.y
        #Image.__init__(self,x,y,"shade.png")
        self.surface.set_alpha(strength)
        
        self.strength = strength
        
        #self.surface.blit(self.image,(player.rect.x,player.rect.y))
    def loop(self,player):
        self.rect.centerx = player.rect.centerx
        self.rect.centery = player.rect.centery
        self.surface.blit(self.image,(player.rect.x,player.rect.y))
        self.image.set_alpha(255)
        print(player.rect.centerx)