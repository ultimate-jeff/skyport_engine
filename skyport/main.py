
import queue
import time

from skyport.global_utils import *
from pygame import _sdl2 as video

pygame.display.init()
pygame.display.set_mode((1, 1), pygame.HIDDEN)



class Render(Class_Data):
    def __init_texture(self,surf,width,height):
        self.OG_image = surf if surf != None else pygame.Surface((width,height),flags=pygame.SRCALPHA)

    def __init__(self,x:"int",y:"int",width:"int",height:"int",angle:"int",surf:"pygame.Surface"=None):
        """this class is meant to be inherited by other classes or used in them so like class MyGameObj(Render): ...."""
        super().__init__()
        self.tags = {}
        self.rect = pygame.Rect(x,y,width,height)
        self.angle = angle
        self.__init_texture(surf,width,height)
        self._last_angle = None
        self._last_size = None
        self._is_dirty = False
        self._is_dirty = True
        self.update_surf()

    def _scale(self):
        size = self.rect.size
        if self._last_size != size or self._is_dirty:
            self._scaled_image = pygame.transform.scale(self.OG_image,size)
            self._last_size = size
            self._last_angle = None
    def _rotate(self):
        if self._last_angle != self.angle or self._is_dirty:
            self.image = pygame.transform.rotate(self._scaled_image,self.angle)
            self._last_angle = self.angle

    def update_surf(self):
        """this updates the self.image so that it is the corect scale and angle"""
        self._scale()
        self._rotate()
        self._is_dirty = False

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
    
    def blit(self,source: "pygame.Surface", dest: "pygame.RectLike" = (0, 0), area: "pygame.RectLike" = None, special_flags: "int" = 0):
        """blits to surf and auto updates"""
        self.OG_image.blit(source,dest,area,special_flags)
        self.force_update()
    def fill(self,color:"tuple"=(0,0,0,0),rect:"pygame.Rect"=None,special_flags:"int"=0):
        """fills surf and auto updates"""
        self.OG_image.fill(color,rect,special_flags)
        self.force_update()

    def force_update(self):
        self._is_dirty = True
        self.update_surf()

    def update(self):
        pass

class Layer(Render):
    def __init__(self,width:"int", height:"int" , x:"int"=0, y:"int"=0, angle:"int"=0, surf:"pygame.Surface" = None,fill_color:"tuple"=None):
        super().__init__(x, y, width, height, angle, surf)
        self.objs = []
        self.fill_color = fill_color if fill_color != None else (0,0,0,255) 

    def add_obj(self,obj):
        self.objs.append(obj)
    def remove_obj(self,obj):
        if obj in self.objs:
            self.objs.remove(obj)
        else:
            loger.error(f"obj {obj} is not in layer {self.id}")
    def get_obj_from_id(self,obj_id:int):
        for obj in self.objs:
            if obj.id == obj_id:
                return obj
    def get_obj_from_index(self,index:int):
        try:
            return self.objs[index]
        except IndexError:
            loger.log(f"index {index} not in Layer {self.id}'s list")
            return None

    def _update_objs(self):
        self.OG_image.fill(self.fill_color)
        for i,obj in enumerate(self.objs):
            obj.force_update()
            self.OG_image.blit(obj.image,obj.get_pos())
        self.force_update()

    def update(self):
        self._update_objs()


class Chunk(Layer):
    def __init__(self, cx = 0, cy = 0, angle = 0,chunk_size=0, surf=None, fill_color=None,update_method:"callable"=None):
        self.cx,self.cy = cx,cy
        x,y = (cx * chunk_size),(cy * chunk_size)
        self.update_method = update_method if update_method != None else lambda s : None

        super().__init__(chunk_size, chunk_size, x, y, angle, surf, fill_color)

    def gen_chunk(self,genorator:"callable"=None):
        if genorator != None:
            return
        genorator(self)
    
    def update(self):
        self.update_surf()
        self.update_method(self)

    
