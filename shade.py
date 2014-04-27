import pygame

class Shade:
    
    def __init__(self, strength,screen):
        self.surface = pygame.Surface(screen.get_size())
    
        self.surface.set_alpha(strength)