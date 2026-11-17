

#from skyport.global_utils import *
from .imports import *
from .global_utils import (
    Interacotr,
    logger,
    Class_Data,
    Delta_timer
)
from pygame import _sdl2 as video

pygame.display.init()
pygame.joystick.init()
pygame.font.init()

pygame.display.set_mode((1, 1), pygame.HIDDEN)

class Render(Class_Data):

    def __init_texture(self,surf,width,height):
        self.surf = surf if surf != None else pygame.Surface((width,height),flags=pygame.SRCALPHA).convert_alpha()
        self.OG_image = self.surf

    def __init__(self,x:"int",y:"int",width:"int",height:"int",angle:"int",surf:"pygame.Surface"=None,tags:dict=None,_auto_init_update=True):
        """this class is meant to be inherited by other classes or used in them so like class MyGameObj(Render): ...."""
        Class_Data.__init__(self,tags)
        #self._base_init()
        self.rect = pygame.Rect(x,y,width,height)
        self.angle = angle
        self.__init_texture(surf,width,height)
        self._last_angle = None
        self._last_size = None
        self._is_dirty = True
        self._lock = threading.Lock()
        if _auto_init_update:
            self.update_surf(True)

    def _scale(self,size,dirty):
        should_scale = (dirty or size != self._last_size)
        with self._lock:
            surf = self.surf
        if should_scale:
            if size == surf.get_size():
                self._scaled_image = surf
            else:
                self._scaled_image = pygame.transform.scale(self.surf, size)
            self._last_size = size
        return should_scale

    def _rotate(self,should_scale,angle):
        if should_scale | (angle != self._last_angle):
            if angle % 360 == 0:
                self.image = self._scaled_image
            else:
                self.image = pygame.transform.rotate(self._scaled_image, angle)
            self._last_angle = angle

    def update_surf(self, forced=False):
        dirty = self._is_dirty | forced
        self._is_dirty = False
        #if dirty | should_scale:
        self._rotate(self._scale(self.rect.size,dirty),self.angle)

    def set_angle(self,new_angle:"int"):
        """sets angle and automaticly updates the surf"""
        self.angle = new_angle
        self._is_dirty = True

    def set_rect(self,new_rect:pygame.Rect):
        """sets the rect and automaticly updates the surf"""
        self.rect = new_rect
        self._is_dirty = True

    def get_pos(self) -> tuple:
        return (self.rect.x,self.rect.y)
    
    def set_pos(self,x,y):
        self.rect.x,self.rect.y = x,y

    def get_size(self) -> tuple:
        return self.rect.size
    
    def set_size(self,new_size):
        """this sets the size and automaticly updates the surf"""
        self.rect.size = new_size
        self._is_dirty = True

    def get_surf(self) -> pygame.Surface:
        return self.surf
    
    def blit(self,source: "pygame.Surface", dest: "pygame.RectLike" = (0, 0), area: "pygame.RectLike" = None, special_flags: "int" = 0):
        """blits to surf and auto updates ( this uses locks for thread safty do not call in high speed loops)"""
        with self._lock:
            self._is_dirty = True
            self.surf.blit(source,dest,area,special_flags)
        #self.update_surf(True)
    def fill(self,color:"tuple"=(0,0,0,0),rect:"pygame.Rect"=None,special_flags:"int"=0):
        """fills surf and auto updates ( this uses locks for thread safty do not call in high speed loops)"""
        with self._lock:
            self._is_dirty = True
            self.surf.fill(color,rect,special_flags)
        #self.update_surf(True)
    def blits(self,blit_sequence:"list[pygame.Surface, pygame.RectLike]", doreturn:"int | bool" = 1):
        """this is self.surf.blits but with a thread safty lock"""
        with self._lock:
            self._is_dirty = True
            self.surf.blits(blit_sequence,doreturn)

    def force_update(self):
        self.update_surf(True)

    def update(self,*args,**kwargs):
        pass

