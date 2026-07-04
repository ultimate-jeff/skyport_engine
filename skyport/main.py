
import queue
import time

from skyport.global_utils import *
from pygame import _sdl2 as video

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
        self.resizeable_window = resizable
        self._display_size = display_size
        self.window_size = window_size
        self.display = pygame.Surface(display_size)
        self.window = pygame.display.set_mode(window_size,pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.RESIZABLE if resizable else 0)
        pygame.display.set_icon(window_ico) if window_ico else None
        pygame.display.set_caption(window_name)

        if not pygame.display.is_fullscreen() and force_full_screen:
            pygame.display.toggle_fullscreen()
        self._couculate_window_scaling()
        self._couculate_display_center()

    def tick(self,tps):
        self._user_clock.tick(tps)

    def _couculate_window_scaling(self):
        self.display_rect = self.display.get_rect(center=(self.window.get_width() // 2, self.window.get_height() // 2))
        self.window_width = self.window.get_width()
        self.window_height = self.window.get_height()
        self._scale = min(self.window_width / self.display.get_width(), self.window_height / self.display.get_height())
        self._new_size = (int(self.display.get_width() * self._scale), int(self.display.get_height() * self._scale))
        self._W_pos = ((self.window_width - self._new_size[0]) // 2, (self.window_height - self._new_size[1]) // 2)

    def _couculate_display_center(self):
        self.center_x = self.display.get_width() / 2
        self.center_y = self.display.get_height() / 2

    def get_mouse_pos(self) -> "tuple(x,y)":
        """returns (x,y) of your mouse relative to the window"""
        mx, my = pygame.mouse.get_pos()
        self.mouse_pos = (((mx - self._W_pos[0]) / self._scale),((my - self._W_pos[1]) / self._scale))
        return self.mouse_pos

    def update_window(self):
        """this manually updates the window (do not call this after starting rendering thread bc the rendering thread already dose)"""
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
        """this starts the rendering thread"""
        self.target_fps = fps
        self.running = True
        self.rendering_thread = threading.Thread(target=self._rendering_loop, daemon=True)
        self.rendering_thread.start()
        loger.log("Rendering thread started")

    def STOP_RENDERING_THREAD(self):
        """did you know that this stops the rendering thread"""
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
        """you will need to call this in your game loop to handle input events like window resizing or keybinds"""
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
                    print(event.size)
                    self._couculate_window_scaling()
                    self.window.fill((0,0,0))
                if event.type == pygame.KEYDOWN:
                    funcs = self.keybinds["down"].get(event.key,[lambda : loger.log(f"key {event.key} is not bound (keydonw)")])
                    self._exacute_funcs(funcs)
                if event.type == pygame.KEYUP:
                    funcs = self.keybinds["up"].get(event.key,[lambda : loger.log(f"key {event.key} is not bound (keyup)")])
                    self._exacute_funcs(funcs)
        except Exception as e:
            loger.log(f"error in event handeling: {e}")
            events = []

    def blit(self,source: "pygame.Surface", dest: "pygame.RectLike" = (0, 0), area: "pygame.RectLike" = None, special_flags: "int" = 0):
        """self.display.blit(.....)"""
        with self._locks["display"]:
            self.display.blit(source,dest,area,special_flags)

    def fill(self,color:"tuple"=(0,0,0,0),rect:"pygame.Rect"=None,special_flags:"int"=0):
        """self.display.fill(...)"""
        with self._locks["display"]:
            self.display.fill(color,rect,special_flags)
    def get_display(self):
        return self.display
    def set_tfps(self,value:"int"):
        """sets the target frames per second"""
        with self._locks["target_fps"]:
            self.target_fps = value
    def get_tfps(self):
        """gets the target frames per second"""
        with self._locks["target_fps"]:
            value = self.target_fps
        return value
    def get_fps(self):
        """this gets the actual fps"""
        return self.__clock.get_fps()
    
    def _add_bind(self, _type, key, func):
        binds = self.keybinds[_type].setdefault(key, [])  # <-- need this
        if isinstance(func, (list, tuple)):
            binds.extend(func)
        else:
            binds.append(func)

    def add_keyup_bind(self,key:"int",func:"function"):
        self._add_bind("up",key,func)
    def add_keydown_bind(self,key:"int",func:"function"):
        self._add_bind("down",key,func)
    def add_keypressed_bind(self,key:"int",func:"function"):
        self._add_bind("buttons",key,func)

    def _remove_bind(self,_type,key,funcs):
        funcs = funcs if isinstance(funcs,(tuple,list)) else [funcs]
        if key not in self.keybinds[_type]:
            loger.log(f"invalid key {key} (try using pygame.K_...)")
            return
        binds = self.keybinds[_type][key]
        for func in funcs:
            try:
                binds.remove(func)
            except ValueError:
                loger.log(f"function to {key} not found. func->{func}")
        if not binds:
            del self.keybinds[_type][key]

    def remove_keyup_bind(self,key:"int",func:"function"):
        self._remove_bind("up",key,func)
    def remove_keydown_bind(self,key:"int",func:"function"):
        self._remove_bind("down",key,func)
    def remove_keypressed_bind(self,key:"int",func:"function"):
        self._remove_bind("buttons",key,func)



class Render(Class_Data):
    def __init__(self,x:"int",y:"int",width:"int",height:"int",angle:"int",surf:"pygame.Surface"=None):
        """this class is meant to be inherited by other classes or used in them so like class MyGameObj(Render): ...."""
        super().__init__()
        self.rect = pygame.Rect(x,y,width,height)
        self.angle = angle
        self.OG_image = surf if surf != None else pygame.Surface((width,height),flags=pygame.SRCALPHA)
        self._last_angle = None
        self._last_size = None
        self.update_surf()

    def _scale(self):
        size = self.rect.size
        if self._last_size != size:
            self._scaled_image = pygame.transform.scale(self.OG_image,size)
            self._last_size = size
            self._last_angle = None
    def _rotate(self):
        if self._last_angle != self.angle:
            self.image = pygame.transform.rotate(self._scaled_image,self.angle)
            self._last_angle = self.angle
    def update_surf(self):
        """this updates the self.image so that it is the corect scale and angle"""
        self._scale()
        self._rotate()

    def set_angle(self,new_angle:"int"):
        """sets angle and automaticly updates the surf"""
        self.angle = new_angle
        self.update_surf()
    def set_rect(self,new_rect:pygame.Rect):
        """sets the rect and automaticly updates the surf"""
        self.rect = new_rect
        self.update_surf()
    def get_pos(self) -> tuple:
        return (self.rect.x,self.rect.y)
    def set_pos(self,x,y):
        self.rect.x,self.rect.y = x,y
    def get_size(self) -> tuple:
        return self.rect.size
    def set_size(self,new_size):
        """this sets the size and automaticly updates the surf"""
        self.rect.size = new_size
        self.update_surf()
    def get_surf(self) -> pygame.Surface:
        return self.image



class SDL2_Display_Manager(Display_Manager):
    def __init__(self, window_size, display_size, force_full_screen = False, window_name = "skyport-engine window", window_ico = None, resizable = True):
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
        self._display_dirty = True

        self.resizeable_window = resizable
        self._display_size = display_size
        self.window_size = window_size
        self.display = pygame.Surface(display_size)
        self.window = video.Window(window_name,window_size,resizable=resizable)
        self._render = video.Renderer(self.window)

        self._display_texture = video.Texture(self._render, self._display_size)
        if window_ico:
            self.window.set_icon(window_ico)
        if force_full_screen:
            self.window.set_fullscreen(True) 

        self._couculate_window_scaling()

    def _couculate_window_scaling(self):

        self.window_width, self.window_height = self.window.size
        self.display_rect = self.display.get_rect(center=(self.window_width // 2, self.window_height // 2))
        self._scale = min(self.window_width / self.display.get_width(), self.window_height / self.display.get_height())
        self._new_size = (int(self.display.get_width() * self._scale), int(self.display.get_height() * self._scale))
        self._W_pos = ((self.window_width - self._new_size[0]) // 2, (self.window_height - self._new_size[1]) // 2)

        self._dest_rect = (*self._W_pos, *self._new_size)  

    def update_window(self):
        """this manually updates the window (do not call this after starting rendering thread bc the rendering thread already dose)"""
        #self._event()
        self.loops += 1
        with self._locks["display"]:
            if self._display_dirty:
                self._display_dirty = False
                self._display_texture.update(self.display)
        self._render.clear()
        self._display_texture.draw(dstrect=self._dest_rect)
        self._render.present()

    def _rendering_loop(self):
        self.__clock = pygame.time.Clock()
        while (self.running):
            self.update_window()
            self.__clock.tick(self.target_fps)

    def blit(self, source: "pygame.Surface", dest: "pygame.RectLike" = (0, 0), area: "pygame.RectLike" = None, special_flags: "int" = 0):
        """self.display.blit(.....)"""
        with self._locks["display"]:
            self.display.blit(source, dest, area, special_flags)
            self._display_dirty = True

    def fill(self, color: "tuple" = (0,0,0,0), rect: "pygame.Rect" = None, special_flags: "int" = 0):
        """self.display.fill(...)"""
        with self._locks["display"]:
            self.display.fill(color, rect, special_flags)
            self._display_dirty = True

    def get_fps(self):
        return self.__clock.get_fps()
        
    def event_handler(self):
        """you will need to call this in your game loop to handle input events like window resizing or keybinds"""
        try:
            self._handle_buttons_keybinds()
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.WINDOWCLOSE:
                    self.running = False
                    print("\nquit pressed\n")
                    self.STOP_RENDERING_THREAD()
                    pygame.quit()

                if event.type == pygame.WINDOWRESIZED:
                    print(event.x, event.y) 
                    self._couculate_window_scaling()
                    self._render.clear()

                if event.type == pygame.KEYDOWN:
                    funcs = self.keybinds["down"].get(event.key,[lambda : loger.log(f"key {event.key} is not bound (keydonw)")])
                    self._exacute_funcs(funcs)
                if event.type == pygame.KEYUP:
                    funcs = self.keybinds["up"].get(event.key,[lambda : loger.log(f"key {event.key} is not bound (keyup)")])
                    self._exacute_funcs(funcs)
        except Exception as e:
            loger.log(f"error in event handeling: {e}")
            events = []

