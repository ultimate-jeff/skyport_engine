"""
made by : Matthew R and William L

////////////////////////////
-----welcome to skyport-----
////////////////////////////

    the purpos of skyport is to:
provide a simpler way to make a 2d game with pygame without having to learn how to use pygame itself.

engine classes:
- Display_manager: main display manager class
- Delta_timer: delta time couculator
- Util: utility functions
- Layar_manager: manager for multiple layers (cameras)
- Camera: layer (camera) class
- r_obj: renderable object class
- Loader: asset loader class
- loger: logging utility
- Sprite: animated texture class

important info:
   -when making chunk genorator funcions make shure that it 
    takes in at least 1 peramiter for the chunk obj it will be called in 
    and the same gose for chunk update funcions.
"""

import os
import sys  
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
   sys.path.insert(0, BASE_DIR)

#from rendering_eng import *
#from global_utils import *
#from assets.layar_manager import *

from .global_utils import Loader
from .global_utils import r_obj
from .global_utils import Sprite
from .global_utils import Util
from .global_utils import Delta_timer

prin_RED = '\033[91m'
prin_GREEN = '\033[92m'
prin_BLUE = '\033[94m'
prin_RESET = '\033[0m'

from .rendering_eng import Display_manager

from .assets.layar_manager import Layar_manager
from .assets.layar_manager import Camera



# example usage:
"""
import random
import time
#import skyport as sp

# 1. Setup Display (Using your scaling logic: 500x500 window -> 1500x750 internal)
dm = sp.Display_manager((500, 500), (1500, 750), False)
loader = sp.Loader(None, "idk_tm.json")
sp.r_obj.loader = loader

# 2. Define a "Chunk Generator" that draws a grid background
def chunk_script(sself):
    sself.bg_image = sp.pygame.Surface((sself.size, sself.size))
    sself.bg_image.fill((30, 30, 30))
    # Draw a grid border so we can see the chunks move
    sp.pygame.draw.rect(sself.bg_image, (50, 50, 50), (0, 0, sself.size, sself.size), 2)
    def update_gen(sself):
        sself.surf.blit(sself.bg_image, (0, 0))
    sself.update_gen_script = update_gen


# 3. Create the Layer (Camera)
# World size: 5000x5000, Chunk size: 250
layar = sp.Camera(dm.display, 250, (5000, 5000), (10, 10, 10), 0, chunk_genorator_func=chunk_script)
dm.get_lm().add_layar(layar)

# 4. Stress Test Variables
objects = []
spawn_rate = 10  # How many objects to add per frame
max_objects = 2000

def spawn_stress_objs(count):
    for _ in range(count):
        # Random position within the 5000x5000 world
        rx = random.randint(0, 4900)
        ry = random.randint(0, 4900)
        # Random size and rotation speed
        obj = sp.r_obj(rx, ry, 40, 40, random.randint(0, 360), 0, "asd.jeff")
        obj.rot_speed = random.uniform(-5, 5)
        dm.get_lm().add_obj(obj, 0)
        objects.append(obj)

# 5. Start the engine
dm.START_RENDERING_THREAD(60) # Capped at 60 for stability, or 0 for unlimited

print("--- SKYPORT ENGINE BENCHMARK STARTING ---")
print("Controls: Arrows to Move, I/K to Zoom, SPACE to spawn 100 more")

try:
    while dm.running:
        time.sleep(0.01) # Low sleep to keep input responsive
        
        # Benchmarking Stats
        fps = dm.clock.get_fps()
        obj_count = len(objects)
        print(f"FPS: {fps:.2f} | Objects: {obj_count} | Cam: ({layar.x}, {layar.y})", end="\r")

        # Automatic Spawning until we hit max
        if obj_count < max_objects and fps > 30:
            spawn_stress_objs(spawn_rate)

        # Update Object Logic (Rotating them to stress the transform.rotate calls)
        for o in objects:
            o.angle += o.rot_speed

        # Input Handling
        keys = sp.pygame.key.get_pressed()
        if keys[sp.pygame.K_LEFT]:  layar.x -= 10
        if keys[sp.pygame.K_RIGHT]: layar.x += 10
        if keys[sp.pygame.K_UP]:    layar.y -= 10
        if keys[sp.pygame.K_DOWN]:  layar.y += 10
        if keys[sp.pygame.K_i]:     layar.set_zoom(layar.zoom + 0.05)
        if keys[sp.pygame.K_k]:     layar.set_zoom(layar.zoom - 0.05)
        if keys[sp.pygame.K_SPACE]: spawn_stress_objs(100)

        dm.event()

except Exception as e:
    # Your "Loving Feature" should catch this!
    print(f"\nBenchmark stopped: {e}")

finally:
    dm.STOP_RENDERING_THREAD()
    print(f"\nFinal Score: Handled {len(objects)} objects at {dm.clock.get_fps():.2f} FPS")


"""