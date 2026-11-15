"""
made by : Matthew R and William L

////////////////////////////
-----welcome to skyport-----
////////////////////////////



"""

REZ_VGA = (640,480)
REZ_SVGA = (800,600)

REZ_360p = (480,360)
REZ_480p = (720,480)
REZ_576p = (720,576)

REZ_720p = (1280,720)
REZ_1080p = (1920,1080)
REZ_1440p = (2560,1440)
REZ_UWFHD = (2560,1080)
REZ_4K = (3840,2160)
REZ_DCI_4K = (4096,2160)
REZ_5K = (5120,2880)
REZ_8K = (7680,4320)

__version__ = "0.3.0"

from .imports import pygame
from . import imports

from .global_utils import (
    Loader,
    logger,
    Delta_timer,
    Save_file,
    Load_file,
    Class_Data,
    Interacotr
)

from .main import (
    Display_Manager,
    Render,
    Layer,
    Chunk,
    Chunked_Layer,
    Font_Render,
    Camera,
    Animated_Render,
    Interactor_Render,
    Interactor_Layer,
)

from .modules import (
    decorators,
    hitbox,
    util
)

from .modules.hitbox import (
    Hitbox
)



def _set_recursion_depth(depth=1500):
    from global_utils import sys
    sys.setrecursionlimit(depth) 

def quit():
    pygame.quit()


