import random
import time
import json
import numpy as np
import sys
import os
import pyperclip
import copy
import math
import pygame

#firts init
prin_RED = '\033[91m'
prin_GREEN = '\033[92m'
prin_BLUE = '\033[94m'
prin_RESET = '\033[0m'
pygame.init()
runing = True
WORLD_WIDTH = 20000
WORLD_HIGHT = 20000
CHUNK_SIZE = 1000
CHUNKS_ON_X = WORLD_WIDTH // CHUNK_SIZE
CHUNKS_ON_Y = WORLD_HIGHT // CHUNK_SIZE
tiles = {}

text_font = pygame.font.SysFont("Arial", 20)
text_font_big = pygame.font.SysFont("Arial", 50)
text_fonts = (text_font,text_font_big)

vol = 1
camra_zoom = 1
heal_amount = 1
simulation_dist = 2000
Menue = 0
loops = 0
Tfps = 40
window_size = (1500,750)
display_size = (1500,750)


# vital classes ------------------------
class Loader:
    def __init__(self,texture_map_path,GF_map_path):
        self.texture_map = {}
        self.file_map = {}
        self.seed_obj = {}
        self.load_texture_map(texture_map_path)
        self.load_file_map(GF_map_path)
        
    def init_comon_textures(self,texture_map):
        all_keys = texture_map.keys()
        TM = texture_map
        for key in all_keys:
            val = TM[key]
            if isinstance(val,bool):
                val = pygame.image.load(key).convert_alpha()
                TM[key] = val
            elif isinstance(val,str):
                val = pygame.image.load(val).convert_alpha()
                TM[key] = val
            else:
                val = pygame.image.load(key).convert_alpha()
                TM[key] = val
        return TM

    def init_game_files(self,file_map):
        all_keys = file_map.keys()
        TM = file_map
        for key in all_keys:
            val = TM[key]
            if isinstance(val,bool):
                with open(key,"r") as file:
                    val = json.load(file)
                TM[key] = val
            elif isinstance(val,str):
                with open(key,"r") as file:
                    val = json.load(file)
                TM[key] = val
            else:
                with open(key,"r") as file:
                    val = json.load(file)
                TM[key] = val
        return TM

    def load_texture_map(self,map_path):
        with open(map_path,"r") as file:
            texture_map = json.load(file)
        self.texture_map = self.init_comon_textures(texture_map)

    def load_file_map(self,map_path):
        with open(map_path,"r") as file:
            file_map = json.load(file)
        self.file_map = self.init_game_files(file_map)

    def image(self,path):
        try:
            return self.texture_map[path]
        except KeyError:
            return pygame.image.load(path).convert_alpha()

    def data(self,file_path):
        try:
            return self.file_map[file_path]
        except KeyError:
            with open(file_path,"r") as file:
                return json.load(file)

    def warp_image(self,image,sizex,sizey,angle):
        image1 = pygame.transform.scale(image,(sizex,sizey))
        image2 = pygame.transform.rotate(image1,angle)
        return image2

    def play_sound(self,file_path, volume=0.5,loops=0):
        try:
            sound = pygame.Sound(file_path)
            sound.set_volume(volume)
            sound.play(loops)
            return 1
        except Exception as e:
            print(f"{prin_RED}!!-error loading sound ->> {e} -!!{prin_RESET}")
            return -1

def get_chunk(cx, cy):
    #return chunk at (cx, cy), create if it doesnt exist yet
    if (cx, cy) not in tiles:
        tiles[(cx, cy)] = Chunk(cx, cy, CHUNK_SIZE)
        print(f"{prin_GREEN}Created chunk {cx},{cy}{prin_RESET}")
    return tiles[(cx, cy)]

class GameCamera:
    def __init__(self, display_surface, chunk_size):
        self.display_surface = display_surface
        self.chunk_size = chunk_size
        self.offset_x = 0
        self.offset_y = 0
        self.zoom = 1.0

    def set_zoom(self, level):
        self.zoom = max(0.1, level)

    def camera_render(self, target_x, target_y, zoom=1.0):
        self.set_zoom(zoom)
        W, H = self.display_surface.get_size()
        z = self.zoom

        self.offset_x = -target_x * z + W // 2
        self.offset_y = -target_y * z + H // 2

        world_left   = -self.offset_x / z
        world_top    = -self.offset_y / z
        world_right  = world_left + W / z
        world_bottom = world_top + H / z

        min_cx = max(0, int(math.floor(world_left / CHUNK_SIZE)))
        max_cx = min(CHUNKS_ON_X - 1, int(math.floor(world_right / CHUNK_SIZE)))
        min_cy = max(0, int(math.floor(world_top / CHUNK_SIZE)))
        max_cy = min(CHUNKS_ON_Y - 1, int(math.floor(world_bottom / CHUNK_SIZE)))

        for cx in range(min_cx, max_cx + 1):
            for cy in range(min_cy, max_cy + 1):
                chunk = get_chunk(cx, cy)
                surf = chunk.scaled_surface(z)
                screen_x = cx * CHUNK_SIZE * z + self.offset_x
                screen_y = cy * CHUNK_SIZE * z + self.offset_y
                self.display_surface.blit(surf, (screen_x, screen_y))

