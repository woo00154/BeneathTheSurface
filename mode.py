import pygame

class Mode:
    
    def __init__(self,screen):
        #basic menu surface
        self.surface = pygame.Surface(screen.get_size())    
    
    def loop(self,events,screen):
        #basic loop with update and draw
        mode = self.tick(events)
        self.render(screen)
        #if mode is not str(self), the game_mode will switch
        return mode
    
    def tick(self,events):
        pass
    
    def render(self,screen):
        #display all contents
        screen.blit(self.surface,(0,0))
    
    def __str__(self):
        return 'Name Not Chosen'