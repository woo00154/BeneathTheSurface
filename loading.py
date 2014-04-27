import pygame

class Loading:
    
    def __init__(self,screen):
        surface = pygame.Surface(screen.get_size())
        font = pygame.font.Font('data/fonts/freesansbold.ttf',50)
        self.name = font.render('Loading...', 1, (100,100,100))
        self.rect = self.name.get_rect()
        x,y = screen.get_size()
        self.rect.centerx = x/2
        self.rect.centery = y/2
        surface.blit(self.name,self.rect)
        screen.blit(surface,(0,0))
        pygame.display.flip()