class Chunked_Layer(Render):
    def __init__(self, x, y, width, height, angle, surf = None,chunk_size:int=0,chunk_updateor:"callable"=None,chunk_genorator:"callable"=None,chunk_fill_color=(0,0,0)):
        self.chunk_size = chunk_size
        self.fill_color = chunk_fill_color
        self._tiles = {}
        self._chunk_genorator = chunk_genorator if chunk_genorator != None else lambda s:None
        self._chunk_update_method = chunk_updateor if chunk_updateor != None else lambda s:None
        super().__init__(x, y, width, height, angle, surf)

    def _gen_tile(self,cx:int,cy:int):
        tile = Chunk(cx,cy,0,self.chunk_size,update_method=self._chunk_update_method,fill_color=self.fill_color) 
        tile.gen_chunk(self._chunk_genorator)
        return tile
    
    def get_tile(self,cx:int,cy:int):
        """returns the tile at the (cx,cy)"""
        if (cx,cy) in self._tiles:
            return self._tiles[(cx,cy)]
        self._tiles[(cx,cy)] = self._gen_tile(cx,cy)
    
    def cpos_to_pos(self,cx:int,cy:int):
        "converts chunk pos to normal pos"
        return (cx*self.chunk_size,cy*self.chunk_size)
    def pos_to_cpos(self,x,y):
        """converts a pos to chunk pos"""
        return (x // self.chunk_size , y // self.chunk_size)

    def chunk_obj(self,obj:"Render"):
        pos = obj.get_pos()
        cpos = self.pos_to_cpos(pos[0],pos[1])
        tile = self.get_tile(cpos[0],cpos[1])
        tile.add_obj(obj)
    
    def re_chunk(self,cx,cy):
        """this will remove and re chunk all obs in chunk (do not call every frame)"""
        tile = self.get_tile(cx,cy)
        objs = tile.objs
        tile.objs.clear()
        for obj in objs:
            self.chunk_obj(obj)
    def rechunk_all_chunks(self):
        for cpos in self._tiles.keys():
            self.re_chunk(cpos[0],cpos[1])

    def _render_visable_chunks(self):
        rect_x,rect_y,rect_w,rect_h = self.rect.x,self.rect.y,self.rect.width,self.rect.height
        
        crect_x,crect_y = self.pos_to_cpos(rect_x,rect_y)
        crect_bx,crect_by = self.pos_to_cpos((rect_x + rect_w),(rect_y + rect_h))

        for cy in range(crect_y,crect_by):
            for cx in range(crect_x,crect_bx):
                tile = self.get_tile(cx,cy)
                tile.update()
                self.OG_image.blit(tile.image,tile.get_pos())

        self.force_update()

    def update(self):
        self._render_visable_chunks()
        


class Display_Manager(Class_Data):
    def __init__(self,window_size:"tuple",display_size:"tuple",force_full_screen:bool=False,window_name:str="skyport-engine window",window_ico:"pygame.Surface"=None,resizable:bool=True,root_layer=None):
        super().__init__()

        self._locks = {
            "target_fps":threading.Lock(),
            "running":threading.Lock(),
            "display":threading.Lock(),
            "root_layer":threading.Lock()
        }
        self.root_layer = root_layer if root_layer != None else Layer(display_size[0],display_size[1])
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

    def _update_root_layer(self):
        self.root_layer.update()
        self.display.blit(
            self.root_layer.get_surf(),
            self.root_layer.get_pos()
        )

    def update_window(self):
        """this manually updates the window (do not call this after starting rendering thread bc the rendering thread already dose)"""
        with self._locks["root_layer"]:
            self._update_root_layer()
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
        self._locks = {
            "target_fps":threading.Lock(),
            "running":threading.Lock(),
            "display":threading.Lock(),
            "root_layer":threading.Lock()
        }
        self.root_layer = root_layer if root_layer != None else Layer(display_size[0],display_size[1])
        self._user_clock = pygame.time.Clock()
        self.rendering_thread = None
        self.keybinds = {"up":{},"down":{},"buttons":{}}
        self.loops = 0
        self.target_fps = 60
        self.running = False
        self._display_dirty = True

        self.window_name = window_name
        self._window_ico = window_ico
        self._force_full_screen = force_full_screen
        self.resizeable_window = resizable
        self._display_size = display_size
        self.window_size = window_size

        self.display = pygame.Surface(display_size)
        self.__clock = pygame.time.Clock()

    def _couculate_window_scaling(self):

        self.window_width, self.window_height = self.window.size
        self.display_rect = self.display.get_rect(center=(self.window_width // 2, self.window_height // 2))
        self._scale = min(self.window_width / self.display.get_width(), self.window_height / self.display.get_height())
        self._new_size = (int(self.display.get_width() * self._scale), int(self.display.get_height() * self._scale))
        self._W_pos = ((self.window_width - self._new_size[0]) // 2, (self.window_height - self._new_size[1]) // 2)

        self._dest_rect = (*self._W_pos, *self._new_size)  

    def update_window(self):
        """this manually updates the window (do not call this after starting rendering thread bc the rendering thread already dose)"""
        with self._locks["root_layer"]:
            self._update_root_layer()
        self.loops += 1
        with self._locks["display"]:
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
                    with self._locks["display"]:
                        print(f"resize to ({event.x},{event.y})")
                        self._couculate_window_scaling()
                        self._display_texture = video.Texture(self._render, self._display_size)
                        self._display_dirty = True

                if event.type == pygame.KEYDOWN:
                    funcs = self.keybinds["down"].get(event.key,[lambda : loger.log(f"key {event.key} is not bound (keydonw)")])
                    self._exacute_funcs(funcs)
                if event.type == pygame.KEYUP:
                    funcs = self.keybinds["up"].get(event.key,[lambda : loger.log(f"key {event.key} is not bound (keyup)")])
                    self._exacute_funcs(funcs)
        except Exception as e:
            loger.log(f"error in event handeling: {e}")
            events = []



