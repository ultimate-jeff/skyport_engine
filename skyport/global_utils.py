
import inspect
import os
import pathlib as pl
import json
import csv
import tomllib
import threading
import math
import numpy as np
import time
import random

import pygame


pygame.init()

base_dir = pl.Path(__file__).resolve().parent

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


class Class_Data:
    instances = 0
    def __init__(self):
        type(self).instances += 1
        self.id = type(self).instances
    def random_function_that_dose_nuthing(self):  
        random_msgs = (
            "nuthing happend",
            "you didn't miss anything",
            "this function has one job and it's not doing it",
            "congratulations, you called a function",
            "404 purpos of function not found",
            "( ⚆ _ ⚆ )  ...nuthing."
        )
        print(random.choice(random_msgs))

class Loger(Class_Data):
    def __init__(self):
        super().__init__()
        self.sevarity_index = [print_YELLOW,prin_ORANGE,prin_RED,"\033[1;37;41m"]
        self._errors = []
        self._logs = []
        self.tags = {}

    def log(self,msg:"str"):
        self._logs.append(msg)
    def output_print_data(self,include_errors=True):
        print("----- logs -----")
        for msg in self._logs:
            print(msg)
        print("----- errors -----")
        for msg in self._errors:
            print(msg)
        print("---------------")
        self._errors.clear()
        self._logs.clear()
    def error(self,msg:"str",error=None,metadata:"str"="",sevarity_index:"int"=0):
        if error == None:
            self._errors.append(f"{self.sevarity_index[sevarity_index]}!!- error -> {msg} , extra_data -> {metadata} -!!{prin_RESET}")
            if sevarity_index >= 3:
                self.output_print_data()
                exit(1)
            return None     
        else:
            self._errors.append(f"{self.sevarity_index[sevarity_index]}!!- error -> {msg} , extra_data -> {metadata} , python error : {self.error}-!!{prin_RESET}")
            if sevarity_index >= 3:
                self.output_print_data()
                exit(1)
    def has_logs(self):
        return (self._errors != [] and self._logs != [])
                
loger = Loger()


class Util(Class_Data):
    def __init__(self):
        super().__init__()

    def dot_product(self,vec1:"tuple[int,float]",vec2:"tuple[int,float]"):
        """returns the dod product of 2 2d vectors (x,y)"""
        return vec1[0]*vec2[0] + vec1[1]*vec2[1]

    def get_angle_and_dist(self,x1:"int",y1:"int",x:"int",y:"int"):
        """returns the angle and dist between 2 points (it returns that data in that ordor )"""
        dx = x1 - x
        dy = y1 - y
        dist = math.hypot(dx, dy)
        angle = (math.degrees(math.atan2(dy, dx)) + 180) % 360
        return angle,dist
    def pryoraty(self,a=None,b=None):
        """"this will alwas return a if there is an a i know aaaaaaaa thats scary"""
        if a != None:
            return a
        else:
            return b
    def snap_cords_in_bounds(self,x:"int",y:"int",max_x:"int",max_y:"int",min_x:"int"=0,min_y:"int"=0):
        """this snaps a point inside of a rect arya """
        new_x = min(max(x,min_x),max_x-1)
        new_y = min(max(y,min_y),max_y-1)
        return new_x,new_y
    def couculate_dx_dy(self,dist:"int",angle:"float"):
        dx = dist * math.cos(angle)
        dy = dist * math.sin(angle)
        return dx,dy
    def couculate_angle_dist(self,dx:"int",dy:"int"):
        speed = math.sqrt(dx**2 + dy**2)
        angle = math.atan2(dy,dx)
        return angle,speed

    def play_sound(self,soud_obj:"pygame.mixer.Sound", volume=0.5,loops=0):
        try:
            soud_obj.set_volume(volume)
            soud_obj.play(loops)
            return 1
        except Exception as e:
            loger.error("error trying to play sound",e)
    def play_sound_from_point(self,pf,sound_pos:"tuple",listener_pos:"tuple",volume:"float"=0.5,loops:"int"=0,distance_fade:"float"=0.5):
        """this playes a sound from a point"""
        max_vol = volume
        dist = math.hypot(sound_pos[0] - listener_pos[0], sound_pos[1] - listener_pos[1])
        volume *= max(0, 1 - dist / distance_fade)
        self.play_sound(pf, volume, loops)

    def warp_image(self,image:"pygame.Surface",sizex:"int",sizey:"int",angle:"float"):
        image1 = pygame.transform.scale(image,(sizex,sizey))
        image2 = pygame.transform.rotate(image1,angle)
        return image2
    def rotate_image(self,image:"pygame.Surface",angle:"float"):
        image2 = pygame.transform.rotate(image,angle)
        return image2
    def scale_image(self,image:"pygame.Surface",sizex:"int",sizey:"int"):
        image1 = pygame.transform.scale(image,(sizex,sizey))
        return image1

    def color_swap(self,surface: 'pygame.Surface', old_color: tuple, new_color: tuple) -> 'pygame.Surface':
        """returns a surf that every instance of one color is replaced with a nuther"""
        arr_rgb = pygame.surfarray.array3d(surface)
        arr_alpha = pygame.surfarray.array_alpha(surface)
        mask = np.all(arr_rgb == old_color, axis=-1)
        arr_rgb[mask] = new_color
        new_surface = pygame.Surface(surface.get_size(), pygame.SRCALPHA, 32)
        new_surface = new_surface.convert_alpha()
        pygame.surfarray.blit_array(new_surface, arr_rgb)
        pygame.surfarray.pixels_alpha(new_surface)[:] = arr_alpha
        return new_surface

