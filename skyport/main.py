
import queue
import time

from skyport.global_utils import *

pygame.display.init()
pygame.display.set_mode((1, 1), pygame.HIDDEN)


class Display_Manager(Class_Data):
    def __init__(self,window_size:"tuple",display_size:"tuple",force_full_screen:bool=False,window_name:str="skyport-engine window",window_ico:"pygame.Surface"=None,resizable:bool=True):
        super().__init__()

        self._locks = {
            "target_fps":threading.Lock(),
            "running":threading.Lock(),
            "display":threading.Lock()
        }

        self.rendering_thread = None
        self.keybinds = {"up":{},"down":{}}
        self.loops = 0
        self.target_fps = 60
        self.running = False
        self._display_size = display_size
        self._window_size = window_size
        self.display = pygame.Surface(display_size)
        self.window = pygame.display.set_mode(window_size,pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.RESIZABLE)
        pygame.display.set_icon(window_ico) if window_ico else None
        pygame.display.set_caption(window_name)

        if not pygame.display.is_fullscreen() and force_full_screen:
            pygame.display.toggle_fullscreen()
        self._couculate_window_scaling()

    def _couculate_window_scaling(self):
        self.display_rect = self.display.get_rect(center=(self.window.get_width() // 2, self.window.get_height() // 2))
        self.window_width = self.window.get_width()
        self.window_height = self.window.get_height()
        self._scale = min(self.window_width / self.display.get_width(), self.window_height / self.display.get_height())
        self._new_size = (int(self.display.get_width() * self._scale), int(self.display.get_height() * self._scale))
        self._W_pos = ((self.window_width - self._new_size[0]) // 2, (self.window_height - self._new_size[1]) // 2)

        self.center_x = self.display.get_width() / 2
        self.center_y = self.display.get_height() / 2

    def get_mouse_pos(self):
        mx, my = pygame.mouse.get_pos()
        self.mouse_pos = (((mx - self._W_pos[0]) / self._scale),((my - self._W_pos[1]) / self._scale))
        return self.mouse_pos

    def _cclock(self):
        #self._event()
        self.loops += 1
        with self._locks["display"]:
            self._s_display = pygame.transform.scale(self.display, self._new_size)
        self.window.blit(self._s_display,self._W_pos)
        pygame.display.flip()
        self._clock.tick(self.target_fps)

    def _rendering_loop(self):
        self._clock = pygame.time.Clock()
        while (self.running):
            self._cclock()
        
    def START_RENDERING_THREAD(self, fps):
        self.target_fps = fps
        self.running = True
        self.rendering_thread = threading.Thread(target=self._rendering_loop, daemon=True)
        self.rendering_thread.start()
        loger.log("Rendering thread started")

    def STOP_RENDERING_THREAD(self):
        if self.rendering_thread and self.rendering_thread.is_alive():
            self.running = False
            self.rendering_thread.join() 
        loger.log("Rendering thread stopped")

    def event_handler(self):
        try:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                    print("\nquit pressed\n")
                    self.STOP_RENDERING_THREAD()
                    pygame.quit()
                if event.type == pygame.VIDEORESIZE:
                    self._couculate_window_scaling()
                if event.type == pygame.KEYDOWN:
                    func = self.keybinds["down"].get(event.key)
                    func()
                if event.type == pygame.KEYUP:
                    func = self.keybinds["up"].get(event.key)
                    func()
        except Exception as e:
            loger.log(f"error in event handeling: {e}")
            events = []

    def blit(self,source: "Surface", dest: "RectLike" = (0, 0), area: "RectLike" = None, special_flags: "int" = 0):
        with self._locks["display"]:
            self.display.blit(source,dest,area,special_flags)

    def fill(self,color:" list[R,G,B,A] "=(0,0,0,0)):
        with self._locks["display"]:
            self.display.fill(color)
    def set_tfps(self,value:"int"):
        with self._locks["target_fps"]:
            self.target_fps = value
    def get_tfps(self):
        with self._locks["target_fps"]:
            value = self.target_fps
        return value
    def get_fps(self):
        return self._clock.get_fps()
    def add_keybind(self,event:"str",key:"str",func:"function"):
        """event can be up down for on key up or on key down"""
        event_type = self.keybinds.get(event.lower(),"down")
        self.keybinds[event_type][key] = func
    def remove_keybind(self,event:"str",key:"str",func:"function"):
        """event can be up down for on key up or on key down"""
        event_type = self.keybinds.get(event.lower(),"down")
        try:
            self.keybinds[event_type].pop(key)
        except KeyError:
            pass