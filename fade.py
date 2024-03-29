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
        
    def switch_mode(self):
        self.speed = -self.speed
        if self.mode == 'in':
            self.mode = 'out'        
        elif self.mode == 'out':
            self.mode = 'in'
        else:
            raise Exception
        self.done = False
        
            

    
    def loop(self):

        if not self.done:
            if 0 <= self.fade <= 255:
                self.fade += self.speed
            elif self.fade < 0:
                self.fade = 0
                self.done = True
            elif self.fade > 255:
                self.fade = 255
                self.done = True
            self.surface.set_alpha(self.fade)
        
        return self.done
    