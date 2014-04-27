import pygame
from person import Person
from img_n_sound import * 
from inputhandler import InputHandler
from status import *
 
class Player(Person):
    
    def __init__(self,spawn_x=100,spawn_y=100,entity = []):
        Person.__init__(self,spawn_x,spawn_y,'0.png', 'player\\default')
        self.inputhandler = InputHandler()
        self.admin = self.physics = self.parkour = False
        self.add_basic_movement()
        self.add_physics()
        self.add_parkour()
        self.add_stats(entity)
        self.state = 'idle'
        self.stage = 0
        self.next_stage = False
        self.direc = 1 #right
        #self.add_animation()
        
    def add_animation(self):    
        self.motion = 'default'
        
    def set_spawn(self,x,y):
        self.spawn_x = x
        self.spawn_y = y
    
    
    def add_basic_movement(self):
        self.jumping = self.onGround = self.running = False
        self.inputhandler.add_button('right')
        self.inputhandler.add_button('left')
        self.inputhandler.add_button('up')
        self.inputhandler.add_button('sprint')
        self.inputhandler.add_button('down')
        self.inputhandler.add_button('jump')
        
    def add_parkour(self):
        self.parkour = True
        self.hanging = self.onWall_R = self.onWall_L = self.climb = False
        
    def place(self,entity):
        Person.reset(self,entity)
        
    def stamina_reset(self):
        self.status['stamina'].reset()
    
    def reset(self,entity):
        Person.reset(self,entity)
        self.status['health'].set(self.status['health'].maximum)
        self.status['stamina'].set(self.status['stamina'].maximum)
        self.dead = False
        self.add_physics()
        self.add_parkour()
        
        
    def add_physics(self):
        self.physics = True
        self.acc = 1
        self.speed_limit = 4
        self.walk_limit = 2
        self.run_limit = 4
        self.sprint_limit = 8
        self.fall_time = 0
        self.fall_limit = 20
        self.wall_slide_limit = 25
        self.wall_slide_time = 0
        
        self.control = True
        
    def add_stats(self,entity):
        
        self.status = {}
        #health
        self.status.update({'health':Health()})
        #exp
        self.exp = None
        #self.status.append(self.exp)
        #hunger
        self.hunger = None
        #self.status.append(self.hunger)
        #stamina
        self.status.update({'stamina':Stamina()})

        #money
        self.money = 0
        #danger
        self.danger = 0

        
    def get_button(self,button):
        return self.inputhandler.button_list[button]
    
    def set_button(self,button,state):
        self.inputhandler.button_list[button] = state
        
    def admin_tick(self):
        #allows the player to float around
        self.xvel = self.yvel = 0
        if self.get_button('right'):
            self.xvel = 5
        if self.get_button('left'):
            self.xvel = -5
        if self.get_button('up'):
            self.yvel = -5
        if self.get_button('down'):
            self.yvel = 5
            
        self.rect.left += self.xvel
        self.rect.top += self.yvel
        
    def x_movement(self):
        if self.physics:
            if self.get_button('right') and not self.get_button('left') and self.control:
                if self.xvel <= self.speed_limit:
                    self.xvel += self.acc
                else:
                    self.xvel -= self.acc
            elif self.get_button('left') and not self.get_button('right') and self.control:
                if self.xvel >= -self.speed_limit:
                    self.xvel -= self.acc
                else:
                    self.xvel += self.acc
            elif (self.get_button('left') and self.get_button('right') and self.control) or \
                (not self.get_button('left') and not self.get_button('right') and self.control):
                if self.xvel != 0:
                    self.xvel /= 2
                    if -1< self.xvel < 1:
                        self.xvel = 0
                #allows a player to run
            
            if self.get_button('sprint'):
                self.speed_limit = self.sprint_limit
            elif self.running:
                self.speed_limit = self.run_limit
            else:
                self.speed_limit = self.walk_limit

        else:
            if self.get_button('right') and not self.get_button('left'):
                self.xvel = self.run_limit
            elif not self.get_button('right') and self.get_button('left'):
                self.xvel = -self.run_limit
            else:
                self.xvel = 0
            if self.get_button('sprint'):
                    self.xvel *=2
                
    def wall_movement(self):
        if self.onWall and self.wall_slide_limit > self.wall_slide_time:
            #wall slide
            if self.yvel > 0:
                self.yvel = 2
                self.wall_slide_time += 1
            #if on ground, do nothing
            elif self.yvel==0 and not self.hanging:
                return
            self.jumping = True
            #wall jump
            if self.get_button('jump') and not self.onGround:
                if self.status['stamina'].cost(20):
                    if self.onWall_R and self.get_button('right') and not self.get_button('left'):
                        self.yvel = -15
                        self.xvel = -5
                    elif self.onWall_L and not self.get_button('right') and self.get_button('left'):
                        self.yvel = -15
                        self.xvel = 5
            #climb
            if self.get_button('up') and self.hanging:
                if self.status['stamina'].cost(10):
                    self.climb = True
                    self.yvel = -15
                    self.xvel = 0
            
        elif not self.onWall or self.hanging:
            self.wall_slide_time = 0
        elif self.wall_slide_limit <= self.wall_slide_time:
            self.onWall_L = self.onWall_R = self.onWall = False
        
    def tick(self,platforms,entity):
        if self.status['health'].current <= 0:
            self.dead = True
            

        self.onWall = self.onWall_L or self.onWall_R
        #make sure the charater has the control at certain point
        if not self.jumping or self.onWall or self.hanging or self.climb:
            self.control = True
        else:
            self.control = False
        
        
        #all the x-component movements
        self.x_movement()
        #apply gravity
        self.gravity.apply(self)
        #all wall-related movements
        self.wall_movement()
        
        #all the y-component movements    
        if self.onGround:
            self.jumping = self.climb = False
    
        if self.get_button('jump') and self.onGround:
            if self.status['stamina'].cost(20):
                self.yvel = -15
                self.set_button('jump',False)
                self.jumping = True
         
        Person.tick(self,platforms)
        
        if self.yvel > 2 and not self.onWall:
            
            self.fall_time+=1
        elif self.onWall and self.fall_time > 0:
            self.fall_time-=1
        elif self.onGround:
            self.status['health'].current -= int(self.fall_time/self.fall_limit) * 20
        if self.yvel <= 0:
            self.fall_time = 0

              
        #make sure status stays updated
        for s in self.status.values():
            s.update()
            
        