
import pygame
import math
import random
import time
import json
import sys
import os

# engine imports
from global_utils import *


class GameCamera:
    def __init__(self, display_surface, chunk_size,WORLD_WIDTH,WORLD_HIGHT,chunk_genorator_script=None):
        self.tiles = {}
        self.all_game_objs = []
        self.display_surface = display_surface
        self.chunk_size = chunk_size
        self.offset_x = 0
        self.offset_y = 0
        self.zoom = 1.0
        self.old_zoom = self.zoom
        self.WORLD_HIGHT = WORLD_HIGHT
        self.WORLD_WIDTH = WORLD_WIDTH
        self.CHUNKS_ON_X = self.WORLD_WIDTH // self.chunk_size
        self.CHUNKS_ON_Y = self.WORLD_HIGHT // self.chunk_size
        self.print_queue = ""
        self.genorator = chunk_genorator_script

    def render_offset_objs(self,disp=None):
        scale_all_obs = self.zoom != self.old_zoom
        sw, sh = self.display_surface.get_size() # sw and sh stand for screen width and screen height
        for obj in self.all_game_objs:
            screen_x = obj.x * self.zoom + self.offset_x
            screen_y = obj.y * self.zoom + self.offset_y
            if -obj.rect.width < screen_x < sw and -obj.rect.height < screen_y < sh:
                if scale_all_obs:
                    obj.scale_surf(self.zoom)
                self.display_surface.blit(obj.surf, (screen_x, screen_y))
        if scale_all_obs:
            self.old_zoom = self.zoom

    def chunkify(self,obj):
        c_pos = self.get_chunk_cords(obj.x,obj.y)
        chunk = self.get_chunk(c_pos[0], c_pos[1])
        chunk.all_objs.append(obj)

    def get_chunk_cords(self,x,y):
        cx = int(x) // self.chunk_size
        cy = int(y) // self.chunk_size
        return (cx,cy)

    def get_chunk(self,cx, cy):
        #return chunk at (cx, cy), create if it doesnt exist yet
        if (cx, cy) not in self.tiles:
            self.tiles[(cx, cy)] = Chunk(cx, cy, self.chunk_size,genorator=self.genorator)
            print(f"{prin_GREEN}Created chunk {cx},{cy}{prin_RESET}")
        return self.tiles[(cx, cy)]

    def tick_ops(self):
        if self.print_queue != "":
            print(self.print_queue)
        self.print_queue = ""

    def set_zoom(self, level):
        self.zoom = max(0.1, level)

    def get_min_max_c_pos(self,z,W,H):
        world_left   = -self.offset_x / z
        world_top    = -self.offset_y / z
        world_right  = world_left + W / z
        world_bottom = world_top + H / z

        min_cx = max(0, int(math.floor(world_left / self.chunk_size)))
        max_cx = min(self.CHUNKS_ON_X - 1, int(math.floor(world_right / self.chunk_size)))
        min_cy = max(0, int(math.floor(world_top / self.chunk_size)))
        max_cy = min(self.CHUNKS_ON_Y - 1, int(math.floor(world_bottom / self.chunk_size)))
        return min_cx,min_cy,max_cx,max_cy

    def camera_render(self, target_x, target_y):
        W, H = self.display_surface.get_size()
        z = self.zoom

        self.offset_x = -target_x * z + W // 2
        self.offset_y = -target_y * z + H // 2

        min_cx,min_cy,max_cx,max_cy = self.get_min_max_c_pos(z,W,H)

        for cx in range(min_cx, max_cx + 1):
            for cy in range(min_cy, max_cy + 1):
                chunk = self.get_chunk(cx, cy)
                surf = chunk.scaled_surface(z)
                chunk.update(self.zoom,self,fill_frame=self.is_transparent)
                screen_x = cx * self.chunk_size * z + self.offset_x
                screen_y = cy * self.chunk_size * z + self.offset_y
                self.display_surface.blit(surf, (screen_x, screen_y))

        self.tick_ops()

class Chunk:
    def __init__(self, cx, cy, chunk_size ,genorator=None):
        self.cx = cx
        self.cy = cy
        self.size = chunk_size
        self.surf = pygame.Surface((chunk_size, chunk_size), flags=pygame.SRCALPHA)
        self.surf.fill((0, 0, 0))
        self._scaled = None
        self._last_zoom = None
        self.tags = {}
        self.all_objs = []
        self.bg_surf = None
        self.generate_terrain(genorator)

    def scale__(self,zoom):
        w = max(1, int(self.size * zoom))
        h = max(1, int(self.size * zoom))
        self._scaled = pygame.transform.scale(self.surf, (w, h))
        self._last_zoom = zoom

    def scaled_surface(self, zoom):
        if self._last_zoom != zoom or self._scaled is None:
            self.scale__(zoom)
        return self._scaled

    def generate_terrain(self,genorator=None):
        if genorator != None:
            exec(genorator)

    def blit_objs(self,zoom):
        for obj in self.all_objs:
            self._scaled.blit(obj.get_surf(zoom), ((obj.x - self.cx) * zoom, (obj.y - self.cy) * zoom))

    def blit_objs_v2(self,zoom,cam):
        for obj in self.all_objs:
            cam.display_surface.blit(obj.get_surf(zoom),((obj.x + self.cx) * zoom, (obj.y + self.cy) * zoom))
            if abs(obj.x - obj.og_x) >= self.size or abs(obj.y - obj.og_y) >= self.size:
                cam.print_queue += f"obj {obj.id} is at {obj.x},{obj.y} and beeing rechunked\n"
                self.all_objs.remove(obj)
                cam.chunkify(obj)

    def update(self,zoom,cam,fill_frame=False):
        if fill_frame:
            self._scaled.fill((0, 0, 0))
        if self.bg_surf != None:
            self.surf.blit(self.bg_surf,(0,0))
        self.blit_objs_v2(zoom,cam)