class Chunk:
    def __init__(self, cx, cy, chunk_size):
        self.cx = cx
        self.cy = cy
        self.size = chunk_size
        self.surf = pygame.Surface((chunk_size, chunk_size), flags=pygame.SRCALPHA)
        self.surf.blit(defalt_image, (0,0))
        self._scaled = None
        self._last_zoom = None
        self.all_particals = []
        self.all_props = []
        self.all_planes = []
        self.all_wepons = []
        self.generate_terrain()

    def scaled_surface(self, zoom):
        if self._last_zoom != zoom or self._scaled is None:
            w = max(1, int(self.size * zoom))
            h = max(1, int(self.size * zoom))
            self._scaled = pygame.transform.scale(self.surf, (w, h))
            self._last_zoom = zoom
        return self._scaled

    def generate_terrain(self):
        pass


#utilaty funcs
class Util:
    def __init__(self):
        pass
    def get_mouse_pos(self):
        global mouse_pos
        mx, my = pygame.mouse.get_pos()
        mouse_pos = (((mx - W_pos[0]) / scale),((my - W_pos[1]) / scale))

    def clock(self,Tfps):
        global loops ,s_display
        loops += 1
        s_display = pygame.transform.smoothscale(display, new_size)
        window.blit(s_display,W_pos)
        print(f"loops are at {loops}")
        pygame.display.flip()
        clock.tick(Tfps)

    def get_angle_and_dist(self,x1,y1,x,y):
        dx = x1 - x
        dy = y1 - y
        dist = math.hypot(dx, dy)
        angle = (math.degrees(math.atan2(dy, dx)) + 180) % 360
        return angle,dist

    def disp_text(self,text, font, color, x, y):
        img = font.render(text, True, color)
        rect = img.get_rect(center=(x, y))
        display.blit(img, rect)
        return rect

    def rand_cords(self,obj):
        global WORLD_HIGHT,WORLD_WIDTH,simulation_dist
        rand_x = random.randint(int(max(0, obj.x - simulation_dist)),int(min(WORLD_WIDTH, obj.x + simulation_dist)))
        rand_y = random.randint(int(max(0, obj.y - simulation_dist)),int(min(WORLD_HIGHT, obj.y + simulation_dist)))
        return rand_x,rand_y

    def update_objs(self,objs):
        for p in objs:
            p.update()

    def get_cx_cy(self,x, y):
        cx = math.floor(x / CHUNK_SIZE)
        cy = math.floor(y / CHUNK_SIZE)
        return cx, cy

    def get_chunks_in_dist(self,cx, cy, dist, circle=True):
        """
        Returns a list of chunk coordinates (x, y) within a given distance.
        Distance is measured in chunk units.
        If circle=True, returns circular radius; otherwise square region.
        """
        results = []
        for dx in range(-dist, dist + 1):
            for dy in range(-dist, dist + 1):
                tx = cx + dx
                ty = cy + dy
                # optional bounds checking if your world has limits
                if tx < 0 or ty < 0 or tx >= CHUNKS_ON_X or ty >= CHUNKS_ON_Y:
                    continue
                if circle:
                    # circular radius check
                    if dx*dx + dy*dy <= dist*dist:
                        results.append((tx, ty))
                else:
                    # square radius
                    results.append((tx, ty))
        return results

class Updator:
    def __init__(self):
        self.all_planes = []
        self.all_xp = []
        self.all_bullets = []
        self.simulation_dist = 2000

    def update_B(self,all_B):
        global simulation_dist
        for bullet in all_B:
            if bullet.dist <= simulation_dist:
                bullet.update(display,camra)
            else:
                bullet.life_time -= 3

    def update_plane(self,all_planes):
        for p in all_planes:
            p.ai_blit(display,camra)
            p.collect_xp()
            p.update_bullets(self.all_bullets)
            if p.health <= 0:
                self.all_planes.remove(p)
                p.drop_xp()
                del p

    def manage_xp(self):
        if len(self.all_xp) <= len(self.all_planes)*settings_data["xpp"]:
            rx,ry = util.rand_cords(player1)
            Xp = Parical(random.choice(("xp","xp","xp")),rx,ry,direction=random.randint(0,360),speed=6)
            Xp.update(display,camra)
            self.all_xp.append(Xp)
        is_mogo_four = loops % 4 == 1
        for xp in self.all_xp:
            if is_mogo_four:
                xp.update_player_dist()
            if xp.player_dist <= self.imulation_dist:
                xp.update(display,camra)
                if xp.life_time != "None" and xp.life_time <= 0:
                    self.all_xp.remove(xp)
                    del xp
            else:
                if xp.owner != "land_form":
                    self.all_xp.remove(xp)
                    del xp

