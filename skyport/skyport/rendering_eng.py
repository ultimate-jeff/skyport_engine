
import json
import os
import sys
import threading

# engine imports and setup
from skyport.core.paths import PathUtil as pu
from skyport.core.paths import loger

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
   sys.path.insert(0, BASE_DIR)

from skyport.core.paths import pygame

pygame.display.init()
pygame.display.set_mode((1, 1), pygame.HIDDEN)

from skyport.assets.layar_manager import Layar_manager
from skyport.assets.layar_manager import Camera

from skyport.global_utils import (
    Delta_timer, Util, Loader, r_obj, Sprite, 
    prin_RESET, prin_RED, prin_GREEN, prin_BLUE,
    loader,util,loger
)

class Display_manager:
    def help():
        print("""the display manager handles almoast every aspect of the pygame display and contains the folowing methods
        get_gamestate(): this methods gives you the engine curent gamestate (LINK:gamestates),
        add_gamestate(name,lm): this method adds a gamestate (LINK:gamestates) to the engine (lm stands for layarmanager)
        remove_game_state(name): this delets a gamestate (LINK:gamestates)
        get_mouse_pos() this gets the cursurs position on the display 
        START_RENDERING_THREAD(fps): this starts the rendering thread and the engine gets to work
        STOP_RENDERING_THREAD() this stops the rendering thread 
        event() this method contains the event handler for the engine/window 

        LINKS:
        gamestates: a gamestate is a layarmanager which holds all the layars and objs of that gamestate and only the 
            active gamestate is renderd 
        """)
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
        self.window = pygame.display.set_mode(window_size,pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.RESIZABLE)
        pygame.display.set_icon(self.window_ico) if self.window_ico else None
        pygame.display.set_caption(window_name)
        lm = Layar_manager(self.display)
        self.dt = Delta_timer()
        self.util = Util()
        self.print_que = ""
        self.curent_game_state = "main"
        self.game_states = {self.curent_game_state:lm}

        if not pygame.display.is_fullscreen() and force_full_screen:
            pygame.display.toggle_fullscreen()

        self._couculate_window_scaling()
        loger.log("Display manager initialized")
    
    def get_gamestate(self):
        return self.game_states[self.curent_game_state]
    def add_gamestate(self,name,lm):
        self.game_states[name] = lm
        loger.log(f"added game state {name}")
    def remove_game_state(self,name):
        if name in self.game_states:
            del self.game_states[name]
            loger.log(f"removed game state {name}")
        else:
            loger.log(f"tried to remove game state {name} but it does not exist")

    def _cclock(self,TFPS):
        #self._event()
        self.loops += 1
        self.s_display = pygame.transform.scale(self.display, self.new_size)
        self.window.blit(self.s_display,self.W_pos)
        Util.print(f"loops are at {self.loops} and fps is at {self.clock.get_fps():.2f}")
        pygame.display.flip()
        self.clock.tick(TFPS)

    def _couculate_window_scaling(self):
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

    def _render(self):
        self.display.blit(self.game_states[self.curent_game_state].render(),(0,0))

    def _rendering_loop(self):
        try:
            while not self._stop_event.is_set():
                self._render()
                self._cclock(self.fps)
                self.dt.get_dt()
        except Exception as e:
            print(f"exiting render loop do to {e}")
            loger.log(f"exiting render loop do to {e}")

    def START_RENDERING_THREAD(self, fps):
        self.fps = fps
        self._stop_event.clear() 
        self.rendering_thread = threading.Thread(target=self._rendering_loop, daemon=True)
        self.rendering_thread.start()
        loger.log("Rendering thread started")

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
                    self._couculate_window_scaling()
        except Exception as e:
            loger.log(f"error in event handeling: {e}")

