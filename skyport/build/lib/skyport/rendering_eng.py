
import os
import sys
import threading
#from pygame._sdl2.video import Window, Renderer, Texture
from skyport.core.paths import PathUtil as pu
from skyport.core.paths import loger

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
   sys.path.insert(0, BASE_DIR)

from skyport.core.paths import pygame
#pygame.init()

pygame.display.init()
pygame.display.set_mode((1, 1), pygame.HIDDEN)

# engine imports
#from skyport.assets.layar_manager import *
from skyport.assets.layar_manager import Layar_manager
from skyport.assets.layar_manager import Camera

from skyport.global_utils import (
    Delta_timer, Util, Loader, r_obj, Sprite, 
    prin_RESET, prin_RED, prin_GREEN, prin_BLUE,
    loader,util,loger
)

class Display_manager:
    def __init__(self,window_size,display_size,force_full_screen=True,window_name="spyport engine window",window_ico=None,resizable=True):
        self.loops = 0
        self.print_rate = 8
        #self.win = Window("skyport engine window--", size=window_size)
        self.running = True
        self.window_ico = window_ico
        self.clock = pygame.time.Clock()
        self._stop_event = threading.Event()
        self.rendering_thread = None
        self.force_full_screen = force_full_screen
        self.window_size = window_size
        self.display_size = display_size
        self.display = pygame.Surface(self.display_size)
        pygame.display.set_icon(self.window_ico) if self.window_ico else None
        self.window = pygame.display.set_mode(window_size,pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.RESIZABLE)
        pygame.display.set_caption(window_name)
        lm = Layar_manager(self.display)
        self.dt = Delta_timer()
        self.util = Util()
        self.print_que = ""
        self.curent_game_state = "main"
        self.game_states = {"main":lm}

        if not pygame.display.is_fullscreen() and force_full_screen:
            pygame.display.toggle_fullscreen()

        self.couculate_window_scaling()
        loger.log("Display manager initialized")
    
    def get_lm(self):
        return self.game_states[self.curent_game_state]
    def add_gamestate(self,name,lm):
        self.game_states[name] = lm
        loger.log(f"added game state {name}")
    def remove_game_stare(self,name):
        if name in self.game_states:
            del self.game_states[name]
            loger.log(f"removed game state {name}")
        else:
            loger.log(f"tried to remove game state {name} but it does not exist")

    def cclock(self,TFPS):
        #self._event()
        self.loops += 1
        self.s_display = pygame.transform.scale(self.display, self.new_size)
        self.window.blit(self.s_display,self.W_pos)
        Util.print(f"loops are at {self.loops} and fps is at {self.clock.get_fps():.2f}")
        pygame.display.flip()
        self.clock.tick(TFPS)

    def couculate_window_scaling(self):
        self.display_rect = self.display.get_rect(center=(self.window.get_width() // 2, self.window.get_height() // 2))
        self.window_width = self.window.get_width()
        self.window_height = self.window.get_height()
        self._scale = min(self.window_width / self.display.get_width(), self.window_height / self.display.get_height())
        self.new_size = (int(self.display.get_width() * self._scale), int(self.display.get_height() * self._scale))
        self.W_pos = ((self.window_width - self.new_size[0]) // 2, (self.window_height - self.new_size[1]) // 2)

        self.center_x = self.display.get_width() / 2
        self.center_y = self.display.get_height() / 2
    
    def get_mouse_pos(self):
        mx, my = pygame.mouse.get_pos()
        self,mouse_pos = (((mx - self.W_pos[0]) / self._scale),((my - self.W_pos[1]) / self._scale))

    def render(self):
        self.display.blit(self.game_states[self.curent_game_state].render(),(0,0))

    def _rendering_loop(self):
        try:
            while not self._stop_event.is_set():
                self.render()
                self.cclock(self.fps)
                self.dt.get_dt()
        except Exception as e:
            print(f"exiting render loop do to {e}")
            loger.log(f"exiting render loop do to {e}")

    def START_RENDERING_THREAD(self, fps):
        self.fps = fps
        self._stop_event.clear() 
        self.rendering_thread = threading.Thread(target=self._rendering_loop, daemon=True)
        self.rendering_thread.start()

    def STOP_RENDERING_THREAD(self):
        if self.rendering_thread and self.rendering_thread.is_alive():
            self._stop_event.set()
            self.rendering_thread.join() 
        loger.log("Rendering thread stopped")
        loger.save()
    def event(self):
        if self.loops % self.print_rate == 0:
            Util.output_print_data()
        try:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                    print("\nquit pressed\n")
                    self.STOP_RENDERING_THREAD()
                    pygame.quit()
                if event.type == pygame.VIDEORESIZE:
                    self.couculate_window_scaling()
        except Exception as e:
            loger.log(f"error in event handeling: {e}")


