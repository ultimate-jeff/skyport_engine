from ..imports import *
from ..global_utils import (
    Class_Data,
    logger,
    Loader
)
from ..main import (
    Layer,
    Render,
    Display_Manager
)


class Scene(Render):
    def __init__(self, x, y, width, height, angle, layer:"Layer"=None,pre_load_asset_map:"dict"=None, tags = None):
        self.layer = layer
        self.pre_load_asset_map = pre_load_asset_map
        super().__init__(x, y, width, height, angle, None, tags)

    def load_assets(self,loader:Loader):
        loader.clear_map()
        t = type(self.pre_load_asset_map)
        if t == dict:
            loader.load_from_dict(self.pre_load_asset_map)
        elif t == str:
            loader.load_from_str(self.pre_load_asset_map)
        else:
            logger.error("could not load Loader file map",sevarity=0.2)

    def _update_(self, event, *args, **kwargs):
        self.layer._update_obj(self.layer,events=event,args=args,kwargs=kwargs)
        img_rect = self.layer.image.get_rect(center=self.layer.rect.center)
        self.surf.blit(self.layer.image,img_rect)
        self._is_dirty = True
        return super()._update_(event, *args, **kwargs)
        


class Scene_Manager(Class_Data):
    def __init__(self,loader:Loader,scenes:"dict[Scene]", tags=None):
        super().__init__(tags)
        self.loader = loader
        self.scenes = scenes

    def add_scene(self,scene:"Scene",name:"str"):
        self.scenes[name] = scene
    def set_scene(self,name:"str",layer:"Layer"):
        scene = self.scenes.get(name)
        if not scene:
            logger.error(f"coult not find scene named {name}",IndexError,sevarity=0.25)
            return
        layer.clear()


        

