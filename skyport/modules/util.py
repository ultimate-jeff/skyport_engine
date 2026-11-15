
from ..imports import *
from ..global_utils import (
    Class_Data,
    logger
)



def snap_in_bounds(value:"int",max_value:"int",min_value:"int"):
    return max(min(value,max_value),min_value)

def dot_product(vec1:"tuple[int,float]",vec2:"tuple[int,float]"):
    """returns the dod product of 2 2d vectors (x,y)"""
    return vec1[0]*vec2[0] + vec1[1]*vec2[1]

def snap_cords_in_bounds(x:"int",y:"int",max_x:"int",max_y:"int",min_x:"int"=0,min_y:"int"=0):
    """this snaps a point inside of a rect arya """
    new_x = min(max(x,min_x),max_x-1)
    new_y = min(max(y,min_y),max_y-1)
    return new_x,new_y

def play_sound(soud_obj:"pygame.mixer.Sound", volume=0.5,loops=0):
    try:
        soud_obj.set_volume(volume)
        soud_obj.play(loops)
        return 1
    except Exception as e:
        logger.error("error trying to play sound",e)

def play_sound_from_point(pf,sound_pos:"tuple",listener_pos:"tuple",volume:"float"=0.5,loops:"int"=0,distance_fade:"float"=0.5):
    """this playes a sound from a point"""
    max_vol = volume
    dist = math.hypot(sound_pos[0] - listener_pos[0], sound_pos[1] - listener_pos[1])
    volume *= max(0, 1 - dist / distance_fade)
    play_sound(pf, volume, loops)


def warp_image(image:"pygame.Surface",sizex:"int",sizey:"int",angle:"float"):
    image1 = pygame.transform.scale(image,(sizex,sizey))
    image2 = pygame.transform.rotate(image1,angle)
    return image2
def rotate_image(self,image:"pygame.Surface",angle:"float"):
    image2 = pygame.transform.rotate(image,angle)
    return image2
def scale_image(image:"pygame.Surface",sizex:"int",sizey:"int"):
    image1 = pygame.transform.scale(image,(sizex,sizey))
    return image1

def color_swap(surface: 'pygame.Surface', old_color: tuple, new_color: tuple) -> 'pygame.Surface':
    """returns a surf that every instance of one color is replaced with a nuther"""
    arr_rgb = pygame.surfarray.array3d(surface)
    arr_alpha = pygame.surfarray.array_alpha(surface)
    mask = np.all(arr_rgb == old_color, axis=-1)
    arr_rgb[mask] = new_color
    new_surface = pygame.Surface(surface.get_size(), pygame.SRCALPHA, 32)
    new_surface = new_surface.convert_alpha()
    pygame.surfarray.blit_array(new_surface, arr_rgb)
    pygame.surfarray.pixels_alpha(new_surface)[:] = arr_alpha
    return new_surface

def couculate_dx_dy(self,dist:"int",angle:"float"):
    rad = math.radians(angle)
    dx = dist * math.cos(rad)
    dy = dist * math.sin(rad)
    return dx,dy
def couculate_angle_dist(dx:"int",dy:"int"):
    speed = math.sqrt(dx**2 + dy**2)
    angle = math.atan2(dy,dx)
    return angle,speed


class Vector(Class_Data):

    def __init__(self,x,y,dx=0,dy=0, tags=None):
        self.x,self.y = x,y
        self.dx,self.dy = dx,dy
        super().__init__(tags)

    def update_angle_lenth(self):
        """updates the angle,lenth from the dx,dy"""
        self.angle,self.lenth = couculate_angle_dist(self.dx,self.dy)
    def update_dx_dy(self):
        """updates the dx,dy from the angle,lenth"""
        self.dx,self.dy = couculate_dx_dy(self.angle,self.lenth)

    def set_angle(self,angle):
        "set angle and auto updates"
        self.angle = angle
        self.update_dx_dy()
    def set_lenth(self,lenth):
        "set lenth and auto updates"
        self.lenth = lenth
        self.update_dx_dy()
    def set_angle_lenth(self,angle,lenth):
        """sets angle,lenth and updates"""
        self.angle,self.lenth = angle,lenth
        self.update_dx_dy()
    def set_dx_dy(self,dx,dy):
        "sets dx,dy and auto updates"
        self.dx,self.dy = dx,dy
        self.update_angle_dist()

    def update(self):
        self.update_angle_dist()

    def update_pos(self):
        self.x += self.dx
        self.y += self.dy

    