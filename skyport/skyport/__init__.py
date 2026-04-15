"""
made by : Matthew R and William L

////////////////////////////
-----welcome to skyport-----
////////////////////////////

    the purpos of skyport is to:
provide a simpler way to make a 2d game with pygame without having to learn how to use pygame itself.


"""


import os
import sys  
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
   sys.path.insert(0, BASE_DIR)

from .rendering_eng import (Display_manager,GSTI)

from .global_utils import (
    Delta_timer, Util, Loader, r_obj, Sprite,loger,Render
)
from .core.paths import pygame

prin_RED = '\033[91m'
prin_GREEN = '\033[92m'
prin_BLUE = '\033[94m'
prin_RESET = '\033[0m'
print_YELLOW = '\033[33m'
print_MAGENTA = '\033[35m'
print_CYAN = '\033[36m'
prin_ORANGE = '\033[38;5;208m'
prin_PINK = '\033[38;5;206m'
prin_PURPLE = '\033[38;5;129m'
prin_BROWN = '\033[38;5;94m'
prin_GOLD = '\033[38;5;220m'
prin_LIME = '\033[38;5;118m'
prin_TEAL = '\033[38;5;30m'
prin_NAVY = '\033[38;5;18m'
prin_SKY_BLUE = '\033[38;5;117m'
prin_HOT_PINK = '\033[38;5;198m'
prin_MAROON = '\033[38;5;88m'
prin_OLIVE = '\033[38;5;100m'
prin_VIOLET = '\033[38;5;93m'
prin_SALMON = '\033[38;5;209m'
prin_DARK_GREEN = '\033[38;5;22m'

from .assets.layar_manager import Layer_manager
from .assets.layar_manager import Camera 
from .assets.layar_manager import Layar
from .gf_map_cunstructor import gen_map

#from .assets.layar_manager import Camera as Layar
#from .global_utils import r_obj as Render

def init(game_loader):
    r_obj.loader = game_loader
    GSTI.lloader = game_loader