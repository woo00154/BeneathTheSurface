from pygame.locals import *


class Camera(object):
    def __init__(self, w, h):
        
        self.state = Rect(0,0,w,h)
        self.w = w
        self.h = h
    
    def apply(self,target):
        return target.rect.move(self.state.topleft)
    
    def update(self,target):
        
        self.state = self.complex_camera(target.rect)
        
    def complex_camera(self,target_rect):
        camera = self.state
        l,t, _, _ = target_rect
        _, _, w, h = camera
        l, t, _, _ = -l+self.w/2, -t + self.h/2, w, h
        
        l = min(0,l)
        l = max(-(self.map_w-camera.w),l)
        t = max(-(self.map_h-camera.h),t)
        t = min(0,t)
    
        
        return Rect(l, t, w, h)