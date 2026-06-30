
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
        self._user_clock = pygame.time.Clock()
        self.rendering_thread = None
        self.keybinds = {"up":{},"down":{},"buttons":{}}
        self.loops = 0
        self.target_fps = 60
        self.running = False
        self._display_size = display_size
        self.window_size = window_size
        self.display = pygame.Surface(display_size)
        self.window = pygame.display.set_mode(window_size,pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.RESIZABLE)
        pygame.display.set_icon(window_ico) if window_ico else None
        pygame.display.set_caption(window_name)

        if not pygame.display.is_fullscreen() and force_full_screen:
            pygame.display.toggle_fullscreen()
        self._couculate_window_scaling()

    def tick(self,tps):
        self._user_clock.tick(tps)

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

    def update_window(self):
        #self._event()
        self.loops += 1
        with self._locks["display"]:
            self._s_display = pygame.transform.scale(self.display, self._new_size)
        self.window.blit(self._s_display,self._W_pos)
        pygame.display.flip()

    def _rendering_loop(self):
        self.window = self.window = pygame.display.get_surface() #pygame.display.set_mode(self.window_size,pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.RESIZABLE)
        self.__clock = pygame.time.Clock()
        while (self.running):
            self.update_window()
            self.__clock.tick(self.target_fps)
        
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

    def _exacute_funcs(self,funcs):
        for func in funcs:
            func()

    def _handle_buttons_keybinds(self):
        buttons = pygame.key.get_pressed()
        binds = self.keybinds["buttons"]
        for bind, funcs in binds.items():
            if buttons[bind]:
                self._exacute_funcs(funcs)

    def event_handler(self):
        try:
            self._handle_buttons_keybinds()
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
                    funcs = self.keybinds["down"].get(event.key,lambda : loger.log(f"key {event.key} is not bound (keydonw)"))
                    self._exacute_funcs(funcs)
                if event.type == pygame.KEYUP:
                    funcs = self.keybinds["up"].get(event.key,lambda : loger.log(f"key {event.key} is not bound (keyup)"))
                    self._exacute_funcs(funcs)
        except Exception as e:
            loger.log(f"error in event handeling: {e}")
            events = []

    def blit(self,source: "pygame.Surface", dest: "pygame.RectLike" = (0, 0), area: "pygame.RectLike" = None, special_flags: "int" = 0):
        with self._locks["display"]:
            self.display.blit(source,dest,area,special_flags)

    def fill(self,color:"tuple"=(0,0,0,0),rect:"pygame.Rect"=None,special_flags:"int"=0):
        with self._locks["display"]:
            self.display.fill(color,rect,special_flags)
    def get_display(self):
        return self.display
    def set_tfps(self,value:"int"):
        with self._locks["target_fps"]:
            self.target_fps = value
    def get_tfps(self):
        with self._locks["target_fps"]:
            value = self.target_fps
        return value
    def get_fps(self):
        return self._clock.get_fps()
    
    def add_keyup_bind(self,key:"int",func:"function"):
        self.keybinds["up"].setdefault(key, []).append(func)
    def add_keydown_bind(self,key:"int",func:"function"):
        self.keybinds["down"].setdefault(key, []).append(func)
    def add_keypressed_bind(self,key:"int",func:"function"):
        self.keybinds["buttons"].setdefault(key, []).append(func)

    def _remove_bind(self,type,key,func):
        if key in self.keybinds[type]:
            try:
                self.keybinds[type][key].remove(func)
            except ValueError:
                loger.log(f"function to key {key} not found")
            if not self.keybinds[type][key]:
                del self.keybinds[type][key]
                
    def remove_keyup_bind(self,key:"int",func:"function"):
        keys = key if isinstance(key, (list, tuple)) else [key]
        for k in keys:
            self._remove_bind("up", k, func)
    def remove_keydown_bind(self,key:"int",func:"function"):
        keys = key if isinstance(key, (list, tuple)) else [key]
        for k in keys:
            self._remove_bind("down", k, func)
    def remove_keypressed_bind(self,key:"int",func:"function"):
        keys = key if isinstance(key, (list, tuple)) else [key]
        for k in keys:
            self._remove_bind("buttons", k, func)