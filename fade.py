import pygame



class Fade:
    
    def __init__(self,screen,mode,speed):
        self.surface = pygame.Surface(screen.get_size())
        self.surface.fill((0,0,0))
        self.mode = mode
        self.done = False
        
        if mode == 'in':
            self.fade = 255
            self.speed = -speed
        elif mode == 'out':
            self.speed = speed
            self.fade = 0
            
        self.surface.set_alpha(self.fade)
        
    

    
    def loop(self):
        if (self.mode == 'in' and self.fade == 255) or (self.mode == 'out' and self.fade == 0):
            self.done = True
        if not self.done:
            if 0 < self.fade < 255:
                self.fade += self.speed
            elif self.fade < 100:
                self.fade = 0
                self.done = True
            elif self.fade >= 100:
                self.fade = 255
                self.done = True
            self.surface.set_alpha(self.fade)
        
        return self.done
    