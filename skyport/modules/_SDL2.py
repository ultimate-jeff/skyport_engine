from ..imports import *
from ..global_utils import (
    Class_Data,
    logger
)

from ..main import (
    Display_Manager,
    Render,
    Layer
)


def _SDL2_access(func):
    def wrapper(self,*args,**kwargs):
        renderer = SDL2_Render._global_render
        prev_target = renderer.target
        renderer.target = self._texture
        data = func(self,*args,**kwargs,render=renderer)
        renderer.target = prev_target
        return data
    return wrapper

class SDL2_Render(Render):
    # still experimental
    _global_render = None
    def __init_texture(self,surf,width,height):
        #self.OG_image = surf if surf != None else pygame.Surface((width,height),flags=pygame.SRCALPHA)
        if SDL2_Render._global_render == None:
            raise RuntimeError("SDL_Render can't be initialized before SDL2_Display_Manager")
        
    def __init__(self,x:"int",y:"int",width:"int",height:"int",angle:"int",surf:"pygame.Surface"=None):
        """this class is meant to be inherited by other classes or used in them so like class MyGameObj(Render): ...."""
        super()
        self._base_init()
        self.tags = {}
        self.rect = pygame.Rect(x,y,width,height)
        self.angle = angle
        self.__init_texture(surf,width,height)
        self._last_angle = None
        self._last_size = None
        self._is_dirty = False
        self._is_dirty = True
        self.update_surf()

class SDL2_Display_Manager(Display_Manager):
    def __init__(self, window_size, display_size, force_full_screen = False, window_name = "skyport-engine window", window_ico = None, resizable = True,root_layer=None):
        """this display manager uses pygames _sdl2 which is experimental so this might not work on ur pygame version (this was built with pygame-ce v2.5.7)"""
        self.root_layer = root_layer if root_layer != None else Layer(display_size[0],display_size[1])
        self._user_clock = pygame.time.Clock()
        self.rendering_thread = None
        self.loops = 0
        self.target_fps = 60
        self.running = False
        self._display_dirty = True

        self.update__root_layers = True

        self.window_name = window_name
        self._window_ico = window_ico
        self._force_full_screen = force_full_screen
        self.resizeable_window = resizable
        self._display_size = display_size
        self.window_size = window_size

        self._base_init()

        self.display = pygame.Surface(display_size)
        self.__clock = pygame.time.Clock()
        self._couculate_window_scaling(pygame.rect.Rect(0,0,window_size[0],window_size[1]))

    def _couculate_window_scaling(self,rect:"pygame.Rect"=None):
        if hasattr(self,"window"):
            self.window_width, self.window_height = self.window.size
        else:
            self.window_width,self.window_height = rect.size
        self.display_rect = self.display.get_rect(center=(self.window_width // 2, self.window_height // 2))
        self._scale = min(self.window_width / self.display.get_width(), self.window_height / self.display.get_height())
        self._new_size = (int(self.display.get_width() * self._scale), int(self.display.get_height() * self._scale))
        self._W_pos = ((self.window_width - self._new_size[0]) // 2, (self.window_height - self._new_size[1]) // 2)

        self._dest_rect = (*self._W_pos, *self._new_size)  

    def update_window(self):
        """this manually updates the window (do not call this after starting rendering thread bc the rendering thread already dose)"""
        with self._locks["update"]:
            if self.update__root_layers:
                self.update_root_layer()
            self.loops += 1
            #if self._display_dirty:
            self._display_dirty = False
            self._display_texture.update(self.display)
            self._render.clear()
            self._display_texture.draw(dstrect=self._dest_rect)
            self._render.present()

    def _init_window(self):
        self.window = video.Window(self.window_name, self.window_size, resizable=self.resizeable_window)
        self._render = video.Renderer(self.window)
        SDL2_Render._global_render = self._render # enshure sdl2_render class has the _render
        self._display_texture = video.Texture(self._render, self._display_size)
        if self._window_ico:
            self.window.set_icon(self._window_ico)
        if self._force_full_screen:
            self.window.set_fullscreen(True)
        self._couculate_window_scaling()

    def _rendering_loop(self):
        self._init_window()

        while (self.running):
            self._run()

    def _run(self):
        self.update_window()
        self.__clock.tick(self.target_fps)
        self.event_handler()


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
        
    def _WINDOW_RESIZE_HANDLER(self,event):
        with self._locks["display"]:
            print(f"resize to ({event.x},{event.y})")
            self._couculate_window_scaling()
            self._display_texture = video.Texture(self._render, self._display_size)
            self._display_dirty = True
