
made by : Matthew R and William L

////////////////////////////
-----welcome to skyport-----
////////////////////////////
v0.1.37(unstable)

    the purpos of skyport is to:
is to be a game engine that automaticly takes care of rendering loop , file pre loading and having a few usful utilaty tools

skyport-engine has some fetchers such as
    - automatically handling window management on a separate thread 
    - rendering objects with automatic image scaling and rotation
    - movable layer system with zoom and camera movement capabilities and will automatically scale surfs blit ed to the layers chunk surface 
    - file loader for pre loading or on fly loading of files 
    - a utility class with some random and potentially useful methods 
    - a animated texture system (although untested)
    - and a loger
    - and vector and hitbox system for objects (although untested and not used by the r_obj)

# boilerplate code :
```python
import skyport as sp

loader = sp.Loader() # the loader is used for pre loading assets
sp.init(loader,do_engine_loging=False) # some classes requier the loader to be used and this automaticly makes them use your loader

display_manager = sp.Display_manager(
    window_size=(800,600),
    display_size=(1000,1000),
    force_full_screen=False,
    window_name="skyport engine demo",
    window_ico=loader.image(path="window_ico.png",load_item_to_map=False),
    resizable=True
)

display_manager.START_RENDERING_THREAD(fps=60)
while(display_manager.running):
    """
    your code that runs every frame goes here
    """
    display_manager.event() # this is the event handler function



```


# engine data:

engine classes:
- Display_manager: main display manager class
- Delta_timer: delta time calculator
- Util: utility functions
- Layar_manager: manager for multiple layers (cameras)
- Camera: layer (camera) class (this can also be called Layer)
- r_obj: render-able object class (this also can be called Render)
- Render : this is a simpler and higher performance rendering obj but it dose not have sprite support and other fetchers  
- Loader: asset loader class
- loger: logging utility
- Sprite: animated texture class
- GSTI : placement map loader



class Util: this class is just for utilaty methods and theses are the methods it has
- disp_text(text, font, color, x, y,display): this method displays text (u need a pygame font),
- output_print_data(): this prints evrything in the print que,
- print(string): this puts a string in the print que,
- get_angle_and_dist(self,x1,y1,x,y): this rets the angle and dist (in that order) between 2 points,
- color_swap(self,surface: 'pygame.Surface', old_color: tuple, new_color: tuple) -> 'pygame.Surface': this method swaps evry
    instance of on ecolor on a pygame surf with another,
- pryoraty(self,a=None,b=None): this will always return a if there is an a i know aaaaaaaa thats scary,
- sort_objects_by_attr(self,obj_list : list, attr_name : str, reverse=False): this sorts a list of objs by an attar,
- snap_cords_in_bounds(x,y,max_x,max_y,min_x=0,min_y=0): this snaps a set of cords in a regon and returns the new cords

class Loader: this class is responsable for file management of all pygame supported images audio and json files
- load_texture_map(self,map_path): this you pass in a path to a texture map and it loades it,
- load_sound_map(self,map_path): this you pass in a path to a sound map and it loades it,
- load_file_map(self,map_path): this you pass in a path to a file map and it loades it,
    NOTE: the next 3 methods all return stuff loaded and precached by pygame and json loaders,
- image(path): this returns the image at the path,
- data(path): this returns the json at the path,
- create_alias(self,existing_path,new_path,map): this chainges the path from a path to any other string value 
- sound(path): this returns the sound at the path,
- warp_image(self,image,sizex,sizey,angle): this returns your image except warped to the specifications,
- rotate_image(self,image,angle): this rotates your image,
- scale_image(self,image,sizex,sizey): this scales your image ,
- play_sound(self,file_path, volume=0.5,loops=0): this actually plays a sound,
- join_maps(self,map_a,map_b): this puts all the elements of map b in map a and returns the modefied map a,
- rename_elament(self,path,new_name,mapp): this method renames an elements path so instead of typing a long path you can type somethong else,
- save_map(self,fp,name,mapp): this saves the current map as a map json that the loader can use later
- remove_file(self,path,map): this removes a file from a map and the loader instance will no longer be able to load it into the map,
- unban_path(self,path): this removes a path from the banned paths list so the loader can load it into map again ,
- play_sound_from_point(self,pf,sound_pos,listener_pos,volume=0.5,loops=0,distance_fade=0.5): this plays a sound from a point realative to anuther for suround sound

    WHAT IS A LOADER MAP:
        a loader map is a json format that the loader class can read for prechashing of files to memory and this is the format
        ```json
        {
            file_path:{"type":type,"value":value},
            ......
        }
        ```
        type:
            there are a cuple of type and depending on the type the value will need to chainge
            TYPES:
                "d" : this is the defalt type if the type is "d" then the value can be anything (bun mainly null) and the reson is bc the content of the path is put in the value spot and thus replaced (this happens in memory so the file is not chainged)
                "r" this stands for replace if there is this type then the value will need to hold a string for a replacement filepath so instead of loading the og filepath it will load a replacement path 
                "c" this stands for cantagory this is for if there are a lot of simularly named files in a dir and how it works is the value main path is a path up to a sertan dir then the value is a list of the rest of the dirs for example :
                    "assets/sounds":{"type":"c","value":[
                                            "bird_sounds/blue_bird.mp3",
                                            ......
                                            ]
                                }

                if the type is not anything the loader reconizes then it will sopose "d"


