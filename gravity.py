

class Gravity:
    
    def __init__(self,magnitude = 9.8):
        self.magnitude = magnitude
        self.limit = 15
        
    def set_mag(self,mag):
        self.magnitude = mag
        
    def get_mag(self):
        return self.magnitude
                  
    def apply(self,target):
        #this must be placed in a loop to work
        if target.yvel <= self.limit:
            target.yvel += self.magnitude/5
        else:
            target.yvel = self.limit
        