# main classes -------------------
class Prop:
    def __init__(self,PT,x,y,direction=0,speed=0,acselaration=0.5,user_name=None,SX=None,SY=None):
        self.PT = PT
        self.x = x
        self.y = y 
        self.dx = 0
        self.dy = 0
        self.speed = speed
        self.accselaration = acselaration
        self.name = user_name
        self.data = loader.data(f"props/{PT}.json")
        self.sx = self.data["sizex"]
        self.sy = self.data["sizey"]
        self.angle = self.data["angle"]
        self.colidable = self.data["colidable"]

        if SX != None and SY != None:
            self.xs = SX
            self.sy = SY
        if direction != None:
            self.angle = direction
        self.rect = pygame.Rect(self.x,self.y,self.sx,self.sy)
        self.og_image = loader.image(f"props/{PT}.png")
        self.image = loader.warp_image(self.og_image,self.sx,self.sy,self.angle)
    
    def update(self):
        display.blit(self.image,((self.x+camra.offset_x),(self.y+camra.offset_y)))

class Parical():
    def __init__(self,PT,x,y,direction=0,speed=0,acselaration=0.5,user_name=None,SX=None,SY=None):
        self.PT = PT
        self.x = x
        self.y = y 
        self.dx = 0
        self.dy = 0
        self.angle = direction
        self.speed = speed
        self.accselaration = acselaration
        self.name = user_name
        self.data = loader.data(f"Paricals/stats/{PT}.json")
        self.sx = self.data["sizex"]
        self.sy = self.data["sizey"]
        self.update_stager = random.randint(0,Tfps)

        if SX != None and SY != None:
            self.xs = SX
            self.sy = SY
        self.og_image = loader.image(f"Paricals/{PT}.png")
        self.image = loader.warp_image(self.og_image,self.sx,self.sy,self.angle)

    def re_couculate_dx_dy(self):
        if self.speed > 0:
            self.speed -= self.accselaration
            rad = math.radians(self.angle)
            self.dx = -self.speed * math.sin(rad)
            self.dy = -self.speed * math.cos(rad)
        elif self.speed < 0:
            self.speed += self.accselaration
            rad = math.radians(self.angle)
            self.dx = -self.speed * math.sin(rad)
            self.dy = -self.speed * math.cos(rad)
        if abs(self.speed) < self.accselaration:
            self.speed = 0

    def colect(self):
        if self.data["colect_sound"] != "":
            sucses = loader.play_sound(self.data["colect_sound"])
            if sucses == -1:
                pygame.draw.rect(display,(100,0,0),(self.x,self.y,self.sx,self.sy),border_radius=5)
    def place(self):
        if self.data["place_sound"] != "":
            sucses = loader.play_sound(self.data["place_sound"])
            if sucses == -1:
                pygame.draw.rect(display,(100,0,0),(self.x,self.y,self.sx,self.sy),border_radius=5)
    
    def update(self):
        self.x += self.dx
        self.y += self.dy
        if loops % self.data["adjust_speed"] == self.update_stager:
            self.re_couculate_dx_dy()
        display.blit(self.image,((self.x+camra.offset_x),(self.y+camra.offset_y)))
        
