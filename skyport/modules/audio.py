from ..global_utils import (
    pygame,
    Class_Data,
    logger
)
from ..imports import (
    math
)

class Sound(Class_Data):
    def __init__(self,file,pos:"tuple",vol:"float",radios:"float",fade_rate:"float",tags=None):
        self.file = file
        self.pos = pos
        self.vol = vol
        self.radios = radios
        self.fade_rate = fade_rate
        super().__init__(tags)

    def _apply_fade(self,dist:"float"):
        self.vol = 0 # formula 
        return self.vol
    



class Sound_engine():
    def __init__(self):
        pass

        