
from .imports import *

class Class_Data:
    """this class records how many instances of said class have been created"""
    instances = 0
    def __init__(self,tags=None):
        if getattr(self,"_class_data_initialized",False):
            return
        self._class_data_initialized = True
        type(self).instances += 1
        self.id = type(self).instances
        self.tags = {} if tags == None else tags

    def __del__(self):
        type(self).instances -= 1
        
    def _update_(self,event,*args,**kwargs):
        pass

class Logger(Class_Data):
    def __init__(self):
        super().__init__()
        self.sevarity_index = [print_YELLOW,prin_ORANGE,prin_RED,"\033[1;37;41m"]
        self._errors = []
        self._logs = []
        self.tags = {}
        self.total_sevarity = 0.0
        self.error_threashhold = 1.0

    def log(self,msg:"str"):
        self._logs.append(msg)
    def output_print_data(self,include_errors=True):
        """prints all the logs and errors"""
        print("----- logs -----")
        for msg in self._logs:
            print(msg)
        print("----- errors -----")
        for msg in self._errors:
            print(msg+"\n")
        print("---------------")
        self._errors.clear()
        self._logs.clear()
    def error(self,msg:"str",error=None,metadata:"str"="",sevarity:"float"=0,_already_handled_error=False):
        """loggs an error (sevarity is in persentages 1 = 100%, 0.5 = 50%,0.0 = 0% )"""
        if _already_handled_error:
            return
        if self.total_sevarity >= self.error_threashhold:
            pass
        if error == None:
            self._errors.append(f"{self.sevarity_index[sevarity]}!!- error -> {msg} , extra_data -> {metadata} -!!{prin_RESET}")   
        else:
            self._errors.append(f"{self.sevarity_index[sevarity]}!!- error -> {msg} , extra_data -> {metadata} , python error : {error}-!!{prin_RESET}")
        self.total_sevarity += sevarity
        if self.total_sevarity >= self.error_threashhold:
            self.output_print_data()
            exit(1)
            

    def get_last_error(self):
        return self._errors[-1]
    def get_last_log(self):
        return self._logs[-1]
    def has_logs(self):
        return (self._errors != [] and self._logs != [])
    def print(self):
        """prints all loggs and errors if there are any"""
        if self.has_logs():
            self.output_print_data()
                
logger = Logger()


class Interacotr():
    def _base_init(self):
        self.events = {
            pygame.KEYDOWN:{}, # key:[funcs(self,event)...] 
            pygame.KEYUP:{},
            "key_pressed":{}, # key:[funcs(self,event)...]
            pygame.MOUSEBUTTONDOWN:{}, # key:[funcs(self,event)...]
            pygame.MOUSEBUTTONUP:{},
            "mouse_pressed":{} # key:[funcs(self,event)...]
        }
        
    def __init__(self):
        self._base_init()

    def _handle_events(self,events): # i need to optomize this to loop over self.events instead of events
        """this handles the events and keybinds for this class"""
        for event in events:
            if event.type in self.events:
                sub_dict = self.events[event.type]
                lookup_key = getattr(event, 'key', getattr(event, 'button', None))
                if lookup_key in sub_dict:
                    for func in sub_dict[lookup_key]:
                        if hasattr(func,"__self__"):
                            func(event)
                        else:
                            func(self, event)

    def add_bind(self, event, button, func):
        if event not in self.events:
            logger.error(f"Render type class dose not yet support events of that type , error in {type(self)} with id of {self.id}")
            return
        sub_container = self.events[event]

        if isinstance(sub_container, list):
            if isinstance(func, (list, tuple)):
                sub_container.extend(func)
            else:
                sub_container.append(func)
            return
        if button not in sub_container:
            sub_container[button] = []
        if isinstance(func, (list, tuple)):
            sub_container[button].extend(func)
        else:
            sub_container[button].append(func)

    def _update_(self,events,*args,**kwargs):
            """this is called every frame and bust call self._handle_events(events) to work proporly"""
            self._handle_events(events)



def Load_file(func,mode="r"):
    """this wrapper you pass in a lambda function that takes a file obj and reads the data and returns it"""
    def wrapper(path):
        with open(path,mode) as f:
            data = func(f)
        return data
    return wrapper
def Save_file(func,mode="w"):
    """this wrapper you pass in a lambda that takes in a file obj and the data it wants to save"""
    def wrapper(path,data):
        with open(path,mode) as f:
            func(f,data)
    return wrapper

