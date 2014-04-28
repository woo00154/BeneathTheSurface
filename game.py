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
        self.game_dimension = (screen.get_size()[0],screen.get_size()[1]*0.75)
        self.game_surface = pygame.Surface(self.game_dimension)
        
        #MUST BE FIXED
        self.stage = Stage(self.game_dimension)
        self.stage.load_stage('Intro')
        self.map = self.stage.rooms[0]
        

        #133442__klankbeeld__horror-ambience-11.wav
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)
        
        
        
        self.fade = Fade(screen,'in',3)
        #add player
        self.player = Player(self.map.spawn_x,self.map.spawn_y,self.map.entity)
        
        self.map.entity.append(self.player)
        self.shade = Shade(self.player,0,self.fade.surface)
        #test
        self.loading = False
        self.next_before = True
    
    def exit_stage(self):
        self.loading = True
        self.fade.switch_mode()
    
    def next_stage(self):

        if self.fade.done:
            self.fade.switch_mode()
            self.player.stage += self.next_before
            self.map = self.stage.rooms[self.player.stage]
            self.player.set_spawn(self.map.spawn_x,self.map.spawn_y)
            self.player.place(self.map.entity)
            self.loading = False
            
            if self.player.stamina_regen:
                self.player.stamina_reset()
            
#             if self.player.stage > 0:
#                 self.shade = Shade(self.player,self.player.stage,self.fade.surface)
#             else:
#                 self.shade = Shade(self.player,0,self.fade.surface)
#
            if self.player.stage == 0:
                self.bgm.stop()
                #self.bgm.fadeout(1000)
            if self.player.stage == 1:
                self.bgm = pygame.mixer.Sound(os.path.join('data','music',"wind.wav"))
                self.bgm.play(loops = -1,fade_ms = 10000)
                
            
    
    def set_button(self,button,state):
        self.player.inputhandler.button_list[button] = state
        
    def tick(self,events):
        
        if self.loading:
            if self.fade.loop():
                if self.next_before != 0:
                    self.next_stage()
                    
        else:
            if self.player.out_of_screen(self.map.map_size):
                self.player.status['health'].current = 0
                

            
            self.player.interacting = False
            
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
                    if e.key == K_RETURN:
                        self.player.interacting = True
                    
                    if e.key == K_RIGHTBRACKET:
                        self.next_before = 1
                        self.exit_stage()
                        
                        
                    if e.key == K_LEFTBRACKET:
                        self.next_before = -1
                        self.exit_stage()
                    
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
                    
            if self.map.previous_stage != None:
                if pygame.sprite.collide_rect(self.player, self.map.previous_stage) and not self.loading and self.player.interacting:
                    self.next_before = -1
                    self.exit_stage()
                    
            if pygame.sprite.collide_rect(self.player, self.map.next_stage) and not self.loading and self.player.interacting:
                self.next_before = 1
                self.exit_stage()   
                     
            for i in self.map.interactables:
                if pygame.sprite.collide_rect(self.player, i) and self.player.interacting and not self.loading:
                    self.interacting = False
                    return 'Shop'
                    
                     
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
        self.layer_5(screen)
    
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
        self.shade = Shade(self.player, self.player.stage * self.player.brightness,screen)
        #self.shade.loop(self.player)
        screen.blit(self.shade.surface,(0,(self.shade.surface.get_size()[1] - self.game_dimension[1])//2))
    