class Layer(Render):
    def __init__(self,width:"int", height:"int" , x:"int"=0, y:"int"=0, angle:"int"=0, surf:"pygame.Surface" = None,fill_color:"tuple"=None,fill_every_frame=True,tags=None):
        super().__init__(x, y, width, height, angle, surf,tags=tags)
        self.objs = []
        self.fill_color = fill_color if fill_color != None else (0,0,0,0) 
        self.fill_every_frame = fill_every_frame

    def set_fill_color(self,color:"tuple"):
        self.fill_color = color

    def add_obj(self,obj):
        """adds an object"""
        if obj == self:
            logger.error(f"cannot add self to self")
        self.objs.append(obj)
    def remove_obj(self,obj):
        """removes an object"""
        if obj in self.objs:
            self.objs.remove(obj)
        else:
            logger.error(f"obj {obj} is not in layer {self.id}")
    def get_obj_from_id(self,obj_id:int):
        """gets an object from the id"""
        objs = self.objs
        for obj in objs:
            if obj.id == obj_id:
                return obj
    def get_obj_from_index(self,index:int):
        """gets an object from an index"""
        try:
            return self.objs[index]
        except IndexError:
            logger.log(f"index {index} not in Layer {self.id}'s list")
            return None
        
    def clear(self):
        self.objs.clear()

    def _update_obj(self,obj,events,forced=True,*args,**kwargs):
        obj._update_(events,*args,**kwargs)
        obj.update(*args,**kwargs)
        obj.update_surf(forced)

    def _update_objs(self,events,forced_update=False,*args,**kwargs):
        objs = self.objs
        _update_obj = self._update_obj
        if self.fill_every_frame:
            self.surf.fill(self.fill_color)
        for obj in self.objs:
            _update_obj(obj,events=events,forced=forced_update,*args,**kwargs)
            #self.surf.blit(obj.image,obj.image.get_rect(center=obj.rect.center))
        self.surf.blits(
            [(o.image, (o.rect.centerx - o.image.get_width() // 2, o.rect.centery - o.image.get_height() // 2)) for o in objs],doreturn=False,)
        self._is_dirty = True

    def _update_(self,events,*args,**kwargs):
        self._update_objs(events,False,*args,**kwargs)
        #self._handle_events(events)


class Chunk(Layer):
    def __init__(self, cx = 0, cy = 0, angle = 0,chunk_size=1, surf=None, fill_color=None,update_method:"callable"=None):
        self.cx,self.cy = cx,cy
        x,y = (cx * chunk_size),(cy * chunk_size)
        self.update_method = update_method if update_method != None else lambda s : None
        self._base_image = None
        super().__init__(chunk_size, chunk_size, x, y, angle, surf, fill_color)

    def gen_chunk(self, genorator=None):
        if genorator is None:
            return
        genorator(self)
        self._base_image = self.surf.copy()
    
    def _update_(self,events,forced_update=False,*args,**kwargs):
        self.surf = self._base_image.copy() 
        for obj in self.objs:
            self._update_obj(obj,events=events,forced=forced_update,*args,**kwargs)
            self.surf.blit(obj.image, obj.get_pos())
        self.update_method(self)
        #self.update_surf(True)
        self._is_dirty = True

        #self._handle_events(events)
    
class Chunked_Layer(Render):
    def __init__(self, x, y, width, height, angle=0, surf = None,chunk_size:int=0,chunk_updateor:"callable"=None,chunk_genorator:"callable"=None,chunk_fill_color=(0,0,0)):
        self.chunk_size = chunk_size
        self.fill_color = chunk_fill_color
        self._tiles = {}
        self._chunk_genorator = chunk_genorator if chunk_genorator != None else lambda s:None
        self._chunk_update_method = chunk_updateor if chunk_updateor != None else lambda s:None
        self.camera_x = 0
        self.camera_y = 0
        super().__init__(x, y, width, height, angle, surf)

    def set_camera_pos(self,new_x,new_y):
        self.camera_x,self.camera_y = new_x,new_y
    
    def get_existing_tile(self,cx,cy):
        if (cx,cy) in self._tiles:
            return self._tiles[(cx,cy)]
    
    def get_tile(self,cx:int,cy:int):
        """returns the tile at the (cx,cy)"""
        if (cx,cy) not in self._tiles:
            tile = Chunk(cx,cy,0,self.chunk_size,update_method=self._chunk_update_method,fill_color=self.fill_color) 
            self._tiles[(cx,cy)] = tile
            tile.gen_chunk(self._chunk_genorator)
        return self._tiles[(cx,cy)]
    
    def remove_tile(self,cx,cy):
        if (cx,cy) in self._tiles:
            self._tiles.pop((cx,cy))
            return
        logger.log(f"chunk ({cx},{cy}) dose not exsist in Chunk_Layer {self.id}")
    
    def cpos_to_pos(self,cx:int,cy:int):
        "converts chunk pos to normal pos"
        return (cx*self.chunk_size,cy*self.chunk_size)
    def pos_to_cpos(self,x,y):
        """converts a pos to chunk pos"""
        return (x // self.chunk_size , y // self.chunk_size)

    def chunk_obj(self,obj:"Render"):
        if obj == self:
            logger.error(f"cannot chunk obj self into self")
        pos = obj.get_pos()
        cpos = self.pos_to_cpos(pos[0],pos[1])
        tile = self.get_tile(cpos[0],cpos[1])
        tile.objs.append(obj)
    
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

    def re_chunk_visable(self):
        crect_x,crect_y,crect_bx,crect_by = self._get_render_range()
        for cy in range(crect_y,crect_by+ 1):
            for cx in range(crect_x,crect_bx + 1):
                self.re_chunk(cx,cy)

    def _get_render_range(self):
        rect_w,rect_h = self.rect.width,self.rect.height
        crect_x,crect_y = self.pos_to_cpos(self.camera_x,self.camera_y)
        crect_bx,crect_by = self.pos_to_cpos((self.camera_x + rect_w),(self.camera_y + rect_h))
        return crect_x,crect_y,crect_bx,crect_by

    def _render_visable_chunks(self,events,*args,**kwargs):
        self.surf.fill(self.fill_color)

        crect_x,crect_y,crect_bx,crect_by = self._get_render_range()

        #print(f"cx,cy -> {crect_x},{crect_y} :: {crect_bx},{crect_by}")
        for cy in range(crect_y,crect_by+ 1):
            for cx in range(crect_x,crect_bx + 1):
                tile = self.get_tile(cx,cy)
                tile._update_(events,args,kwargs)
                tile.update(args,kwargs)
                x,y = tile.rect.x,tile.rect.y
                self.surf.blit(tile.image,(x- self.camera_x,y - self.camera_y))

        self.update_surf(True)

    def _update_(self,events,*args,**kwargs):
        self._render_visable_chunks(events)
        #self._handle_events(events)

class Camera(Layer):
    def __init__(self, width, height,world_width,world_height, x = 0, y = 0, angle = 0, surf = None, fill_color = None,cx=0,cy=0,zoom=1):
        super().__init__(width, height, x, y, angle,None, fill_color)
        self.world_width = world_width
        self.world_height = world_height
        self.camera_x,self.camera_y = cx,cy
        self.zoom = zoom
        self._last_zoom = None
        self.map = surf if surf != None else pygame.Surface((world_width,world_height),pygame.SRCALPHA)

    def _scale_map(self):
        if self._last_zoom != self.zoom:
            self._last_zoom = self.zoom
            nsx,nsy = self.map.get_size()
            nsx = math.ceil(nsx * self.zoom)
            nsy = math.ceil(nsy * self.zoom)
            self._scaled_map = pygame.transform.scale(self.map,(nsx,nsy))

    def _update_objs(self,events,forced_update=True,*args,**kwargs):
            self.map.fill(self.fill_color)
            for i,obj in enumerate(self.objs):
                self._update_obj(obj,events=events,forced=forced_update,*args,**kwargs)
                img_rect = obj.image.get_rect(center=obj.rect.center)
                self.map.blit(obj.image,img_rect)
            self.update_surf(True)

    def _render_map(self):
        self._scale_map()
        view_rect = pygame.Rect(self.camera_x*self.zoom, self.camera_y*self.zoom, self.width, self.height)
        self.surf.fill(self.fill_color)
        self.surf.blit(self._scaled_map, (0, 0), area=view_rect)

    def _update_(self,events,*args,**kwargs):
            self._update_objs(events,False)
            self._render_map()
            
            #self._handle_events(events)

    def set_cam_pos(self, new_x, new_y):
        max_x = max(0, self.world_width - self.width / self.zoom - 0.01)
        max_y = max(0, self.world_height - self.height / self.zoom - 0.01)
        self.camera_x = max(0, min(new_x, max_x))
        self.camera_y = max(0, min(new_y, max_y))

    def get_cam_pos(self):
        return (self.camera_x,self.camera_y)
        
class Font_Render(Render):
    Sys_fonts = pygame.font.get_fonts()
    def __init__(self,font:"pygame.font.Font", text:str ,x:"int", y:"int", width:"int", height:"int",text_color:"tuple"=(0,0,0),font_size:"int"=50, angle:"int"=0,tags:dict=None,word_wrapping:bool=True,bg_color:"tuple"=(0,0,0,0)):
        self.text = text
        self.text_color = text_color
        self._last_text = None
        self.font = font
        self.word_wrapping = word_wrapping
        self.bg_color = bg_color
        super().__init__(x=x, y=y, width=width, height=height, angle=angle,tags=tags)
        self.update_text()

    def _word_wrapping_text_render(self):
        #self.OG_image.fill(self.bg_color)
        collection = [word.split(" ") for word in self.text.splitlines()]
        space = self.font.size(' ')[0]
        #wh = self.font.get_height()

        #self.OG_image = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        self.surf.fill(self.bg_color)

        x,y = 0,0
        for line in collection:
            for word in line:
                w_surf = self.font.render(word,True,self.text_color)
                ww,wh = w_surf.get_size()
                if x + ww >= self.rect.width:
                    x = 0
                    y += wh
                self.surf.blit(w_surf,(x,y))
                x += ww + space
            x = 0
            y += wh

    def update_text(self):
        if self._last_text != self.text:
            if self.word_wrapping:
                self._word_wrapping_text_render()
            else:
                self.surf = self.font.render(self.text,True,self.text_color,self.bg_color)
            self._is_dirty = True
            self._last_text = self.text

    def update_surf(self,forced=False):
            """this updates the self.image so that it is the corect scale and angle"""
            self.update_text()
            dirty = self._is_dirty | forced
            self._is_dirty = False
            #should_scale = (dirty or size != self._last_size)
            self._rotate(self._scale(self.rect.size,dirty),self.angle)
            self._is_dirty = False

class Animated_Render(Render):
    def __init__(self, x, y, width:"int", height:"int", angle:"int"=0, frames:"list"=None,fps:"int"=1,starting_frame:"int"=0,surf=None,loops:int=1, tags=None):
        self.frame_index = starting_frame
        #self._last_frame_index = None
        self._frame_duration  = 1 / fps if fps > 0 else 0.0000000001
        self.fps = fps
        self.loops = loops
        self.playing = True
        self._elapsed = 0
        if not isinstance(frames,(list,tuple)):
            logger.error(f"wrone type for frames",TypeError,2)
            self.frames = [surf if surf != None else pygame.Surface((width,height))]
        else:
            self.frames = frames
        self._total_frames = len(frames)
        self.dt = Delta_timer()
        super().__init__(
            x, y,
            width, height, 
            angle, 
            surf, 
            tags
        )

    def _update_frame_index(self):
        self._elapsed += self.dt.get_dt()
        if self._elapsed >= self._frame_duration:
            self._elapsed = 0
            new_fi = (self.frame_index + 1) % self._total_frames
            if abs(self.frame_index - new_fi) > 1:
                self.loops -= 1
            if self.loops > 0:
                self.frame_index = new_fi
            self._is_dirty = True
        return self.frame_index

    def _update_(self,events,*args,**kwargs):
        pass
        #self._handle_events(events)
        #self._update_frame_index()
        #self.OG_image = (self.frames[self.frame_index])

    def update_surf(self, forced=False):
        """this updates the self.image so that it is the corect scale and angle"""
        self._update_frame_index()
        self.surf = (self.frames[self.frame_index])
        dirty = self._is_dirty | forced
        self._is_dirty = False
        self._rotate(self._scale(self.rect.size,dirty),self.angle)

class Interactor_Render(Render,Interacotr):
    def __init__(self, x, y, width, height, angle, surf = None, tags=None):
        Render.__init__(self,x,y,width,height,angle,surf,tags)
        Interacotr.__init__(self)
        #self._base_init()
class Interactor_Layer(Layer,Interacotr):
    def __init__(self, width, height, x = 0, y = 0, angle = 0, surf = None, fill_color = None, fill_every_frame=True, tags=None):
        Layer.__init__(self,width, height, x, y, angle, surf, fill_color, fill_every_frame, tags)
        Interacotr.__init__(self)

class Display_Manager(Class_Data):
    def _base_init(self):
        self._locks = {
            "target_fps":threading.Lock(),
            "running":threading.Lock(),
            "display":threading.Lock(),
            "event":threading.Lock(),
            "update":threading.Lock()
        }
        self.keybinds = {
            pygame.KEYUP:{},
            pygame.KEYDOWN:{},
            "buttons":{},
            pygame.JOYBUTTONUP:{},
            pygame.JOYBUTTONDOWN:{},

            }
        self.event_que = {}
        self.update_args_que = []
        self.update_kwargs_que = {}
        self.joysticks = []
        self.__clock = pygame.time.Clock()
        self._user_clock = pygame.time.Clock()

    def __init__(self,window_size:"tuple",display_size:"tuple",force_full_screen:bool=False,window_name:str="skyport-engine window",window_ico:"pygame.Surface"=None,resizable:bool=True,root_layer=None,post_render_hook=None,pre_render_hook=None):
        super().__init__()
        self._base_init()
        self.rendering_thread = None
        self.loops = 0
        self.target_fps = 60
        self.running = False
        self.resizeable_window = resizable
        self._display_size = display_size
        self.window_size = window_size
        self._s_display = None

        self.update__root_layers = True
        self.post_render_hook = post_render_hook
        self.pre_render_hook = pre_render_hook

        self.display = pygame.Surface(display_size).convert()
        self.root_layer = root_layer if root_layer != None else Layer(display_size[0],display_size[1],surf=self.display,fill_color=(0,0,0))
        self.window = pygame.display.set_mode(window_size,pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.RESIZABLE if resizable else 0)
        pygame.display.set_icon(window_ico) if window_ico else None
        pygame.display.set_caption(window_name)

        if not pygame.display.is_fullscreen() and force_full_screen:
            pygame.display.toggle_fullscreen()
        self._couculate_window_scaling()
        self._couculate_display_center()
        self._window_size = pygame.display.get_window_size()

    def tick(self,tps):
        self._user_clock.tick(tps)

    def set_update_args_kwargs(self,*args,**kwargs):
        self.update_args_que = args
        self.update_kwargs_que = kwargs
    def clear_update_args_kwargs(self):
        self.update_args_que.clear()
        self.update_kwargs_que.clear()

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

    def update_root_layer(self,*args,**kwargs):
        """this updates the rood layer but do not call unless you set update__root_layers to False and want to manualy manage Render updating """
        #self.root_layer._update_objs(self.event_que,False,args=args,kwargs=kwargs)
        root_layer = self.root_layer 
        root_layer._update_obj(root_layer,self.event_que,False,*args,**kwargs)
        rect = self.root_layer.rect
        if root_layer.image is not self.display:
            self.display.blit(
                root_layer.image,
                (rect.x,rect.y)
            )
    def update_window(self,*args,**kwargs):
        """this manually updates the window (do not call this after starting rendering thread bc the rendering thread already dose)
        # what args and kwargs do:
        the args and kwargs peramiters get passed throught every .uodate and ._update_ method in the rendering pipeline
        """
        with self._locks["update"]:
            self.loops += 1

            if self.pre_render_hook:
                self.pre_render_hook(self)
            if self.update__root_layers:
                self.update_root_layer(*args,**kwargs)
            if self.post_render_hook:
                self.post_render_hook(self)

            new_size = self._new_size
            display_pos = self._W_pos
            display = self.display
            if new_size == display.get_size():
                self.window.blit(display,display_pos)
            else:
                buffer = self._s_display
                if buffer == None or buffer.get_size() != new_size:
                    buffer = self._s_display = pygame.Surface(new_size,0,display)
                pygame.transform.scale(display,new_size,buffer)
                self.window.blit(buffer,display_pos)
            pygame.display.flip()
    def create_window(self):
        self.window = self.window = pygame.display.get_surface()

    def _rendering_loop(self):
        self.create_window() #pygame.display.set_mode(self.window_size,pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.RESIZABLE)
        while (self.running):
            self.update_window(*self.update_args_que,**self.update_kwargs_que)
            self.__clock.tick(self.target_fps)    
    def START_RENDERING_THREAD(self, fps):
        """this starts the rendering thread"""
        self.target_fps = fps
        self.running = True
        self.rendering_thread = threading.Thread(target=self._rendering_loop, daemon=True)
        self.rendering_thread.start()
        logger.log("Rendering thread started")
    def STOP_RENDERING_THREAD(self):
        """did you know that this stops the rendering thread"""
        if self.rendering_thread and self.rendering_thread.is_alive():
            self.running = False
            self.rendering_thread.join() 
        logger.log("Rendering thread stopped")

    def quit(self):
        self.running = False
        print("\nquit pressed\n")
        self.STOP_RENDERING_THREAD()
    def _exacute_funcs(self,funcs,*peramiters):
        for func in funcs:
            func(*peramiters)
    def _handle_buttons_keybinds(self):
        buttons = pygame.key.get_pressed()
        binds = self.keybinds["buttons"]
        for bind, funcs in binds.items():
            if buttons[bind]:
                self._exacute_funcs(funcs)
    def _handle_joystick_buttons(self,binds):
        for i,joy in enumerate(self.joysticks):
            for bind , funcs in binds:
                if joy.get_button(bind):
                    self._exacute_funcs(funcs,i)
    def event_handler(self):
        """you will need to call this in your game loop to handle input events like window resizing or keybinds"""
        try:
            with self._locks["event"]:
                self._handle_buttons_keybinds()
                if self.joysticks:
                    self._handle_joystick_buttons(self.keybinds["joy_button_down"])
                    self._handle_joystick_buttons(self.keybinds["joy_button_up"])
                events = pygame.event.get()
                self.event_que = events
                for event in events:
                    if event.type == pygame.KEYDOWN:
                        funcs = self.keybinds[pygame.KEYDOWN].get(event.key,[lambda : logger.log(f"key {event.key} is not bound (keydonw)")])
                        self._exacute_funcs(funcs)
                    if event.type == pygame.KEYUP:
                        funcs = self.keybinds[pygame.KEYUP].get(event.key,[lambda : logger.log(f"key {event.key} is not bound (keyup)")])
                        self._exacute_funcs(funcs)

                    if event.type == pygame.QUIT:
                        self.quit
                    elif event.type == pygame.WINDOWCLOSE:
                        self.quit()
                    if event.type == pygame.VIDEORESIZE:
                        print(event.size)
                        self._couculate_window_scaling()
                        self.window.fill((0,0,0))
                        self._window_size = pygame.display.get_window_size()
                    if event.type == pygame.JOYDEVICEADDED:
                        joy = pygame.joystick.Joystick(event.device_index)
                        self.joysticks.append(joy)
        except Exception as e:
            logger.log(f"error in event handeling: {e}")
            events = []
    def simple_event_handler(self):
        """this is an event handler that dose not have keybids for people who have or want to built there own system"""
        try:
            with self._locks["event"]:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.quit()
                    if event.type == pygame.WINDOWCLOSE:
                        self.quit()
                    if event.type == pygame.VIDEORESIZE:
                        print(event.size)
                        self._couculate_window_scaling()
                        self.window.fill((0,0,0))
                        self._window_size = pygame.display.get_window_size()
        except Exception as e:
            logger.log(f"error in event handeling: {e}")
            events = []

    def update(self,tps=60):
        """this method just combines the event handler and loops speed regulation into 1 method"""
        self.event_handler()
        self.tick(tps)

    def blit(self,source: "pygame.Surface", dest: "pygame.RectLike" = (0, 0), area: "pygame.RectLike" = None, special_flags: "int" = 0):
        """self.display.blit(.....)"""
        #with self._locks["display"]:
        try:
            self.display.blit(source,dest,area,special_flags)
        except Exception as e:
            logger.error(f"failed to blit surf to display due to {e}")
    def fill(self,color:"tuple"=(0,0,0,0),rect:"pygame.Rect"=None,special_flags:"int"=0):
        """self.display.fill(...)"""
        #with self._locks["display"]:
        try:
            self.display.fill(color,rect,special_flags)
        except Exception as e:
            logger.error(f"failed to fill display withg {color} due to {e}")

    # getters and setters 

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
        """this gets fps"""
        if self.rendering_thread == None:
            return self._user_clock.get_fps()
        return self.__clock.get_fps()
    def get_mouse_pos(self) -> "tuple":
            """returns (x,y) of your mouse relative to the window"""
            mx, my = pygame.mouse.get_pos()
            self.mouse_pos = (((mx - self._W_pos[0]) / self._scale),((my - self._W_pos[1]) / self._scale))
            return self.mouse_pos
    # binds 
    
    def _add_bind(self, _type, key, func):
        binds = self.keybinds[_type].setdefault(key, [])  # <-- need this
        if isinstance(func, (list, tuple)):
            binds.extend(func)
        else:
            binds.append(func)

    def add_bind(self,_type,key,func):
        if _type in self.keybinds.keys():
            self._add_bind(_type,key,func)

    def add_keyup_bind(self,key:"int",func:"function"):
        self._add_bind(pygame.KEYUP,key,func)
    def add_keydown_bind(self,key:"int",func:"function"):
        self._add_bind(pygame.KEYDOWN,key,func)
    def add_keypressed_bind(self,key:"int",func:"function"):
        self._add_bind("buttons",key,func)
    def add_joy_button_down_bind(self,button_index:"int",func:"function"):
        """Note the functions must be able to take 1 peramiter of the joystick id"""
        self._add_bind(pygame.JOYBUTTONDOWN,button_index,func)
    def add_joy_button_up_bind(self,button_index:"int",func:"function"):
        """Note the functions must be able to take 1 peramiter of the joystick id"""
        self._add_bind(pygame.JOYBUTTONUP,button_index,func)

    def _remove_bind(self,_type,key,funcs):
        funcs = funcs if isinstance(funcs,(tuple,list)) else [funcs]
        if key not in self.keybinds[_type]:
            logger.log(f"invalid key {key} (try using pygame.K_...)")
            return
        binds = self.keybinds[_type][key]
        for func in funcs:
            try:
                binds.remove(func)
            except ValueError:
                logger.log(f"function to {key} not found. func->{func}")
        if not binds:
            del self.keybinds[_type][key]

    def remove_bind(self,_type,key,funcs):
        if _type in self.keybinds.keys():
            self._remove_bind(_type,key,funcs)

    def remove_keyup_bind(self,key:"int",func:"function"):
        self._remove_bind("up",key,func)
    def remove_keydown_bind(self,key:"int",func:"function"):
        self._remove_bind("down",key,func)
    def remove_keypressed_bind(self,key:"int",func:"function"):
        self._remove_bind("buttons",key,func)
    def remove_joy_button_down_bind(self,button_index,func:"function"):
        self._remove_bind("joy_button_down",button_index,func)
    def remove_joy_button_up_bind(self,button_index,func:"function"):
        self._remove_bind("joy_button_up",button_index,func)