class Loader(Class_Data):
    error_asset_bace_dir=__file__
    error_asset_map = {}
    _suported_alpha_images = [".png", ".webp", ".svg"]
    _suported_opaque_images = [".jpg", ".jpeg", ".bmp", ".tga", ".gif", ".tiff", ".tif", ".qoi"]
    _suported_audio_formats = [".wav", ".ogg", ".mp3", ".flac", ".mid", ".midi"]
    def _init_supported_types(self):
        for t in Loader._suported_alpha_images:
            self.supported_types[t] = lambda p: pygame.image.load(p).convert_alpha()
        for t in Loader._suported_opaque_images:
            self.supported_types[t] = lambda p: pygame.image.load(p).convert()
        for t in Loader._suported_audio_formats:
            self.supported_types[t] = pygame.mixer.Sound

    def init(self,_is_internal_call=False):
        loader = Loader(Loader.error_asset_bace_dir,{"is_internal":_is_internal_call})
        Loader.error_asset_map["image"] = loader.read("assets/images/error.png")
        Loader.error_asset_map["sound"] = loader.read("assets/sounds/error.mp3")
        Loader.error_asset_map["data"] = loader.read("assets/data/error.json")

    def _setup(self):
        self._map = {}
        self._error_assets = {}
        self.supported_types = {
            ".txt": Load_file(lambda f: f.read()),
            ".json": Load_file(json.load),
            ".csv": Load_file(lambda f: list(csv.reader(f))),
            ".bin":  Load_file(lambda f: f.read(),"rb"),
            ".toml": Load_file(lambda f: _load_toml(f))
        } # unknow types will be read as a bynary 
        self.unsupported_handler = None
        self.supported_savers = {
            ".png": lambda p, d: pygame.image.save(d, p),
            ".jpg": lambda p, d: pygame.image.save(d, p),
            ".jpeg": lambda p, d: pygame.image.save(d, p),
            ".txt": Save_file(lambda f, d: f.write(str(d))),
            ".json": Save_file(lambda f, d: json.dump(d, f, indent=4)),
            ".csv": self._save_csv,
            ".bin": Save_file(lambda f, d: f.write(d)),
        }

    def __init__(self,dunder_file=None,tags=None):
        super().__init__(tags)
        if(dunder_file == None):
            call_frame = inspect.stack()[1]
            dunder_file = call_frame.filename
        self.base_dir = pl.Path(dunder_file).resolve().parent
        self._setup()
        self._init_supported_types()

        # this is to auto load the error assets
        if not Loader.error_asset_map and not self.tags.get("is_internal") == True:
            logger.log(f"created Loader instance with id of {self.id} and initialized error assets")
            self.init(True)

    def _save_csv(self, path, data):
        if not isinstance(data, list):
            logger.error(f"CSV saver expected a list of rows, got {type(data)}")
            return
        with open(path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(data)
    def _abs_resolve_path(self,path,bace_dir):
        path = pl.Path(path)
        if(path.is_absolute() ):
            return path.resolve()
        return (self.base_dir / path).resolve()
    def add_new_file_handler(self,type_extension:str,handler:"callable"):
        """examle : sp.Load_file(lambda file_obj: file_obj.read())"""
        self.supported_types[type_extension] = handler
    def add_new_save_file_handler(self,type_extension:str,handler:"callable"):
            """example : sp.Save_file(lambda f, d: json.dump(d, f, indent=4))"""
            self.supported_savers[type_extension] = handler
    def get_supported_types(self):
        return self.supported_types.keys()
    def set_unsupported_handler(self,handler=None):
        self.unsupported_handler = handler
    def resolve_path(self,path:"str"):
        path = pl.Path(path)
        if(path.is_absolute() ):
            return path.resolve()
        return (self.base_dir / path).resolve()
    def create_alias(self,path:"str",alias:"str"):
        data = self._map.get(path)
        if(data != None):
            self._map.pop(path)
            self._map[alias] = data
            return
        logger.error(f"could not create alias to {path} do to {path} not being found in Loader map")
    def get_map(self):
        return self._map
    def set_map(self,mapp:dict):
        self._map = mapp
    def _load_file(self,path,_already_handled_error=False):
        path = self.resolve_path(path)
        extension = os.path.splitext(path)[1].lower()
        if extension in self.supported_types:
            loader = self.supported_types[extension]
        else:
            loader = self.unsupported_handler
            if loader is None:
                logger.error(f"unsupported type {extension} while loading {path}, ( returning None )",_already_handled_error=_already_handled_error)
                return None
            logger.error(f"unsupported type {extension} for {path}, using fallback handler",_already_handled_error=_already_handled_error)
        try:
            return loader(path)
        except Exception as e:
            logger.error(f"error during loading of file {path}, ( returning None )", e, metadata="error from internal method",_already_handled_error=_already_handled_error)
            return None

    def read(self, path: "str", add_to_map:bool=False,overwrite_map:bool=False):
        if path in self._map and not overwrite_map:
            return self._map[path]
        result = self._load_file(path)
        if add_to_map and result is not None:
            self._map[path] = result
        elif result == None:
            logger.error(f"coild not open file {path} , returning None")
        return result
    def image(self,path:"str",add_to_map:bool=False,overwrite_map:bool=False):
        data = self.read(path,add_to_map,overwrite_map)
        if data == None:
            return Loader.error_asset_map.get("image")
        return data
    def data(self,path:"str",add_to_map:bool=False,overwrite_map:bool=False):
        data = self.read(path,add_to_map,overwrite_map)
        if data == None:
            return Loader.error_asset_map.get("data")
        return data
    def sound(self,path:"str",add_to_map:bool=False,overwrite_map:bool=False):
        data = self.read(path,add_to_map,overwrite_map)
        if data == None:
            return Loader.error_asset_map.get("sound")
        return data

    def _preload_folder_list(self,path:"str",preload_data:dict):
        path_list = preload_data["value"]
        value = []
        if(type(path_list) != list):
            return
        for p in path_list:
            combined_path = (pl.Path(path) / pl.Path(p))
            data = self._load_file(combined_path)
            value.append(data)
        self._map[path] = value
        return value
    def _preload_folder_dict(self,path:"str",preload_data:dict):
        path_list = preload_data["value"]
        value = {}
        if(type(path_list) != dict):
            return
        for name in path_list.keys():
            combined_path = pl.Path(path) / pl.Path(path_list[name])
            data = self._load_file(combined_path)
            value[name] = data
        self._map[path] = value
        return

    def _preload_elm(self,k,data):
        preload_data = data[k]
        preload_type = preload_data["type"]
        if(preload_type == "r" or preload_type == "replace"): # where value == replacement_path
            self.read(path=preload_data["value"],add_to_map=True,overwrite_map=True)
        elif(preload_type == "list"): # where u load an entire folder under 1 name 
            self._preload_folder_list(k,preload_data)
        elif(preload_type == "dict"):
             self._preload_folder_dict(k,preload_data)
        else: # defalt loading of path as the file
            self.read(path=k,add_to_map=True,overwrite_map=True)
    def load_from_dict(self,data:dict,completion_hook:callable=None,*completion_args,completion_kwargs,map_name:"str"=""):
        keys = data.keys()
        for k in keys:
            self._preload_elm(k,data) 
        logger.log(f"Loader {self.id} is complete loading map {map_name}")
        if completion_hook:
            completion_hook(completion_args,completion_kwargs)
    def load_from_map(self,map_path:"str",completion_hook:callable=None,*completion_args,**completion_kwargs):
        data = self.read(map_path,False)
        if(type(data) != dict):
            logger.error(f"Loader {self.id} canot load {map_path} as a Loader map (file is not .json)")
            return
        self.load_from_dict(data,completion_hook,completion_args,completion_kwargs,map_name=map_path)
    def load_from_str(self,data:str,completion_hook:callable=None,*completion_args,completion_kwargs,map_name:"str"=""):
        try:
            json_data = json.load(data)
            self.load_from_dict(json_data,completion_hook,completion_args,completion_kwargs,map_name=map_name)
        except json.JSONDecodeError as e:
            logger.error(f"could not load string map from map named {map_name}",e,sevarity=0.02)

    def load_map_on_thread(self, map_path: "str",completion_hook:callable=None,*completion_args,**completion_kwargs):
        thread = threading.Thread(target=self.load_from_map, args=(map_path,completion_hook,completion_args,completion_kwargs))
        thread.start()
        return thread
    def join_maps(self,map_a,map_b):
        """this method takes one map and adds all the content to the other"""
        for k in map_b.keys():
            item = map_b[k]
            map_a[k] = item
        return map_a
    def save(self,path:"str",data):
        data
        if( data == None ):
            logger.error(f"None is an invalid file content. can't save None to {path}")
            return
        full_path = self.resolve_path(path)
        extension = os.path.splitext(full_path)[1].lower()
        if extension not in self.supported_savers:
            logger.error(f"{extension} is an unsuported format for saving")
            return
        try:
            self.supported_savers[extension](full_path, data)
            logger.log(f"sucsesfully saved map_key data to {path}")
        except Exception as e:
            logger.error(f"error during save of file to path  : {path}",e)

    def save_map(self,path:"str",mapp:dict):
        try:
            with open(self._abs_resolve_path(path,self.base_dir),"w" ) as f:
                json.dump(mapp,f,indent=4)
        except Exception as e:
            logger.error(f"failed to save Loader map to path {path}",e)
    def clear_map(self):
        """this clears all pre loaded files out of memory"""
        self._map.clear()

class Delta_timer(Class_Data):
    def __init__(self):
        super().__init__()
        # Using perf_counter for highest precision
        self.prev_time = time.perf_counter()
        self.dt = 0.0

    def get_dt(self):
        now = time.perf_counter()
        self.dt = now - self.prev_time
        self.prev_time = now
        return self.dt

