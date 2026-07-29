from .global_utils import (
    pygame,
    math,
    time,
    random
)

class Sound():
    def __init__(self,x:"int",y:"int",sound:"pygame.Sound",base_volume:"int"=1,loops:"int"=0,min_dist:"int"=1,max_dist:"int"=9999999999):
        self.x,self.y = x
        self.sound = sound
        self.base_vol = base_volume
        self.loops = loops
        self.min_dist = min_dist
        self.max_dist = max_dist

    def _get_angle_and_dist(self,x1:"int",y1:"int",x:"int",y:"int"):
            """returns the angle and dist between 2 points (it returns that data in that ordor )"""
            dx = x1 - x
            dy = y1 - y
            dist = math.hypot(dx, dy)
            angle = (math.degrees(math.atan2(dy, dx)) + 180) % 360
            return angle,dist

    def _get_vol(self,x,y):
         angle,dist = self._get_angle_and_dist(x,y,self.x,self.y)
         value = (dist - self.min_dist) / (self.max_dist - self.min_dist)
         return self.base_vol * (1- value)

    def play(self,x,y,max_time:"int"=0):
        self._vol = self._get_vol(x,y)
        self.sound.set_volume(self._vol)
        self.sound.play(self.loops,max_time)

class Sound_Engine():

    def __init__(self):
        self.spatial_sounds = [] 