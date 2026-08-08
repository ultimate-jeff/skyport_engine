from ..global_utils import (
    math,
    pygame,
    Class_Data
)

import pymunk as pm

class Hitbox(Class_Data):
    def __init__(self):
        super().__init__()
        self.hitbox = pm

class Hitbox_handler(Class_Data):
    def __int__(self):
        super().__init__()
        self.space = pm.Space()

    def update(self):
        pass




    