class Wepons():
    def __init__(self,WT,x,y,direction,user_name,NW_OW="server"):
        self.NW_OW = NW_OW
        self.WT = WT
        self.x = x
        self.y = y
        self.angle = direction
        data = loader.data(f"wepons/wepon_stats/{WT}.json")
        self.data = data
        self.speed = data['speed']
        self.damage = data['damage']
        self.sizex = data['sizex']
        self.sizey = data['sizey']
        self.life_time = data['life_time']
        self.fire_sound = data['fire_sound']
        self.hit_sound = data['hit_sound']
        if self.data['extra_BC'] >= 1:
            self.life_time += random.randint(0,self.data['extra_BLT']*self.data['extra_BC'])
        rad = math.radians(direction)
        delta_x = -self.speed * math.sin(rad)
        delta_y = -self.speed * math.cos(rad)
        self.x += delta_x
        self.y += delta_y
        self.dx = delta_x
        self.dy = delta_y
        self.Roriginal_image = loader.image(f"wepons/{WT}.png")
        self.image = pygame.transform.scale(self.Roriginal_image,(self.sizex,self.sizey))
        self.original_image = pygame.transform.scale(self.Roriginal_image,(self.sizex,self.sizey))
        self.original_image = pygame.transform.rotate(self.original_image, direction)
        self.rect = self.image.get_rect(center=(500, 350))
        self.owner = user_name
        self.screen_rect = self.rect
        self.dist = 0
        self.scaled_width = int(self.original_image.get_width() * camra.zoom)
        self.scaled_height = int(self.original_image.get_height() * camra.zoom)

        self.has_ai = False
        self.turn_speed = 0
        self.target = None
        self.rect.center = (self.x, self.y)

    def update_player_dist(self):
        global player1
        dx = self.x - player1.x
        dy = self.y - player1.y
        self.dist = math.hypot(dx, dy)

    def update(self, display_surface, camera_obj):
        self.x += self.dx
        self.y += self.dy
        self.life_time -= 1
        if loops % 5 == 1:
            self.update_player_dist()
        #screen_rect = self.original_image.get_rect(center=(self.x + camera_obj.offset_x, self.y + camera_obj.offset_y))
        display_surface.blit(self.original_image, self.original_image.get_rect(center=(self.x + camera_obj.offset_x, self.y + camera_obj.offset_y)))
        return 0 #screen_rect

    def scater(self):
        global all_bullets,display,camra
        BT = self.data["extra_BT"]
        BC = self.data["extra_BC"]
        for B in range((BC)):
            bullet = Wepons(BT,self.x,self.y,random.randint(0,360),self.owner)
            bullet.life_time = self.data['extra_BLT']
            all_bullets.append(bullet)
          
    def fire(self):
        #global vol
        max_vol = vol + 1
        max_dist = 2000
        clamped_dist = min(self.dist, max_dist)
        volume_factor = 1.0 - (clamped_dist / max_dist)
        calculated_volume = max_vol * volume_factor
        final_volume = max(0.0, min(max_vol, calculated_volume))
        sound = pygame.mixer.Sound((f"sounds/{self.fire_sound}.mp3"))
        sound.set_volume(final_volume)
        sound.play()

    def hit(self):
        dx = self.x - player1.x
        dy = self.y - player1.y
        self.dist = math.hypot(dx, dy)
        max_vol = vol + 0.3
        max_dist = 1000
        clamped_dist = min(self.dist, max_dist)
        volume_factor = 1.0 - (clamped_dist / max_dist)
        calculated_volume = max_vol * volume_factor
        final_volume = max(0.0, min(max_vol, calculated_volume))
        sound = pygame.mixer.Sound((f"sounds/{self.hit_sound}.mp3"))
        sound.set_volume(final_volume)
        sound.play()

