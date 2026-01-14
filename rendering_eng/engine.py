import random
import time
import json
import sys
import os
import pyperclip
import copy
import math
import pygame
import threading


from assets import layar_manager as lm
from global_utils import *


# 1. Setup your display and layer as you did in your snippet
display = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
LM = lm.layar_manager(display)
LM.add_layar("jeffy1",(50,50),(2000,2000),display.get_size())
LM.add_layar("jeffy2",(50,50),(2000,2000),display.get_size())
l = LM.get_layar("jeffy1")
L = LM.get_layar("jeffy2")
LM.get_rendering_surfs()
l.layar.zoom = 0.9
L.layar.zoom = 0.9
for i in range(500):
    start_time = time.time()
    l.add_obj(G_obj(random.randint(0,600),random.randint(0,600),random.randint(10,200),random.randint(10,200),random.randint(0,360),l.layar.zoom,"assets/images/pt-17.png"),render_type="chunk")
    L.add_obj(G_obj(random.randint(0,600),random.randint(0,600),random.randint(10,200),random.randint(10,200),random.randint(0,360),l.layar.zoom,"assets/images/error.png"),render_type="chunk")
    LM.get_rendering_surfs()
    LM.render_layars()
    end_time = time.time()
    print(f"total time : {abs(start_time - end_time)} and the fps is : {clock.get_fps()} at frame {i}")
    pygame.display.flip()
    clock.tick(100000)




