import pygame

class Shade:
    
    def __init__(self, strength,screen):
        self.surface = pygame.Surface(screen.get_size())
        
        self.surface.set_alpha(strength)
        
        self.strength = strength
    def loop(self):
        self.surface.set_alpha(self.strength)