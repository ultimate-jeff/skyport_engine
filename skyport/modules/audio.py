from ..global_utils import (
    pygame,
    Class_Data
)
from ..imports import (
    math
)
class Sound(Class_Data):
    def __init__(self,sound:"pygame.Sound",x,y,max_dist=math.inf,strenth=1.0,base_vol=1):
        super().__init__()
        self.sound = sound
        self.x,self.y = x,y
        self.max_dist = max_dist
        self.base_vol = base_vol
        self.sound_threashold = 0.01
        self.loops = 0
        self.max_time = 0
        self.strenth = strenth

class Sound_Engine(Class_Data):
    def _get_angle_and_dist(self,x1:"int",y1:"int",x:"int",y:"int"):
        """returns the angle and dist between 2 points (it returns that data in that ordor )"""
        dx = x1 - x
        dy = y1 - y
        dist = math.hypot(dx, dy)
        angle = (math.degrees(math.atan2(dy, dx)) + 180) % 360
        return angle,dist

    def __init__(self,x:"int",y:"int",max_dist=math.inf,fade=1):
        super().__init__()
              
              