def Load_file(func,mode="r"):
    """this wrapper you pass in a lambda function that takes a file obj and reads the data and returns it"""
    def wrapper(path):
        with open(path,mode) as f:
            data = func(f)
        return data
    return wrapper
def Save_file(func,mode="w"):
    """this wrapper you pass in a lambda that takes in a file obj and the data it wants to save"""
    def wrapper(path,data):
        with open(path,mode) as f:
            func(f,data)
    return wrapper

class Loader(Class_Data):
    error_asset_bace_dir=__file__
    error_asset_map = {}
    _suported_alpha_images = [".png", ".webp", ".svg"]
    _suported_opaque_images = [".jpg", ".jpeg", ".bmp", ".tga", ".gif", ".tiff", ".tif", ".qoi"]
    _suported_audio_formats = [".wav", ".ogg", ".mp3", ".flac", ".mid", ".midi"]
    def _init_supported_types(self):
        for t in Loader._suported_alpha_images:
            self.supported_types[t] = lambda p: pygame.image.load(p).convert_alpha()
        for t in Loader._suported_opaque_images:
            self.supported_types[t] = lambda p: pygame.image.load(p).convert()
        for t in Loader._suported_audio_formats:
            self.supported_types[t] = pygame.mixer.Sound
    def init():
        loader = Loader(Loader.error_asset_bace_dir)
        Loader.error_asset_map["image"] = loader.read("assets/images/error.png")
        Loader.error_asset_map["sound"] = loader.read("assets/sounds/errpr.mp3")
        Loader.error_asset_map["data"] = loader.read("assets/data/error.json")

    def __init__(self,dunder_file=None):
        super().__init__()
        if(dunder_file == None):
            call_frame = inspect.stack()[1]
            dunder_file = call_frame.filename
        self.base_dir = pl.Path(dunder_file).resolve().parent
        self.tags = {}
        self._map = {}
        self._error_assets = {}
        self.supported_types = {
            ".txt": Load_file(lambda f: f.read()),
            ".json": Load_file(json.load),
            ".csv": Load_file(lambda f: list(csv.reader(f))),
            ".bin":  Load_file(lambda f: f.read(),"rb"),
            ".toml": Load_file(lambda f: tomllib.load(f))
        } # unknow types will be read as a bynary 
        self.unsupported_handler = None
        self.supported_savers = {
            ".png": lambda p, d: pygame.image.save(d, p),
            ".jpg": lambda p, d: pygame.image.save(d, p),
            ".jpeg": lambda p, d: pygame.image.save(d, p),
            ".txt": Save_file(lambda f, d: f.write(str(d))),
            ".json": Save_file(lambda f, d: json.dump(d, f, indent=4)),
            ".csv": self._save_csv,
            ".bin": Save_file(lambda f, d: f.write(d)),
        }
        self._init_supported_types()
    def _save_csv(self, path, data):
        if not isinstance(data, list):
            loger.error(f"CSV saver expected a list of rows, got {type(data)}")
            return
        with open(path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(data)
    def _abs_resolve_path(self,path,bace_dir):
        path = pl.Path(path)
        if(path.is_absolute() ):
            return path.resolve()
        return (base_dir / path).resolve()
    def add_new_file_handler(self,type_extension:str,handler:"examle : lambda p: open(p, "r").read()"):
        self.supported_types[type_extension] = handler
    def add_new_save_file_handler(self,type_extension:str,handler:r"example : lambda p, d: json.dump(d, open(p, 'w'), indent=4)"):
            self.supported_savers[type_extension] = handler
    def get_supported_types(self):
        return self.supported_types.keys()
    def set_unsupported_handler(self,handler=None):
        unsupported_handler = handler
    def resolve_path(self,path:"str"):
        path = pl.Path(path)
        if(path.is_absolute() ):
            return path.resolve()
        return (self.base_dir / path).resolve()
    def create_alias(self,path:"str",alias:"str"):
        data = self._map.get(path)
        if(data != None):
            self._map.pop(path)
            self._map[alias] = data
            return
        loger.error(f"could not create alias to {path} do to {path} not being found in Loader map")
    def get_map(self):
        return self._map
    def set_map(self,mapp):
        self._map = mapp
    def _load_file(self,path):
        path = self.resolve_path(path)
        extension = os.path.splitext(path)[1].lower()
        if extension in self.supported_types:
            loader = self.supported_types[extension]
        else:
            loader = self.unsupported_handler
            if loader is None:
                loger.error(f"unsupported type {extension} while loading {path}, ( returning None )")
                return None
            loger.error(f"unsupported type {extension} for {path}, using fallback handler")
        try:
            return loader(path)
        except Exception as e:
            loger.error(f"error during loading of file {path}, ( returning None )", e)
            return None

    def read(self, path: "str", add_to_map:bool=False,overwrite_map:bool=False):
        if path in self._map and not overwrite_map:
            return self._map[path]
        result = self._load_file(path)
        if add_to_map and result is not None:
            self._map[path] = result
        elif result == None:
            loger.error(f"coild not open file {path} , returning None")
        return result
    def image(self,path:"str",add_to_map:bool=False,overwrite_map:bool=False):
        data = self.read(path,add_to_map,overwrite_map)
        if data == None:
            return Loader.error_asset_map["image"]
    def data(self,path:"str",add_to_map:bool=False,overwrite_map:bool=False):
        data = self.read(path,add_to_map,overwrite_map)
        if data == None:
            return Loader.error_asset_map["data"]
    def sound(self,path:"str",add_to_map:bool=False,overwrite_map:bool=False):
        data = self.read(path,add_to_map,overwrite_map)
        if data == None:
            return Loader.error_asset_map["sound"]

    def _preload_folder_list(self,path:"str",preload_data:dict):
        path_list = preload_data["value"]
        value = []
        if(type(path_list) != list):
            return
        for p in path_list:
            combined_path = (pl.Path(path) / pl.Path(p))
            data = self._load_file(combined_path)
            value.append(data)
        self._map[path] = value
        return value
    def _preload_folder_dict(self,path:"str",preload_data:dict):
        path_list = preload_data["value"]
        value = {}
        if(type(path_list) != dict):
            return
        for name in path_list.keys():
            combined_path = pl.Path(path) / pl.Path(path_list[name])
            data = self._load_file(combined_path)
            value[name] = data
        self._map[path] = value
        return

    def _preload_elm(self,k,data):
        preload_data = data[k]
        preload_type = preload_data["type"]
        if(preload_type == "r" or preload_type == "replace"): # where value == replacement_path
            self.read(path=preload_data["value"],add_to_map=True,overwrite_map=True)
        elif(preload_type == "list"): # where u load an entire folder under 1 name 
            self._preload_folder_list(k,preload_data)
        elif(preload_type == "dict"):
             self._preload_folder_dict(k,preload_data)
        else: # defalt loading of path as the file
            self.read(path=k,add_to_map=True,overwrite_map=True)
    def load_from_map(self,map_path:"str"):
        data = self.read(map_path,False)
        if(type(data) != dict):
            loger.error(f"Loader {self.id} canot load {map_path} as a Loader map (file is not .json)")
            return
        keys = data.keys()
        for k in keys:
            self._preload_elm(k,data) 
        loger.log(f"Loader {self.id} is complete loading map {map_path}")
    def load_map_on_thread(self, map_path: "str"):
        thread = threading.Thread(target=self.load_from_map, args=(map_path,))
        thread.start()
        return thread
    def join_maps(self,map_a,map_b):
        """this method takes one map and adds all the content to the other"""
        for k in map_b.keys():
            item = map_b[k]
            map_a[k] = item
        return map_a
    def save(self,path:"str",data):
        data
        if( data == None ):
            loger.error(f"None is an invalid file content. can't save None to {path}")
            return
        full_path = self.resolve_path(path)
        extension = os.path.splitext(full_path)[1].lower()
        if extension not in self.supported_savers:
            loger.error(f"{extension} is an unsuported format for saving")
            return
        try:
            self.supported_savers[extension](full_path, data)
            loger.log(f"sucsesfully saved map_key data to {path}")
        except Exception as e:
            loger.error(f"error during save of file to path  : {path}",e)

    def save_map(self,path:"str",mapp:dict):
        try:
            with open(self._abs_resolve_path(path,self.base_dir),"w" ) as f:
                json.dump(mapp,f,indent=4)
        except Exception as e:
            loger.error(f"failed to save Loader map to path {path}",e)


class Delta_timer(Class_Data):
    def __init__(self):
        super().__init__()
        # Using perf_counter for highest precision
        self.prev_time = time.perf_counter()
        self.dt = 0.0

    def get_dt(self):
        now = time.perf_counter()
        self.dt = now - self.prev_time
        self.prev_time = now
        return self.dt



class Camera(Class_Data):
    def pryoraty(self,a=None,b=None):
        """"this will alwas return a if there is an a i know aaaaaaaa thats scary"""
        if a != None:
            return a
        else:
            return b
    def __init__(self,display_surface,world_size:"tuple",chunk_size:"int"=500,bg_fill_color:"tuple"=None,layer_name:"str"=None,genorator:"function"=None):
        super().__init__()
        self.display_surface = display_surface
        self.world_size = world_size
        self.bg_fill_color = self.pryoraty(bg_fill_color,(0,0,0,0))
        self.layer_name = self.pryoraty(layer_name,Camra.instances)
        self.chunk_size = chunk_size
        self.x,self.y = 0,0
        self.tiles = {}
        self.zoom = 1.0
        self.old_zoom = self.zoom
        self.WORLD_HIGHT = world_size[0]
        self.WORLD_WIDTH = world_size[1]
        self.CHUNKS_ON_X = self.WORLD_WIDTH // self.chunk_size
        self.CHUNKS_ON_Y = self.WORLD_HIGHT // self.chunk_size
        self.obj_render_surf = pygame.Surface(display_surface.get_size(),flags=pygame.SRCALPHA)
        self.genorator = genorator

    def set_genorator(self,genorator:"function"):
        for chunk in self.tiles:
            chunk.generate_terrain(genorator)
    def set_chunk_update_func(self,func:"function"):
        for chunk in self.tiles:
            chunk.update_gen_script = func

    def _get_min_max_c_pos(self,z,W,H):
        world_left   = -self._offset_x / z
        world_top    = -self._offset_y / z
        world_right  = world_left + W / z
        world_bottom = world_top + H / z

        min_cx = max(0, int(math.floor(world_left / self.chunk_size)))
        max_cx = min(self.CHUNKS_ON_X - 1, int(math.floor(world_right / self.chunk_size)))
        min_cy = max(0, int(math.floor(world_top / self.chunk_size)))
        max_cy = min(self.CHUNKS_ON_Y - 1, int(math.floor(world_bottom / self.chunk_size)))
        return min_cx,min_cy,max_cx,max_cy

    def render(self, target_x, target_y):
        W, H = self.display_surface.get_size()
        z = self.zoom
        self.obj_render_surf.fill((0,0,0,0))
        self._offset_x = -target_x * z + W // 2
        self._offset_y = -target_y * z + H // 2

        min_cx,min_cy,max_cx,max_cy = self._get_min_max_c_pos(z,W,H)

        for cx in range(min_cx, max_cx + 1):
            for cy in range(min_cy, max_cy + 1):
                chunk = self.get_chunk(cx, cy)
                screen_x = cx * self.chunk_size * z + self._offset_x
                screen_y = cy * self.chunk_size * z + self._offset_y
                surf = chunk.scaled_surface(z)
                self.display_surface.blit(surf, (screen_x, screen_y))
                chunk.update(self.zoom,self,screen_x,screen_y)
        self.display_surface.blit(self.obj_render_surf,(0,0))
        return self.display_surface

    def get_chunk_cords(self,x,y):
        cx = int(x) // self.chunk_size
        cy = int(y) // self.chunk_size
        return (cx,cy)

    def get_chunk(self,cx, cy):
        #return chunk at (cx, cy), create if it doesnt exist yet
        if (cx, cy) not in self.tiles:
            self.tiles[(cx, cy)] = Chunk(cx, cy, self.chunk_size,genorator=self.genorator,bg_fill_color=self.bg_fill_color,zoom=self.zoom,cam=self)
            Util.print(f"{prin_GREEN}Created chunk {cx},{cy}{prin_RESET}")
        return self.tiles[(cx, cy)]

    def set_pos(self,x,y):
        self.x = x
        self.y = y

    def get_surf(self):
        return self.display_surface

    def blit(self,surf:"pygame.surface.Surface",x,y):
        rect = surf.get_rect()
        chunks_on_x = math.ceil(rect.width / self.chunk_size)
        chunks_on_y = math.ceil(rect.height / self.chunk_size)
        for Y in range(chunks_on_y):
            for X in range(chunks_on_x):
                Y = (Y * self.chunk_size) + y
                X = (X * self.chunk_size) + y
                cx,cy = self.get_chunk_cords(X,Y)
                chunk = self.get_chunk(cx,cy)
                chunk.blit(surf,x,y)
    def simple__blit(self,surf:"pygame.surface.Surface",x,y):
        self.display_surface.blit(surf,(x,y))
    def simple_chunk_blit(self,surf:"pygame.surface.Surface",x,y):
        cx,cy = self.get_chunk_cords(x,y)
        chunk = self.get_chunk(cx,cy)
        chunk.blit(surf,x,y)
    def scb(self,surf:"pygame.surface.Surface",x,y):
        self.simple_chunk_blit(surf,x,y)
    def simple_fill(self,fill_color):
        self.display_surface.fill(fill_color)
    
    def fill(self,fill_color):
        for cpos in self.tiles.keys():
            self.get_chunk(cpos[0],cpos[1]).set_fill_data(fill_color)
    def chunk_fill(self,cx,cy,fill_color):
        chunk = self.get_chunk(cx,cy)
        chunk.full(fill_color)

    def set_zoom(self, level):
        self.zoom = max(0.1, level)

class Chunk(Class_Data):
    def pryoraty(self,a=None,b=None):
        """"this will alwas return a if there is an a i know aaaaaaaa thats scary"""
        if a != None:
            return a
        else:
            return b

    def __init__(self,cpos:"list",chunk_size:"int",bg_fill_color:"list"=None,genorator:"function"=None,update_function:"function"=None):
        super().__init__()
        self.tags = {}
        self.cpos = cpos
        self.size = chunk_size
        self.surf = pygame.Surface((chunk_size, chunk_size), flags=pygame.SRCALPHA)
        self.bg_color = self.pryoraty(bg_fill_color,(0,0,0,255))
        self.pryoraty(genorator,lambda self : None)(self)
        self._update_func = self.pryoraty(update_function,lambda self : None)
        self._scaled = None
        self._last_zoom = None
        self.all_objs = []

    def scale__(self,zoom):
        w = max(1, int(self.size * zoom))
        h = max(1, int(self.size * zoom))
        self._scaled = pygame.transform.scale(self.surf, (w, h))
        self._last_zoom = zoom

    def scaled_surface(self, zoom):
        if self._last_zoom != zoom or self._scaled is None:
            self.scale__(zoom)
        return self._scaled
    
    def blit(self,surf,x,y):
        self.surf.blit(surf,(x,y))
    def fill(self,fill_color):
        self.surf.fill(fill_color)
    def get_surf(self,zoom=None):
        if zoom == None:
            zoom = self._last_zoom
        return self.scaled_surface(zoom)
    
    def render(self,zoom=1):
        self.fill(self.bg_color)
        self._update_func(self)
