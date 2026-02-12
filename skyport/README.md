
made by : Matthew R and William L

////////////////////////////
-----welcome to skyport-----
////////////////////////////

    the purpos of skyport is to:
provide a simpler way to make a 2d game with pygame without having to learn how to use pygame itself.

engine classes:
- Display_manager: main display manager class
- Delta_timer: delta time couculator
- Util: utility functions
- Layar_manager: manager for multiple layers (cameras)
- Camera: layer (camera) class
- r_obj: renderable object class
- Loader: asset loader class
- loger: logging utility
- Sprite: animated texture class
- GSTI : placement map loader



class Util: this class is just for utilaty methods and theses are the methods it has
    disp_text(text, font, color, x, y,display): this method displays text (u need a pygame font),
    output_print_data(): this prints evrything in the print que,
    print(string): this puts a string in the print que,
    get_angle_and_dist(self,x1,y1,x,y): this rets the angle and dist (in that order) between 2 points,
    color_swap(self,surface: 'pygame.Surface', old_color: tuple, new_color: tuple) -> 'pygame.Surface': this method swaps evry
        instance of on ecolor on a pygame surf with a nuther,
    pryoraty(self,a=None,b=None): this will alwas return a if there is an a i know aaaaaaaa thats scary,
    sort_objects_by_attr(self,obj_list : list, attr_name : str, reverse=False): this sorts a list of objs by an attar,

class Loader: this class is responsable for file management of all pygame suported images adio and json files
    load_texture_map(self,map_path): this you pass in a path to a texture map and it loades it,
    load_sound_map(self,map_path): this you pass in a path to a sound map and it loades it,
    load_file_map(self,map_path): this you pass in a path to a file map and it loades it,
    NOTE: the next 3 methods all return stuff loaded and prechashed by pygame and json loaders,
    image(path): this returns the image at the path,
    data(path): this returns the json at the path,
    sound(path): this returns the sound at the path,
    warp_image(self,image,sizex,sizey,angle): this returns your image exept warped to the specifacations,
    rotate_image(self,image,angle): this rotates your image,
    scale_image(self,image,sizex,sizey): this scales your image ,
    play_sound(self,file_path, volume=0.5,loops=0): this actualy plays a sound

class Delta_timer: this class gets the dt
    def get_dt(): this returns the delta time

class Display_manager:
    get_gamestate(): this methods gives you the engine curent gamestate (LINK:gamestates),
    add_gamestate(name,lm): this method adds a gamestate (LINK:gamestates) to the engine (lm stands for layarmanager)
    remove_game_state(name): this delets a gamestate (LINK:gamestates)
    get_mouse_pos() this gets the cursurs position on the display 
    START_RENDERING_THREAD(fps): this starts the rendering thread and the engine gets to work
    STOP_RENDERING_THREAD() this stops the rendering thread 
    event() this method contains the event handler for the engine/window 

    LINKS:
    gamestates: a gamestate is a layarmanager which holds all the layars and objs of that gamestate and only the 
        active gamestate is renderd 

class GSTI: this is for placement maps
    loade_placement() this places the placement map which you initalized when u created a GSTI instance
    save_placement_map(layar_pryoraty,save_fp): this takes all the objs in a layar and saves a placement map baced off of this 

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