class GSTI:
    lloader = loader# GSTI stands for: Game State Config Interpriter
    def help():
        print("""
        example placement map
        'o' stands for override so it will use a declaration but u can override the declarations
            attars by having some of your own
        'm' stands for manual this placement has all the requierd attars
        'd' stands for defalt this takes a declaration but you must provide the pos
        {
          "obj_declarations": {
            "jeff": {
              "size": [ 50, 50 ],
              "hitbox_size": [ 50, 50 ],
              "angle": 45,
              "image_path": "planes/pt-17/pt-17.png"
            }

          },
          "placement": [
            {
              "type": "m",
              "pos": [ 5, 5 ],
              "size": [ 50, 50 ],
              "hitbox_size": [ 50, 50 ],
              "angle": 0,
              "image_path": "planes/pt-17/pt-17.png",
              "lable": null
            },
            {
              "type": "o",
              "pos": [ 50, 50 ],
              "lable": "jeff"
            }
          ]
        }
        """)
    def __init__(self,fp,lm:"Layar_manager",layar_pryoraty=0):
        """u pass in a placement map and it will automaticly place all objs in the map"""
        self.lm = lm
        self.fp = fp
        self.layar_pryoraty = layar_pryoraty
        self.data = GSTI.lloader.data(fp)
        #self.load_placements()

    def load_placements(self):
        objs = []
        timer = Delta_timer()
        declarations = self.data["obj_declarations"]
        for data in self.data["placement"]:
            T = data["type"].lower()
            if T == "m":
                objs.append(self._M_cunstruct(data,declarations))
            elif T == "d":
                objs.append(self._D_cunstruct(data,declarations))
            elif T == "o":
                objs.append(self._O_cunstruct(data,declarations))
        self._add(objs)
        print(f"compleet with placement at {timer.get_dt()}")

    
    def _O_cunstruct(self,data,declarations):
        value = declarations[data["lable"]]
        pos = self._get_attar(data,value,"pos")
        size = self._get_attar(data,value,"size")
        hitbox_size = self._get_attar(data,value,"hitbox_size")
        angle = self._get_attar(data,value,"angle")
        image_path = self._get_attar(data,value,"image_path")
        return self._make_obj(pos,size,hitbox_size,angle,image_path)
    def _M_cunstruct(self,data,declarations):
        #value = declarations[data["lable"]]
        pos = data["pos"]
        size = data["size"]
        hitbox_size = data["hitbox_size"]
        angle = data["angle"]
        image_path = data["image_path"]
        return self._make_obj(pos,size,hitbox_size,angle,image_path)
    def _D_cunstruct(self,data,declarations):
        value = declarations[data["lable"]]
        pos = data["pos"]
        size = self._get_attar(data,value,"size")
        hitbox_size = self._get_attar(data,value,"hitbox_size")
        angle = self._get_attar(data,value,"angle")
        image_path = self._get_attar(data,value,"image_path")
        return self._make_obj(pos,size,hitbox_size,angle,image_path)

    def _make_obj(self,pos,size,hitbox_size,angle,image_path):
        hit_box_rect = pygame.rect.Rect(pos[0],pos[1],hitbox_size[0],hitbox_size[1])
        return r_obj(pos[0],pos[1],size[0],size[1],angle,2,image_path,hit_box_rect)
        
    def _get_attar(self,data,value,attar_name,biost=0):
        if attar_name in data:
            ddata = data[attar_name]
        else:
            ddata = value[attar_name]
        return ddata

    def _add(self,all_objs):
        for obj in all_objs:
            self.lm.add_obj(obj,self.layar_pryoraty)


    def _create_obj_declaration(self,obj):
        data = {"type":"m","pos":(obj.x,obj.y),"size":(obj.sx,obj.sy),
         "hitbox_size":(obj.hitbox_rect.width,obj.hitbox_rect.height),
         "angle":obj.angle,"image_path":obj.texture_path,"lable": None
         }
        return data
    def _create_data_map(self,layar_pryoraty):
        layar = self.lm.get_layar(layar_pryoraty)
        chunk_objs,offset_objs = self.lm.get_layar_objs(layar)
        all_objs = chunk_objs+offset_objs
        all_data = []
        for obj in all_objs:
            data = self._create_obj_declaration(obj)
            all_data.append(data)
        return all_data

    # -------------- ai made --------------------------------------------
    def _find_simular_objs(self, all_objs):
        """God-level: Automatically mines patterns and structures the final JSON."""
        from collections import Counter
        # 1. Count occurrences of each image to identify 'Archetypes'
        path_counts = Counter([obj.texture_path for obj in all_objs])
        
        final_json = {
            "obj_declarations": {},
            "placement": []
        }
        # Use a helper to track which labels we've already created
        path_to_label = {}
        for obj in all_objs:
            path = obj.texture_path
            
            # DECISION: Is this common enough to be a Declaration? (Threshold: 2+ occurrences)
            if path_counts[path] > 1:
                # Get or Create the Declaration
                if path not in path_to_label:
                    label = self._generate_unique_label(path, final_json["obj_declarations"])
                    path_to_label[path] = label
                    final_json["obj_declarations"][label] = {
                        "size": [obj.sx, obj.sy],
                        "hitbox_size": [obj.hitbox_rect.width, obj.hitbox_rect.height],
                        "angle": 0, # Baseline angle is always 0
                        "image_path": path
                    }
                # Add to placements as 'd' or 'o'
                label = path_to_label[path]
                final_json["placement"].append(self._get_optimized_placement(obj, label, final_json["obj_declarations"][label]))
            else:
                # Rare object: Save as manual 'm'
                final_json["placement"].append(self._create_obj_declaration(obj))      
        return final_json
    def _generate_unique_label(self, path, existing_decs):
        """Creates a clean, readable name from a file path."""
        base = path.split('/')[-1].split('.')[0] # 'pt-17.png' -> 'pt-17'
        name = base
        counter = 1
        while name in existing_decs: # Avoid name collisions
            name = f"{base}_{counter}"
            counter += 1
        return name
    def _get_optimized_placement(self, obj, label, declaration):
        """Determines if the instance is a Default (d) or an Override (o)."""
        # A 'Default' only changes position. 
        # An 'Override' is used if Angle, Size, or Hitbox differs from the Declaration.
        is_standard = (obj.angle == declaration["angle"] and 
                       [obj.sx, obj.sy] == declaration["size"])
        data = {
            "type": "d" if is_standard else "o",
            "lable": label,
            "pos": [obj.x, obj.y]
        }
        if not is_standard:
            # Only add what actually changed
            if obj.angle != declaration["angle"]: data["angle"] = obj.angle
            if [obj.sx, obj.sy] != declaration["size"]: data["size"] = [obj.sx, obj.sy]  
        return data
    # ---------------------------------------------------------------

    def save_placement_map(self,layar_pryoraty,save_file_path):
        all_data = self._create_data_map(layar_pryoraty)
        json_data = self._find_simular_objs(all_data)
        with open(save_file_path,"w") as f:
            json.dump(json_data,f,indent=4)
        print("saved placement map")

