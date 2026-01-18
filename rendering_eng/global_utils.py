import numpy as np
import pygame
import math
import copy
import random
import time
import json

class Loader:
    loader_instanses = 0
    def __init__(self,texture_map_path,GF_map_path,sound_map_path=None,loader_name=None,error_img=None,error_sound=None):
        self.texture_map = {}
        self.file_map = {}
        self.sound_map = {}
        self.load_texture_map(texture_map_path)
        self.load_file_map(GF_map_path)
        # loader naming for debuging
        self.error_assets = {"img":error_img,"sound":error_sound}
        Loader.loader_instanses += 1
        self.loader_name = util.pryoraty(loader_name,str(Loader.loader_instanses))
        print(f"{prin_BLUE}++| inisalized Loader instans '{self.loader_name}' |++{prin_RESET}")

    def _error(self,Type,error,path):
        print(f"{prin_RED}!!-error loading {Type} : {path} ->> in loader {self.loader_name} with error >> {error} -!!{prin_RESET}")

    def _loade_img_catagory(self,val):
        paths = val["value"]
        images = []
        for path in paths:
            images.append(pygame.image.load(path).convert_alpha())
        val["value"] = images
        return val
    def init_comon_textures(self,texture_map):
        all_keys = texture_map.keys()
        TM = texture_map
        for key in all_keys:
            val = TM[key]
            Type = val["type"].lower()
            if Type == "d" or Type == "defalt":
                val["value"] = pygame.image.load(key).convert_alpha()
                TM[key] = val
            elif Type == "r" or Type == "replace":
                val["value"] = pygame.image.load(val["value"]).convert_alpha()
                TM[key] = val
            elif Type == "c" or Type == "catagory":
                val = self._loade_img_catagory(val)
            else:
                val["value"] = pygame.image.load(key).convert_alpha()
                TM[key] = val
        return TM
    def load_texture_map(self,map_path):
        with open(map_path,"r") as file:
            texture_map = json.load(file)
        self.texture_map = self.init_comon_textures(texture_map)


    def _loade_file_catagory(self,val):
        paths = val["value"]
        files = []
        for path in paths:
            with open(path,"r") as file:
                files.append(json.load(file))
        val["value"] = files
        return val
    def init_game_files(self,file_map):
        all_keys = file_map.keys()
        TM = file_map
        for key in all_keys:
            val = TM[key]
            Type = val["type"].lower()
            if Type == "d" or Type == "defalt":
                with open(key,"r") as file:
                    val["value"] = json.load(file)
                TM[key] = val
            elif Type == "r" or Type == "replace":
                with open(val["value"],"r") as file:
                    val["value"] = json.load(file)
                TM[key] = val
            elif Type == "c" or Type == "catagory":
                val = self._loade_file_catagory(val)
            else:
                with open(key,"r") as file:
                    val["value"] = json.load(file)
                TM[key] = val
        return TM
    def load_file_map(self,map_path):
        with open(map_path,"r") as file:
            file_map = json.load(file)
        self.file_map = self.init_game_files(file_map)


    def _loade_sound_catagory(self,val):
        file_paths = val["value"]
        sounds = []
        for file_path in file_paths:
            sounds.append(pygame.mixer.Sound(file_path))
        val["value"] = sounds
        return val
    def init_sound_map(self,sound_map):
        all_keys = sound_map.keys()
        TM = sound_map
        for key in all_keys:
            val = TM[key]
            Type = val["type"].lower()
            if Type == "d" or Type == "defalt":
                val["value"] = pygame.mixer.Sound(key)
                TM[key] = val
            elif Type == "r" or Type == "replace":
                val["value"] = pygame.mixer.Sound(val["value"])
                TM[key] = val
            elif Type == "c" or Type == "catagory":
                val = self._loade_sound_catagory(val)
            else:
                val["value"] = pygame.mixer.Sound(key)
                TM[key] = val
        return TM
    def load_sound_map(self,map_path):
        with open(map_path,"r") as file:
            sound_map = json.load(file)
        self.sound_map = self.init_sound_map(sound_map)

    def image(self,path):
        try:
            return self.texture_map[path]["value"]
        except KeyError:
            return pygame.image.load(path).convert_alpha()
        except Exception as e:
            self._error("image",e,path)
            return self.error_assets["img"]
    def data(self,file_path):
        try:
            return self.file_map[file_path]["value"]
        except KeyError:
            with open(file_path,"r") as file:
                return json.load(file)
        except Exception as e:
            self._error("data",e,file_path)
            return -1
    def sound(self,file_path):
        try:
            return self.sound_map[file_path]["value"]
        except KeyError:
            return pygame.mixer.Sound(file_path)
        except Exception as e:
            self._error("sound",e,file_path)
            return self.error_assets["sound"]

    def warp_image(self,image,sizex,sizey,angle):
        image1 = pygame.transform.scale(image,(sizex,sizey))
        image2 = pygame.transform.rotate(image1,angle)
        return image2
    def rotate_image(self,image,angle):
        image2 = pygame.transform.rotate(image,angle)
        return image2
    def scale_image(self,image,sizex,sizey):
        image1 = pygame.transform.scale(image,(sizex,sizey))
        return image1

    def play_sound(self,file_path, volume=0.5,loops=1):
        try:
            sound = self.sound(file_path)
            sound.set_volume(volume)
            sound.play(loops)
            return 1
        except Exception as e:
            print(f" error >> loader ")
            sound = pygame.mixer.Sound(file_path)
            sound.set_volume(volume)
            sound.play(loops)
            return -1
        except KeyError:
            self._error("sound","KeyError",file_path)
            return -1

