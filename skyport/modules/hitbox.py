from ..global_utils import (
    math,
    pygame,
    Class_Data,
    logger
)

import shapely

class Hitbox(Class_Data):
    def _setup(self,angle=0,on_collide=None):
        super().__init__()
        self.angle = angle
        self._last_angle = None
        self._is_dirty = True
        self.origin = self.OG_shape.centroid
        self.on_collide = on_collide

        self.update()

    def __init__(self,x,y,width,height,angle:"int"=0,on_collide=None):
        self.OG_shape = shapely.geometry.box(x,y,x+width,y+height)
        self._setup(angle,on_collide)

    @classmethod
    def from_points(cls,points,angle:"int"=0,hole_points=None,on_collide=None):
        self = cls.__new__(cls)
        self.OG_shape = shapely.geometry.Polygon(points,hole_points)
        self._setup(angle,on_collide)
        return self

    def _rotate(self):
        if(self._last_angle != self.angle or self._is_dirty):
            self._last_angle = self.angle
            self._is_dirty = False
            self.shape = shapely.affinity.rotate(
                self.OG_shape,
                self.angle,self.origin
            )

    def update(self):
        """call this to update the hitbox (note when calling .collide it auto updates)"""
        self._rotate()

    def collide(self,other_hitbox:"Hitbox") -> bool:
        self.update()
        if isinstance(other_hitbox,Hitbox):
            other_hitbox.update()
            _other_hitbox = other_hitbox.shape
        else:
            _other_hitbox = other_hitbox
        try:
            if (self.shape.intersects(_other_hitbox)):
                if self.on_collide != None:
                    self.on_collide()
                return True
            return False
        except Exception as e:
            logger.error(f"could not couculate a collision between {type(self)} with id of {self.id} and {type(other_hitbox)} . e -> {e}")
            return False

    def get_pos(self):
        return (self.origin.x,self.origin.y)
    def get_bounds(self):
        return self.shape.bounds
    def get_width_height(self):
        minx, miny, maxx, maxy = self.shape.bounds
        return (maxx - minx, maxy - miny)
    def set_pos(self,x,y):
        ox,oy = self.origin.x,self.origin.y
        dx,dy = x - ox , y - oy
        self.OG_shape = shapely.affinity.translate(self.OG_shape,dx,dy)
        self.origin = self.OG_shape.centroid
        self._is_dirty = True
    def translate(self,dx,dy):
        self.OG_shape = shapely.affinity.translate(self.OG_shape,dx,dy)
        self.origin = self.OG_shape.centroid
        self._is_dirty = True

    def set_angle(self,angle):
        self.angle = angle % 360

    def mark_dirty(self):
        self._is_dirty = True


class Hitbox_Manager(Class_Data):
    def _setup(self):
        super().__init__()

    def __init__(self):
        self._setup()
        self.hitboxes = []

    def get_colliding(self):
        colliding = {}
        for h1 in self.hitboxes:
            colliding[h1.id] = []
            for h2 in self.hitboxes:
                if h1.collide(h2):
                    colliding[h1.id].append(h2.id)
        return colliding

    def remove_hitbox(self,id):
        for hitbox in self.hitboxes:
            if id == hitbox.id:
                self.hitboxes.remove(hitbox)

    def translate_all(self,dx,dy):
        for hitbox in self.hitboxes:
            hitbox.translate(dx,dy)
    def rotate_all(self,angle):
        for hitbox in self.hitboxes:
            hitbox.set_angle(angle)




    