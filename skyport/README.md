
made by : Matthew R and William L

////////////////////////////
-----welcome to skyport-----
////////////////////////////
v0.1.32(unstable)

    the purpos of skyport is to:
provide a simpler way to make a 2d game with pygame without having to learn how to use pygame itself.

engine classes:
- Display_manager: main display manager class
- Delta_timer: delta time couculator
- Util: utility functions
- Layar_manager: manager for multiple layers (cameras)
- Camera: layer (camera) class (this can also be caled Layar)
- r_obj: renderable object class (this also can be caled Render)
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
    instance of on ecolor on a pygame surf with a nuther,
- pryoraty(self,a=None,b=None): this will alwas return a if there is an a i know aaaaaaaa thats scary,
- sort_objects_by_attr(self,obj_list : list, attr_name : str, reverse=False): this sorts a list of objs by an attar,
- snap_cords_in_bounds(x,y,max_x,max_y,min_x=0,min_y=0): this snaps a set of cords in a regon and returns the new cords

class Loader: this class is responsable for file management of all pygame suported images adio and json files
- load_texture_map(self,map_path): this you pass in a path to a texture map and it loades it,
- load_sound_map(self,map_path): this you pass in a path to a sound map and it loades it,
- load_file_map(self,map_path): this you pass in a path to a file map and it loades it,
    NOTE: the next 3 methods all return stuff loaded and prechashed by pygame and json loaders,
- image(path): this returns the image at the path,
- data(path): this returns the json at the path,
- sound(path): this returns the sound at the path,
- warp_image(self,image,sizex,sizey,angle): this returns your image exept warped to the specifacations,
- rotate_image(self,image,angle): this rotates your image,
- scale_image(self,image,sizex,sizey): this scales your image ,
- play_sound(self,file_path, volume=0.5,loops=0): this actualy plays a sound,
- join_maps(self,map_a,map_b): this puts all the elaments of map b in map a and returns the modefied map a,
- rename_elament(self,path,new_name,mapp): this method renames an elamets path so instead of typing a long path you can type somethong else,
- save_map(self,fp,name,mapp): this saves the curent map as a map json that the loader can use later
- remove_file(self,path,map): this removes a file from a map and the loader instance will no longer be able to load it into the map,
- unban_path(self,path): this removes a path frome the banned paths list so the loader can load it into map again ,
- play_sound_from_point(self,pf,sound_pos,listener_pos,volume=0.5,loops=0,distance_fade=0.5): this playes a sound from a point realative to anuther for suround sound

    WHAT IS A LOADER MAP:
        a loader map is a json format that the loader class can read for prechashing of files to memory and this is the format
        
        {
            file_path:{"type":type,"value":value},
            ......
        }

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


class Camera: (this class can also go by the name Layar) this class is responsable for the rendering of chunks and objects on it and camra movement
- chunkify(self,obj):this method puts an render obj in int propor chunk,
- get_chunk_cords(self,x,y): this method returns the cords of the chunk that a set of cords is in),
- get_chunk(self,cx, cy): this method returns the chunk at the cords and if there is none it creates one,
- get_obj_coliding_with_point(self,x,y): this method returns all rendering obj's in the layar that are colliding with that point,
- set_zoom(self, level): this sets the layars camras zoom,
- get_surf(self) : this returns the layars surface,
- remove_chunk_obj(self,obj): this removes an obj from its chunk

class Layar_manager: this class is responsable for managing multiple layars (cameras)
- get_surf(self): self explanitory,
- sort(self): this sorts all the layars baced off of there pryoraty,
- add_layar(self,layar): this adds and a layar to the list of layars to render and then sorts the list,
- del_layar(self,pryoraty): this returns true if the layar at that pryoraty was deleted
- remove_layar(self,pryoraty): this removes the layar from the list to be renderd but ceeps the layar in a stash
- get_layar(self,pryoraty): this returns the layar at the pryoraty,
- get_layar_objs(self,layar): this returns all the objs in that layar like this all__chunk_objs,all_offset_objs,
- set_layar_objs(self,chunk_objs,offset_objs,layar): this loads a layar with objs,
- add_obj(self,obj,layar_pryoraty): this automaticly adds an rendering obj to a layar,
- remove_obj(self,obj,layar_pryoraty): this automaticly removes an rendering obj from a layar


class Delta_timer: this class gets the dt
    - def get_dt(): this returns the delta time

class Display_manager:
- get_gamestate(): this methods gives you the engine curent gamestate (LINK:gamestates),
- add_gamestate(name,lm): this method adds a gamestate (LINK:gamestates) to the engine (lm stands for layarmanager)
- remove_game_state(name): this delets a gamestate (LINK:gamestates)
- get_mouse_pos() this gets the cursurs position on the display 
- START_RENDERING_THREAD(fps): this starts the rendering thread and the engine gets to work
- STOP_RENDERING_THREAD() this stops the rendering thread 
- event() this method contains the event handler for the engine/window 
important atrabutes:
- .print_engine_data :this is a bool that if by defalt is True and if True then the engine will print data like the fps to consle,
- .print_rate :this is how many ticks the engine can attempt to print engine data 
    LINKS:
    gamestates: a gamestate is a layarmanager which holds all the layars and objs of that gamestate and only the 
        active gamestate is renderd 

class GSTI: this is for placement maps
- loade_placement() this places the placement map which you initalized when u created a GSTI instance
- save_placement_map(layar_pryoraty,save_fp): this takes all the objs in a layar and saves a placement map baced off of this 

    example placement map
    'o' stands for override so it will use a declaration but u can override the declarations
        attars by having some of your own
    'm' stands for manual this placement has all the requierd attars
    'd' stands for defalt this takes a declaration but you must provide the pos
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
