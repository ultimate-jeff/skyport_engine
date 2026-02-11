"""
made by : Matthew R and William L

////////////////////////////
-----welcome to skyport-----
////////////////////////////

    the purpos of skyport is to:
provide a simpler way to make a 2d game with pygame without having to learn how to use pygame itself.

engine classes:
- Display_manager: main display manager class
- Delta_timer: delta time couculator
- Util: utility functions
- Layar_manager: manager for multiple layers (cameras)
- Camera: layer (camera) class
- r_obj: renderable object class
- Loader: asset loader class
- loger: logging utility
- Sprite: animated texture class

"""



"""
class Util: this class is just for utilaty methods and theses are the methods it has
    disp_text(text, font, color, x, y,display): this method displays text (u need a pygame font),
    output_print_data(): this prints evrything in the print que,
    print(string): this puts a string in the print que,
    get_angle_and_dist(self,x1,y1,x,y): this rets the angle and dist (in that order) between 2 points,
    color_swap(self,surface: 'pygame.Surface', old_color: tuple, new_color: tuple) -> 'pygame.Surface': this method swaps evry
        instance of on ecolor on a pygame surf with a nuther,
    pryoraty(self,a=None,b=None): this will alwas return a if there is an a i know aaaaaaaa thats scary,
    sort_objects_by_attr(self,obj_list : list, attr_name : str, reverse=False): this sorts a list of objs by an attar,

class Loader: this class is responsable for file management of all pygame suported images adio and json files
    load_texture_map(self,map_path): this you pass in a path to a texture map and it loades it,
    load_sound_map(self,map_path): this you pass in a path to a sound map and it loades it,
    load_file_map(self,map_path): this you pass in a path to a file map and it loades it,
    NOTE: the next 3 methods all return stuff loaded and prechashed by pygame and json loaders,
    image(path): this returns the image at the path,
    data(path): this returns the json at the path,
    sound(path): this returns the sound at the path,
    warp_image(self,image,sizex,sizey,angle): this returns your image exept warped to the specifacations,
    rotate_image(self,image,angle): this rotates your image,
    scale_image(self,image,sizex,sizey): this scales your image ,
    play_sound(self,file_path, volume=0.5,loops=0): this actualy plays a sound

class Delta_timer: this class gets the dt
    def get_dt(): this returns the delta time
"""

import os
import sys  
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
   sys.path.insert(0, BASE_DIR)

#from rendering_eng import *
#from global_utils import *
#from assets.layar_manager import *

from .rendering_eng import Display_manager

from .global_utils import (
    Delta_timer, Util, Loader, r_obj, Sprite,util,loger
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

from .assets.layar_manager import Layar_manager
from .assets.layar_manager import Camera
from .gf_map_cunstructor import gen_map