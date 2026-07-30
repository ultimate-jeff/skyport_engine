from .global_utils import (
    pygame,
    math,
)
class Sound():
    def __init__(self,sound:"pygame.Sound",x,y,max_dist=math.inf,base_vol=1,fade=1.0):
        self.sound = sound
        self.x,self.y = x,y
        self.max_dist = max_dist
        self.base_vol = base_vol
        self.sound_threashold = 0.01
        self.loops = 0
        self.max_time = 0
        self.fade = fade

class Sound_Engine():
    def _get_angle_and_dist(self,x1:"int",y1:"int",x:"int",y:"int"):
        """returns the angle and dist between 2 points (it returns that data in that ordor )"""
        dx = x1 - x
        dy = y1 - y
        dist = math.hypot(dx, dy)
        angle = (math.degrees(math.atan2(dy, dx)) + 180) % 360
        return angle,dist

    def __init__(self,x:"int",y:"int",max_dist=math.inf,fade=1):
        self.x,self.y = x,y
        self.max_dist = max_dist
        self.min_dist = 0
        self.spatial_sounds = []
        self.global_sounds = []
        self.obstruction_renders = []
        self.sound_threashold = 0.01
        self.fade = fade

    def _play_sound(self,sound,angle):
        angle = math.radians(angle)
        lv = max(0,0.5 * (1 - math.sin(angle)))
        rv = max(0,0.5 * (1 + math.sin(angle)))

        channel = pygame.mixer.find_channel()
        if channel != None:
            channel.play(sound.sound,sound.loops,sound.max_time)
            channel.set_volume(lv,rv)
        else:
            print("sound chanle full")

    def _get_fade_vol(self, max_dist, dist, vol, fade=1):
        t = min(max(dist / max_dist, 0), 1)
        return vol * (1 - t) ** fade

    def play_audio(self):
        for sound in self.spatial_sounds:
            angle,dist = self._get_angle_and_dist(self.x,self.y,sound.x,sound.y)
            max_dist = self.max_dist if sound.max_dist != None else sound.max_dist
            if dist > max_dist:
                continue
            vol = sound.base_vol
            print(f"vol -> {vol}")
            vol = self._get_fade_vol(max_dist,dist,vol,self.fade)
            print(f"post faded vol -> {vol}")
            for obj in self.obstruction_renders:
                if obj.rect.clipline((self.x,self.y),(sound.x,sound.y)):
                    multiplier = 1 - min(abs(obj.tags.get("sound_dampening", 0)) / 100, 1)
                    vol *= multiplier
                    vol *= multiplier

            if vol >= self.sound_threashold:
                self._play_sound(sound,angle)
                self.spatial_sounds.remove(sound)
              
              