class Camera: (this class can also go by the name Layer) this class is responsible for the rendering of chunks and objects on it and camra movement
- chunkify(self,obj):this method puts an render obj in int proper chunk,
- get_chunk_cords(self,x,y): this method returns the cords of the chunk that a set of cords is in),
- get_chunk(self,cx, cy): this method returns the chunk at the cords and if there is none it creates one,
- get_obj_coliding_with_point(self,x,y): this method returns all rendering obj's in the layer that are colliding with that point,
- set_zoom(self, level): this sets the layers cameras zoom,
- get_surf(self) : this returns the layers surface,
- remove_chunk_obj(self,obj): this removes an obj from its chunk

class Layar_manager: this class is responsible for managing multiple layers (cameras)
- get_surf(self): self explanitory,
- sort(self): this sorts all the layers based off of there priority,
- add_layar(self,layer): this adds and a layer to the list of layers to render and then sorts the list,
- del_layar(self,pryoraty): this returns true if the layer at that priority was deleted
- remove_layar(self,pryoraty): this removes the layer from the list to be rendered but keeps the layer in a stash
- get_layar(self,pryoraty): this returns the layer at the priority,
- get_layar_objs(self,layar): this returns all the objs in that layer like this all__chunk_objs,all_offset_objs,
- set_layar_objs(self,chunk_objs,offset_objs,layer): this loads a layer with objs,
- add_obj(self,obj,layar_pryoraty): this automatically adds an rendering obj to a layer,
- remove_obj(self,obj,layar_pryoraty): this automatically removes an rendering obj from a layer


class Vector: this is a simple vector class for 2d vectors
- data : this vector dose not actualy update the position of its self until an update method is called. instead it perjects the destination point 
- this contains a dx,dy and its x,y but dose not actualy contain an angle or a speed 
- couculate_dx_dy(self,speed,angle): this couculates the angle and the speed and then returns it in the order that the function name sais
- couculate_angle_speed(self,dx,dy): this couculates the angle and speed of the vector baced off of the dx and dy
- update_pos(self,time_=1):  this updates the pos of the vector and sets the pos to the perjected pos 
- add_vector(self,vector:"Vector"): this adds another vector the the curent vector
- sub_vector(self,vector:"Vector"): this subtracts another vector from the curent vector
- print_data(self): prints the vectors data to the console
- get_pos_prejection(self,time_=1): gets the perjected pos of the vector
- get_pos(self): get the actual pos of the vector
- get_angle_speed(self): gets the angle and speed of the vector
- set_pos(self,x,y): sets the pos of the vector
- set_dx_dy(self,dx,dy): sets the dx and dy of the vector without updating the pos first
- set_dx_dy_updated(self,dx,dy,time_=1): this sets the dx and dy after updating the pos of the vector

class Interactor: this class is holds a hitbox rect and a vector for movement and colision detection and in the future other stuff as well but the interactor dose use an angle and speed unlike the Vector class
- variavles : Interactor.interactor_count = 0 , Interactor.intoractors = []   : these are clas wide varyables
- update(self): this updates the vectors pos to be at the vectors perjection and sycs the hitbox
- add_to_built_in_list(self): this adds the curent class intance to the interactors build in list
- get_pos(self): this gets the perjected pos of the interactor
- set_pos(self,x,y): this sets the pos of the interactor
- set_angle_speed(self,angle,speed): this sets the angle and speed of the interactor
- add_vector(self,vector:"Vector"): adds a vector to the interactor
- sub_vector(self,vector:"Vector"): subtracts a vector from the interactor
- check_colision(self,other:"Interactor"): this check if the curent interactor is coliding with another interactor
- check_colisions(self,others:"list[Interactor]"): this returns all the interactors that the curent interactor is coliding with
- check_colisions_with_vectors(self,others:"list[Vector]"): this returns all vectors that collide with the hitbox of the curent interactor
- 

class Delta_timer: this class gets the dt
    - def get_dt(): this returns the delta time

class Display_manager:
- get_gamestate(): this methods gives you the engine curent gamestate (LINK:gamestates),
- add_gamestate(name,lm): this method adds a gamestate (LINK:gamestates) to the engine (lm stands for layarmanager)
- remove_game_state(name): this deletes a gamestate (LINK:gamestates)
- get_mouse_pos() this gets the cursors position on the display 
- START_RENDERING_THREAD(fps): this starts the rendering thread and the engine gets to work
- STOP_RENDERING_THREAD() this stops the rendering thread 
- event() this method contains the event handler for the engine/window 
important attributes:
- .print_engine_data :this is a bool that if by default is True and if True then the engine will print data like the fps to consle,
- .print_rate :this is how many ticks the engine can attempt to print engine data 
    LINKS:
    gamestates: a gamestate is a layarmanager which holds all the layers and objs of that game state and only the 
        active gamestate is rendered 

class GSTI: this is for placement maps
- loade_placement() this places the placement map which you initialized when u created a GSTI instance
- save_placement_map(layar_pryoraty,save_fp): this takes all the objs in a layer and saves a placement map based off of this 

    example placement map
    'o' stands for override so it will use a declaration but u can override the declarations
        attars by having some of your own
    'm' stands for manual this placement has all the required attars
    'd' stands for default this takes a declaration but you must provide the pos
    ```json
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
    ```
dev_info:
    email:matthew.le.robins+proj@gmail.com
    (plz only email if u have found a bug and a good way to fix it and plz ensure i have a way to contact you about you suggested changes or requests)

