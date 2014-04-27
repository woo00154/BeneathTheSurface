import pygame,os
from pygame.locals import *


def load_image(name='',colorkey=None,main_folder = 'images',folder=''):
    
    fullname = os.path.join('data',main_folder,folder,name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print("Cannot load image:", fullname)
        raise SystemExit
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

def load_sound(name):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer:
        return NoneSound()
    fullname = os.path.join('data','sounds',name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error as message:
        print("Cannot load sound:", name)
        raise(SystemExit, message)
    return sound

def load_tileset(width,height,tx,ty):
    fullname = os.path.join('data','maps','Tileset.png')
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print("Cannot load tileset.")
        raise SystemExit
    image = image.convert()
    rect = (tx*width,ty*height,width,height)
    return image.subsurface(rect)



