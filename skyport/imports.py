
import inspect
import os
import sys
import pathlib as pl
import json
import csv
import tomllib
import threading
import math
import numpy as np
import time
import random
import pygame
import shapely

sys.setrecursionlimit(1500) 

pygame.init()

base_dir = pl.Path(__file__).resolve().parent

prin_RED = '\033[91m'
prin_GREEN = '\033[92m'
prin_BLUE = '\033[94m'
prin_RESET = '\033[0m'
print_YELLOW = '\033[33m'
print_MAGENTA = '\033[35m'
print_CYAN = '\033[36m'
prin_ORANGE = '\033[38;5;208m'
prin_PINK = '\033[38;5;206m'
prin_PURPLE = '\033[38;5;129m'
prin_BROWN = '\033[38;5;94m'
prin_GOLD = '\033[38;5;220m'
prin_LIME = '\033[38;5;118m'
prin_TEAL = '\033[38;5;30m'
prin_NAVY = '\033[38;5;18m'
prin_SKY_BLUE = '\033[38;5;117m'
prin_HOT_PINK = '\033[38;5;198m'
prin_MAROON = '\033[38;5;88m'
prin_OLIVE = '\033[38;5;100m'
prin_VIOLET = '\033[38;5;93m'
prin_SALMON = '\033[38;5;209m'
prin_DARK_GREEN = '\033[38;5;22m'

def get_text_color(color:"tuple"):
    return f"\033[{color[0]};{color[1]};{color[2]}m"
def get_colord_text(color:"tuple",text):
    return f"{get_text_color(color)}{text}{prin_RESET}"