class Plane():
    def __init__(self,user_name,PT,NW_OW="server"):
        global all_bullets,player1,WORLD_HIGHT,WORLD_WIDTH
        self.NW_OW = NW_OW
        self.user_name = user_name
        self.angle = 0
        self.speed = 1
        self.x = random.randint(100,WORLD_WIDTH-100)
        self.y = random.randint(100,WORLD_HIGHT-100)
        self.PT = PT
        try:
            data = loader.data(f"planes/stats/{PT}.json")
        except Exception:
            print(f"could not load planes/stats/{PT}.json")
            sys.exit()
        self.data = data
        self.acceleration = data['acceleration']
        self.armor = data['armor']
        self.fire_speed = data['fire_speed']
        self.max_health = data['health']
        self.health = self.max_health
        self.reload_speed = data['reload_speed']
        self.sizex = data['sizex']
        self.sizey = data['sizey']
        self.HB_sizex = data['HB_sizex']
        self.HB_sizey = data['HB_sizey']
        self.top_speed = data['top_speed']
        self.min_speed = data['min_speed']
        self.turn_speed = data['turn_speed']
        self.wepons = data['wepons']
        self.wepon = self.wepons[0]
        self.wepon_amounts = data['wepon_amounts']
        self.xp_value = data['xp_value']
        self.curent_leval = data['leval']
        self.value = data['plane_value']
        self.turbulance = 0
        self.curent_pow = []
        self.pow_duration = 0
        self.curent_pow_duration = 0
        self.C_amo = self.wepon_amounts[0]
        self.original_image = loader.image(f"planes/{PT}.png")
        self.image = pygame.transform.scale(self.original_image,(self.sizex,self.sizey))
        self.original_image = pygame.transform.scale(self.original_image,(self.sizex,self.sizey))
        self.Rect = self.image.get_rect(center=(center_x, center_y))
        self.screen_rect = self.Rect
        self.num = 0
        self.xp = 0
        self.fired = 0
        self.coliding_planes = 0
        self.death_cause = ["None",""]
        self.hitbox = pygame.rect.Rect(self.x,self.y,self.HB_sizex,self.HB_sizey)

    def respawn(self,PT,op_data=None):
        self.PT = PT
        if op_data == None:
            data = loader.data(f"planes/stats/{PT}.json")
        else:
            data = op_data
        self.acceleration = data['acceleration']
        self.armor = data['armor']
        self.fire_speed = data['fire_speed']
        self.max_health = data['health']
        self.health = self.max_health
        self.reload_speed = data['reload_speed']
        self.sizex = data['sizex']
        self.sizey = data['sizey']
        self.HB_sizex = data['HB_sizex']
        self.HB_sizey = data['HB_sizey']
        self.top_speed = data['top_speed']
        self.min_speed = data['min_speed']
        self.turn_speed = data['turn_speed']
        self.wepons = data['wepons']
        if self.wepons != []:
            self.wepon = self.wepons[0]
        self.wepon_amounts = data['wepon_amounts']
        self.xp_value = data['xp_value']
        self.curent_leval = data['leval']
        if self.wepon_amounts != []:
            self.C_amo = self.wepon_amounts[0]
        self.original_image = loader.image(f"planes/{PT}.png")
        self.image = pygame.transform.scale(self.original_image,(self.sizex,self.sizey))
        self.original_image = pygame.transform.scale(self.original_image,(self.sizex,self.sizey))
        self.Rect = self.image.get_rect(center=(center_x, center_y))
        self.data = data
        self.coliding_planes = 0
        self.death_cause = ["None",""]
        self.hitbox = pygame.rect.Rect(self.x,self.y,self.HB_sizex,self.HB_sizey)

    def add_pows(self,Pow):
        self.acceleration += Pow['acceleration_give']
        self.armor += Pow['armor_give']
        self.fire_speed += Pow['fire_speed_give']
        self.max_health += Pow['health_give']
        self.health += Pow['health_give']
        self.reload_speed += Pow['reload_speed_give']
        self.sizex += Pow['sizex_give']
        self.sizey += Pow['sizey_give']
        self.top_speed += Pow['top_speed_give']
        self.min_speed += Pow['min_speed_give']
        self.turn_speed += Pow['turn_speed_give']
        self.turbulance += Pow['tubulance_give']
        self.angle += Pow['angle_give']
        self.x += Pow['x_give']
        self.y += Pow['y_give']
        self.speed += Pow['speed_give']
        if Pow['wepons_give'] != []:
            self.wepon_amounts.append(Pow['wepon_amounts_give'])
            self.wepons.append(Pow['wepons_give'])

    def remove_pows(self,Pow):
        self.acceleration -= Pow['acceleration_give']
        self.armor -= Pow['armor_give']
        self.fire_speed -= Pow['fire_speed_give']
        self.max_health -= Pow['health_give']
        self.health -= Pow['health_give']
        self.reload_speed -= Pow['reload_speed_give']
        self.sizex -= Pow['sizex_give']
        self.sizey -= Pow['sizey_give']
        self.top_speed -= Pow['top_speed_give']
        self.min_speed -= Pow['min_speed_give']
        self.turn_speed -= Pow['turn_speed_give']
        self.turbulance -= Pow['tubulance_give']
        if Pow['wepons_give'] in self.wepons:
            index = self.wepons.index(Pow['wepons_give'])
            del self.wepons[index]
            del self.wepon_amounts[index]
            if self.num == index:
                if len(self.wepons) >= 1:
                    self.num = 0
                    self.wepon = self.wepons[0]
                    self.C_amo = self.wepon_amounts[0]
                else:
                    self.wepon = "pNone"
                    self.C_amo = 0
                    self.num = 0
            elif self.num > index:
                self.num -= 1

    def manage_pows(self):
        for Pow in self.curent_pow:
            if Pow['duration_give'] != "one_time" and Pow['duration_give'] <= 0:
                self.remove_pows(Pow)
                self.curent_pow.remove(Pow)
            if Pow['duration_give'] != "one_time":
                Pow['duration_give'] -= 1

    def to_dict(self):
        return {
            "id": self.user_name,
            "x": round(self.x, 2),
            "y": round(self.y, 2),
            "ang": round(self.angle, 2),
            "H": int(self.health),
            "PT": self.PT,
            "o": self.NW_OW
        }

    def rotate(self):
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.Rect = self.image.get_rect(center=(center_x, center_y))

    def apliey_tubulance(self):
        if self.turbulance > 0:
            self.x += random.randint(-self.turbulance, self.turbulance)
            self.y += random.randint(-self.turbulance, self.turbulance)

    def blit(self):
        global camra_zoom
        if not self.health <= 0:
            display.blit(self.image, self.Rect.topleft)
        else:
            camra.camera_render(self.x, self.y,camra_zoom)
            return True
        rec = util.disp_text(self.user_name,text_font,(0,10,0),self.Rect.centerx,self.Rect.y -30)
        pygame.draw.rect(display,(0,100,0),(center_x-self.health/2,rec.y+30,self.health,10),border_radius=3)

    def drop_xp(self):
        global all_xp
        for i in range(self.data["death_xp_amount"]):
            XP = Parical(random.choice(self.data["death_xp"]),self.x+random.randint(0,self.sizex),self.y+random.randint(0,self.sizey),direction=random.randint(0,360),speed=self.data["death_xp_speed"],user_name=self.user_name,acselaration=self.data["death_xp_accselaration"])
            XP.update(display,camra)
            all_xp.append(XP)

    def move(self):
        self.hitbox = pygame.rect.Rect(self.x,self.y,self.HB_sizex,self.HB_sizey)
        self.apliey_tubulance()
        amount = self.speed
        direction = self.angle
        rad = math.radians(direction)
        delta_x = -amount * math.sin(rad)
        delta_y = -amount * math.cos(rad)
        self.x += delta_x
        self.y += delta_y
        
    def wep(self,num):
        if num != None:
            num -= 1
            WL = len(self.wepons)
            num = (num % WL)
            self.wepon = self.wepons[num]
            self.C_amo = self.wepon_amounts[num]
            self.num = num

    def fire(self):
        global all_bullets,display,camra
        if (self.fired) <= self.C_amo:
            B1 = Wepons(self.wepon,self.x,self.y,self.angle,self.user_name)
            B1.fire()
            all_bullets.append(B1)
            self.fired += 1

    def update_bullets(self,all_bullets,owners_bullets=False):
        #self.screen_rect = self.image.get_rect(center=(self.x, self.y))
        for bullet in all_bullets:
                bullet.screen_rect = bullet.image.get_rect(center=(bullet.x, bullet.y))
                bullet.rect = pygame.rect.Rect(bullet.x, bullet.y, bullet.sizex, bullet.sizey)
                if bullet.owner != self.user_name:
                    if bullet.rect.colliderect((self.x,self.y,self.HB_sizex,self.HB_sizey)):
                        self.health -= bullet.damage / self.armor
                        bullet.hit()
                        bullet.life_time = 0
                        if self.health <= 0:
                            self.death_cause = ["shot_down",bullet.owner]
                elif bullet.owner == self.user_name:
                    if bullet.life_time <= 0:
                        if bullet.data["extra_BC"] >= 1:
                            bullet.scater()
                            self.fired += 1
                        self.fired -= 1
                        all_bullets.remove(bullet)
                        del bullet
            
    def collect_xp(self):
        global all_xp
        for Xp in all_xp:         
            if self.hitbox.colliderect((Xp.x,Xp.y,Xp.sizex,Xp.sizey)):#Xp.screen_rect
                self.xp += Xp.amount
                if Xp.life_time != "None":
                    pygame.draw.rect(display,(255,0,0),Xp.screen_rect)
                    Xp.life_time = 0
                Pow = Xp.give_pows
                if Pow != "None":
                    #with open(f"data/powers.json","r") as file:
                    #powers_data = json.load(file)
                    pow_obj = powers_data['pows'][Pow]
                    self.curent_pow.append(pow_obj)
                    self.add_pows(pow_obj)
                    

    def collide_plane(self):
        global all_planes
        self.coliding_planes = 0
        for plane in all_planes:
            if plane != self:
                #ang,dist = get_angle_and_dist(plane.x,plane.y,self.x,self.y)
                #total_d = (self.HB_sizex/2) + (plane.HB_sizex/2)
                if self.hitbox.colliderect(plane.hitbox):
                    self.coliding_planes += 1
                    self.apply_collide1(plane)

    def apply_collide1(self, plane):
        ang, dist = util.get_angle_and_dist(self.x, self.y, plane.x, plane.y)
        amount = self.speed/1.1
        rad = math.radians(ang)
        by = amount * math.cos(rad)
        bx = amount * math.sin(rad)
        self.x += -bx
        self.y += -by
        if self.speed > 0:
            self.speed -= self.acceleration*1.1

        self.health -= self.data["impact_damage_rate"]/self.armor
        if plane.data["pow_gives"] != []:
            for p in plane.data["pow_gives"]:
                self.add_pows(powers_data["pows"][p])
                        
    def display_death_msg(self):
        global death_msgs,display
        try:
            msg = death_msgs[self.death_cause[0]]
            msg = msg.format(player=self.death_cause[1])
        except Exception:
            msg = f"you died = {self.death_cause[0]}"
        util.disp_text(msg, text_font_big, (255, 0, 0), center_x, center_y-100)

    def tick_ops(self):
        self.collide_plane()

    def fourth_tick_ops(self):
        if self.speed < self.min_speed:
            self.speed += self.acceleration
        elif self.speed > self.top_speed:
            self.speed -= self.acceleration
                         
    def event(self,loops):
        global all_planes,R_menue_G,button_rects,respawn_lev,heal_amount,settings_data,vol
        presed = False
        num = None
        button = pygame.key.get_pressed()
        if button[pygame.K_w]:
            if self.speed <= self.top_speed:
                self.speed += self.acceleration
            presed = True
        elif button[pygame.K_s]:
            if self.speed > self.min_speed:
                self.speed -= self.acceleration
            elif self.speed < self.min_speed:
                self.speed = self.min_speed
            presed = True
        if button[pygame.K_a]:
            self.angle += self.turn_speed
            self.rotate()
            presed = True
        elif button[pygame.K_d]:
            self.angle -= self.turn_speed
            self.rotate()
            presed = True
        if button[pygame.K_SPACE]:
            if loops % self.fire_speed == 0:
                self.fire()

        if self.speed > self.top_speed:
            self.speed -= self.acceleration

        if button[pygame.K_1]:
            num = 1
        elif button[pygame.K_2]:
            num = 2
        elif button[pygame.K_3]:
            num = 3
        elif button[pygame.K_4]:
            num = 4
        elif button[pygame.K_5]:
            num = 5
        elif button[pygame.K_6]:
            num = 6
        elif button[pygame.K_7]:
            num = 7
        elif button[pygame.K_8]:
            num = 8
        elif button[pygame.K_9]:
            num = 9
        elif button[pygame.K_0]:
            num = 10

        self.wep(num)
        self.move()
        self.tick_ops()
        if loops % 4 == 0:
            self.manage_pows()
            self.fourth_tick_ops()
            out_of_bounds = False
            if self.x < 0:
                out_of_bounds = True
            elif self.x > WORLD_WIDTH:
                out_of_bounds = True
            if self.y < 0:
                out_of_bounds = True
            elif self.y > WORLD_HIGHT:
                out_of_bounds = True
            if out_of_bounds:
                self.health = 0
                if self.health <= 0 and self.PT != "pNone":
                    self.death_cause = ["out_of_bounds",""]
                    util.disp_text("you died ", text_font_big, (255, 0, 0), center_x, center_y-100)
            # ----------------------

        if self.xp >= self.xp_value and self.health < self.data["health"] and heal_amount == 10:
            self.xp -= heal_amount/5
            self.xp = int(self.xp)
            self.health += heal_amount/5
          
        if self.health <= 0 and self.PT != "pNone":
            self.respawn("pNone")
            obj = all_planes.index(self)
            all_planes[obj].PT = "pNone"
            pygame.mixer_music.load(f"sounds/{random.choice(settings_data['death_songs'])}")
            pygame.mixer_music.set_volume(vol + 1)
            pygame.mixer_music.play()
            respawn_lev = None
            button_rects = []
            R_menue_G = None
            self.drop_xp()

        print(f"user >{self.user_name} is at x>{self.x} y>{self.y}")
        print(f"the speed is {self.speed}")
        return presed

    def ai_move(self):
        self.hitbox = pygame.rect.Rect(self.x,self.y,self.HB_sizex,self.HB_sizey)
        amount = self.speed
        rad = math.radians(self.angle)
        delta_x = -amount * math.sin(rad)
        delta_y = -amount * math.cos(rad)
        self.x += delta_x
        self.y += delta_y

    def ai_blit(self, display_surface, camera_obj):
        if self.health <= 0:
            return

        scaled_width = int(self.original_image.get_width() * camera_obj.zoom)
        scaled_height = int(self.original_image.get_height() * camera_obj.zoom)

        if scaled_width > 0 and scaled_height > 0:
            scaled_image = pygame.transform.scale(self.original_image, (scaled_width, scaled_height))
        else:
            scaled_image = pygame.Surface((1,1))

        rotated_image = pygame.transform.rotate(scaled_image, self.angle)
        rect = rotated_image.get_rect()
    
        screen_x = (self.x * camera_obj.zoom) + camera_obj.offset_x
        screen_y = (self.y * camera_obj.zoom) + camera_obj.offset_y
        rect.center = (screen_x, screen_y)

        display_surface.blit(rotated_image, rect)

        # Optional: Draw name above AI plane
        rec = util.disp_text(self.user_name, text_font, (0, 0, 0), rect.centerx, rect.top - 15)
        pygame.draw.rect(display,(0,100,0),(rect.centerx-self.health/2,rec.y+30,self.health,10),border_radius=3)

    def ai_event(self,loops,frontBack,leftRite,spaceShif,num_k):
        global all_planes
        presed = False
        num = None
        if frontBack == 1:
            if self.speed <= self.top_speed:
                self.speed += self.acceleration
            presed = True
        elif frontBack == 2:
            if self.speed > self.min_speed:
                self.speed -= self.acceleration
            elif self.speed < self.min_speed:
                self.speed = self.min_speed
            presed = True
        if leftRite == 1:
            self.angle += self.turn_speed
            self.rotate()
            presed = True
        elif leftRite == 2:
            self.angle -= self.turn_speed
            self.rotate()
            presed = True
        if spaceShif == 1:
            if loops % self.fire_speed == 0:
                self.fire()
        elif spaceShif == 2:
            print("shift is not bound")

        if num_k == 1:
            num = 1
        elif num_k == 2:
            num = 2
        elif num_k == 3:
            num = 3
        elif num_k == 4:
            num = 4
        elif num_k == 5:
            num = 5
        elif num_k == 6:
            num = 6
        elif num_k == 7:
            num = 7
        elif num_k == 8:
            num = 8
        elif num_k == 9:
            num = 9
        elif num_k == 10:
            num = 10

        self.wep(num)
        self.ai_move() 
        self.tick_ops()
        if loops % 4 == 0:
            self.manage_pows()
            self.fourth_tick_ops()
            out_of_bounds = False
            if self.x < 0:
                out_of_bounds = True
            elif self.x > WORLD_WIDTH:
                out_of_bounds = True
            if self.y < 0:
                out_of_bounds = True
            elif self.y > WORLD_HIGHT:
                out_of_bounds = True
            if out_of_bounds:
                self.health -= 1
            # ----------------------

        if self.health <= 0 and self.PT != "pNone":
            self.respawn("pNone")
            obj = all_planes.index(self)
            all_planes[obj].PT = "pNone"
            self.xp = self.xp / 2
            self.drop_xp()

        if self.xp >= self.xp_value and self.health < self.data["health"] and heal_amount == 10:
            self.xp -= heal_amount/1.5
            self.xp = int(self.xp)
            self.health += heal_amount/5

        print(f"AI>{self.user_name} is at x>{self.x} y>{self.y} at speed {self.speed}")
        print(f"AI>{self.user_name}s health is {self.health}")
        return presed

