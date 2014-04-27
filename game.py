import pygame,sys
from mode import Mode
from pygame.locals import *
from map import *
from fade import Fade 
from loading import Loading 
from player import Player 
from shade import Shade
 
 
        
class Game(Mode):
    def __init__(self,screen):
        Mode.__init__(self,screen)
        #create a loading screen
        Loading(screen)
        self.loading = True
        
        #border color
        self.surface.fill((0,0,0))
        
        screen.blit(self.surface,(0,0))
        #create border at top and bottom
        game_dimension = (screen.get_size()[0],screen.get_size()[1]*0.75)
        self.game_surface = pygame.Surface(game_dimension)
        
        #MUST BE FIXED
        self.stage = Stage(game_dimension)
        self.stage.load_stage('Intro')
        self.map = self.stage.rooms[0]
        self.shade = Shade(200,screen)
        
        
        self.fade = Fade(screen,'in',3)
        #add player
        self.player = Player(self.map.spawn_x,self.map.spawn_y,self.map.entity)
        
        self.map.entity.append(self.player)
        
        #test
        self.loading = False
    
    
    def next_stage(self):
        self.fade.switch_mode()
        while self.fade.loop():
            print(1)
        
        if self.fade.done:
            self.fade.switch_mode()
            self.player.stage += 1
            self.map = self.stage.rooms[self.player.stage]
            self.player.set_spawn(self.map.spawn_x,self.map.spawn_y)
            self.player.place(self.map.entity)
        
            
    
    def set_button(self,button,state):
        self.player.inputhandler.button_list[button] = state
        
    def tick(self,events):
        
        if pygame.sprite.collide_rect(self.player, self.map.next_stage):
            self.next_stage()
        
        
        
        for e in self.map.entity:
            if e.dead:
                self.map.entity.remove(e)
        for e in events:
            if e.type == KEYDOWN:
                if e.key == K_RIGHT:
                    self.set_button('right',True)
                if e.key == K_LEFT:
                    self.set_button('left',True)
                if e.key == K_UP:
                    self.set_button('up',True)
                    self.player.jumping = True
                if e.key == K_LSHIFT:
                    self.set_button('sprint',True)
                if e.key == K_DOWN:
                    self.set_button('down',True)
                if e.key == K_z:
                    self.set_button('jump',True)    
                if e.key == K_x:
                    self.set_button('low_jump',True)
                if e.key == K_r:
                    self.player.reset(self.map.entity)
                if e.key == K_t:
                    self.player.admin = not self.player.admin
                if e.key == K_TAB:
                    self.player.running = not self.player.running
                
                if e.key == K_ESCAPE:
                    return 'Menu'

            elif e.type == KEYUP:
                if e.key == K_RIGHT:
                    self.set_button('right',False)
                if e.key == K_LEFT:
                    self.set_button('left',False)
                if e.key == K_LSHIFT:
                    self.set_button('sprint',False)
                if e.key == K_UP:
                    self.set_button('up',False)
                if e.key == K_DOWN:
                    self.set_button('down',False)
                if e.key == K_z:
                    self.set_button('jump',False)    
            elif e.type == QUIT:
                pygame.display.quit()
                sys.exit()
        self.fade.loop()
        self.map.camera.update(self.player)
        if not self.player.dead:
            if not self.player.admin:
                self.player.tick(self.map.platforms,self.map.entity)
            elif self.player.admin:
                self.player.admin_tick()
                
        

            


    
    def render(self,screen):
        self.layer_1(screen)
        self.layer_2(screen)
        self.layer_3(screen)
        self.layer_4(screen)
    
    def __str__(self):
        return 'Game'
    
    #background
    def layer_1(self,screen):
        Mode.render(self,screen)
    #map obstacles + player
    def layer_2(self,screen):
        
        self.game_surface.fill((255,255,255))
        for e in self.map.entity:
            self.game_surface.blit(e.image, self.map.camera.apply(e))
        screen.blit(self.game_surface,(0,screen.get_size()[1]*0.125))
    #player status       
    def layer_3(self,screen):
        for s in self.player.status.values():
            s.render(screen)
    #fade in/out    
    def layer_4(self,screen):
        screen.blit(self.fade.surface,(0,0))
        
    def layer_5(self,screen):
        screen.blit(self.shade.surface,(0,0))
    