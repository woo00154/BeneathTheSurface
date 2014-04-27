import pygame,os
from pygame.locals import *
import xml.etree.ElementTree as ET
from img_n_sound import *
from camera import *
from platform import Platform
from object import Object




class Map():
    def __init__(self,dimension):
        self.platforms = []
        self.objects = []
        self.entity = []
        self.people = []
        self.dimension = dimension
        self.camera = Camera(*self.dimension)
        
        
    def load_map(self,folder,name):
        #This should be read from layout.txt
        self.spawn_x = 50
        self.spawn_y = 50
        
        #opens an .oel file and create map from it
        tree = ET.parse(os.path.join('data','maps',folder,name))
        root = tree.getroot()
        self.camera.map_w = int(root.attrib['width'])
        self.camera.map_h = int(root.attrib['height'])
        for r in root:

            for o in r:
                if o.tag == 'tile':
                    size = 25
                    target = Platform(int(o.attrib['x'])*size,int(o.attrib['y'])*size,int(o.attrib['tx']),int(o.attrib['ty']),size)
                    if int(o.attrib['tx']) == 7 and int(o.attrib['ty']) == 1:
                        self.spawn_x = int(o.attrib['x']) * size
                        self.spawn_y = int(o.attrib['y']) * size
                    elif int(o.attrib['tx']) == 6 and int(o.attrib['ty']) == 1:
                        pass
                    else:
                        self.platforms.append(target)
                        self.entity.append(target)
                
                else:
                    
                    target = Object(int(o.attrib['x']),int(o.attrib['y']),o.tag+'.png',colorkey=None,folder='maps')
                    target.set_message('This is a ' + o.tag)
                    self.objects.append(target)
                    self.entity.append(target)
                
                

        return self
    
    def add_platform(self,target):
        self.entity.append(target)
        self.platforms.append(target)
        
    def add_object(self,target):
        self.entity.append(target)
        self.objects.append(target)
        
class Stage():
    def __init__(self,dimension):
        self.dimension = dimension
        self.rooms = []
        #self.add_floor()
        
    def load_stage(self,stage):
       
        for room in os.listdir(os.path.join('data','maps',stage)):
            if room != 'layout.txt':
                self.add_room(stage,room)
            
        return self.rooms
        
    def add_room(self,stage,room):
        self.rooms.append(Map(self.dimension).load_map(stage,room))