class AI:
    def __init__(self):
        pass



#more initing --------------------
def SET_UP_FILE_SYSTEM():

    print("[SETUP] Creating minimal engine filesystem...")

    # -------------------------------------------------
    # REQUIRED FOLDERS (including empty asset folders)
    # -------------------------------------------------
    folders = [
        "data",
        "data/GFmaps",
        "data/texture_maps",
        "images",

        # empty but required game asset folders
        "props",
        "planes",
        "Paricals",
        "wepons",

        # their stats folders
        "props/stats",
        "planes/stats",
        "Paricals/stats",
        "wepons/wepon_stats"
    ]

    for f in folders:
        if not os.path.exists(f):
            os.makedirs(f)
            print(f"[SETUP] Created folder: {f}")

    # -------------------------------------------------
    # REQUIRED JSON FILES WITH MINIMAL VALID CONTENT
    # (engine will crash without these)
    # -------------------------------------------------

    # death messages
    death_msgs = {
        "shot_down": "You were shot down by {player}",
        "out_of_bounds": "You went out of bounds",
        "crashed": "You crashed"
    }

    # settings
    settings = {
        "xpp": 4,
        "volume": 1.0,
        "death_songs": []
    }

    # GF map (points to essential JSON files)
    gf_map = {
        "data/death_msgs.json": False,
        "data/settings.json": False
    }

    # texture map (only watter.png is required)
    texture_map = {
        "images/watter.png": False
    }

    json_files = {
        "data/death_msgs.json": death_msgs,
        "data/settings.json": settings,
        "data/GFmaps/Main.json": gf_map,
        "data/texture_maps/D1.json": texture_map
    }

    for path, content in json_files.items():
        if not os.path.exists(path):
            with open(path, "w") as f:
                json.dump(content, f, indent=4)
            print(f"[SETUP] Created file: {path}")

    # -------------------------------------------------
    # DEFAULT WATER PNG
    # -------------------------------------------------
    water_path = "images/watter.png"
    if not os.path.exists(water_path):
        pygame.init()
        surf = pygame.Surface((32, 32))
        surf.fill((50, 100, 255))  # basic blue
        pygame.image.save(surf, water_path)
        print(f"[SETUP] Created default image: {water_path}")

    print("[SETUP] Minimal filesystem complete!")



with open("data/death_msgs.json","r") as file:
    death_msgs = json.load(file)
with open("data/settings.json","r") as file:
    settings_data = json.load(file)

defalt_image = pygame.image.load("images/watter.png")
window = pygame.surface.Surface(window_size)

window = pygame.display.set_mode(window_size)
if not pygame.display.is_fullscreen():
    pygame.display.toggle_fullscreen()

display = pygame.Surface(display_size)
display_rect = display.get_rect(center=(window.get_width() // 2, window.get_height() // 2))
window_width = window.get_width()
window_height = window.get_height()
scale = min(window_width / display.get_width(), window_height / display.get_height())
new_size = (int(display.get_width() * scale), int(display.get_height() * scale))
W_pos = ((window_width - new_size[0]) // 2, (window_height - new_size[1]) // 2)

center_x = display.get_width() / 2
center_y = display.get_height() / 2

loader = Loader("data/texture_maps/D1.json","data/GFmaps/Main.json")
camra = GameCamera(display,CHUNK_SIZE)
util = Util()
updator = Updator()
clock = pygame.Clock()
#------------ Main classes  -----------