class Util:
    def __init__(self):
        pass

    def get_angle_and_dist(self,x1,y1,x,y):
        dx = x1 - x
        dy = y1 - y
        dist = math.hypot(dx, dy)
        angle = (math.degrees(math.atan2(dy, dx)) + 180) % 360
        return angle,dist

    def color_swap(self,surface: pygame.Surface, old_color: tuple, new_color: tuple) -> pygame.Surface:
        arr_rgb = pygame.surfarray.array3d(surface)
        arr_alpha = pygame.surfarray.array_alpha(surface)
        mask = np.all(arr_rgb == old_color, axis=-1)
        arr_rgb[mask] = new_color
        new_surface = pygame.Surface(surface.get_size(), pygame.SRCALPHA, 32)
        new_surface = new_surface.convert_alpha()
        pygame.surfarray.blit_array(new_surface, arr_rgb)
        pygame.surfarray.pixels_alpha(new_surface)[:] = arr_alpha
        return new_surface

    def pryoraty(self,a=None,b=None):
        if a != None:
            return a
        else:
            return b

    def sort_objects_by_attr(self,obj_list, attr_name, reverse=False):
        return sorted(obj_list, key=lambda x: getattr(x, attr_name), reverse=reverse)

prin_RED = '\033[91m'
prin_GREEN = '\033[92m'
prin_BLUE = '\033[94m'
prin_RESET = '\033[0m'
util = Util()
loader = Loader(
    "assets/loader/texture_maps/engine_textures.json",
    "assets/loader/game_file_maps/engine_assets.json",
    "assets/loader/sound_maps/engine_sounds.json",
    loader_name="engine_loader",
    error_img=pygame.image.load("assets/images/error.png"),
    error_sound=None
)

class r_obj:
    instanses = 0
    loader = loader
    def __init__(self,x,y,sx,sy,angle,zoom,texture_fp=None,render_type="chunk"):
        self.x,self.y,self.sx,self.sy = x,y,sx,sy
        self.angle = angle
        self.last_zoom = None
        self.last_angle = None
        self.texture_path = texture_fp
        self.render_type = render_type
        self.OG_IMAGE = self.get_df_img(texture_fp)
        self.surf = self.render(zoom)
        r_obj.instanses += 1
        self.id = r_obj.instanses

    def get_df_img(self,fp):
        if fp == None:
            return loader.image("assets/images/None.png")
        return self.image(fp)

    def image(self,fp):
        return r_obj.loader.image(fp)
    def file(self,fp):
        return r_obj.loader.data(fp)

    def should_scale(self,zoom):
        if self.last_zoom != zoom:
            self.last_zoom = zoom
            return True
        return False

    def should_rotate(self,angle):
        if angle != self.last_angle:
            self.last_angle = angle
            return True
        return False

    def render(self,zoom):
        if self.should_scale(zoom):
            self.surf = pygame.transform.scale(self.OG_IMAGE,(self.sx * zoom , self.sy * zoom))
        if self.should_rotate(self.angle):
            self.surf = pygame.transform.rotate(self.surf,self.angle)
        return self.surf

    def get_surf(self,zoom):
        return self.render(zoom)





