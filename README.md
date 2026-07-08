made by: Matthew R and William L
```
///////////////////////////////////
-----welcome to skyport_engine-----
///////////////////////////////////
```
( semmi stable )
 
skyport is a 2D game engine built on pygame-ce that simplifies tasks like managing the window , asset loading , rendering and eventually more.
# Data :
## links :
- GitHub : https://github.com/ultimate-jeff/skyport_engine 
- pypi : https://pypi.org/project/skyport-engine/ 

## Table of Contents
- Data : (like links or other data)
- getting started : (like a tutorial on how to use skyport)
- Content : (like all classes in skyport_engine)
- dev_info : (like email ...)

## what platforms does skyport_engine work on :
- windows (this is the platform it is developed on)
- linux (slight testing has been done on linux)
- mac (has not been tested yet but might work)

# features :
- Multithreaded rendering
- Automatic window management
- Asset preloading and caching
- Built-in input handling
- Delta timer
- Render helper class
- Experimental chunk renderer
- SDL2 renderer (experimental)

# Getting started:
Note: 
    skyport is not a replacement for pygame, so it is good to be familiar with pygame.
    
to start you will first need skyport_engine 
```terminal
pip install skyport-engine
```
## Boilerplate code:
```python
import skyport as sp
 
dm = sp.Display_Manager(
    window_size=(1920,1080),
    display_size=(960,540),
    window_name="skyport test"
    )
 
dm.START_RENDERING_THREAD(fps=60)
while dm.running:
 
    dm.event_handler()
```

## Creating the window:
To start off you might want to have pygame and skyport, but don't import pygame directly — otherwise you will be using a separate instance of pygame from the rest of skyport. Instead, get pygame from skyport:
```python
import skyport as sp
 
pygame = sp.pygame
```
Now you can use pygame and skyport normally.
 
To create your window you will need to create a Display_Manager instance:
```python
 
    display_manager = sp.Display_Manager(
        window_size=(500, 500),
        display_size=(100, 100), # the display size is the scale at which the game is run
        window_name="my window"
        window_ico=None # this would be a pygame.Surface or an image, but we will go over this later
        force_full_screen=False # this determines if the window will start full screened
        resizable=True # if this is False then the window will not be resizable
    )
```
This will make a window pop up, but it won't respond, because the rendering thread is not on and you have to manually manage the window in this state.
 
One thing you can do while the window is in this state is manually run a loading screen while your game initializes before the rendering thread starts:
```python
import time
pygame = sp.pygame
 
# you will see how to use the loader further down in the README.md
loader = sp.Loader(__file__)
img = loader.read(path="C:\\Users\\matt\\source\\repos\\RSPG\\RSPG\\pt-17.png",add_to_map=True)
 
 
dm = sp.Display_Manager(
    window_size=(500,500),
    display_size=(100,100),
    window_name="my first skyport window",
    window_ico=img
)
 
time.sleep(10) # your game loading
 
# until you start the rendering thread the window will not respond
dm.START_RENDERING_THREAD(60)
 
sp.loger.output_print_data() # this line prints out everything that the engine has logged, including any errors or random logs
 
 
#game loop
while dm.running:
 
    dm.event_handler()
    dm.tick(tps=20) # <- this just ensures that the game loop runs at 20 ticks per second 
```
In this example the window will not respond for 10 seconds, but in that time you could initialize your game on a separate thread and run a loading screen (video on threading: https://www.youtube.com/watch?v=A_Z1lgZLSNc).
 
## Game loop:
After you have the window created:
```python
import skyport.__init__ as sp
import time
pygame = sp.pygame
 
dm = sp.Display_Manager(
    window_size=(500,500),
    display_size=(100,100),
    window_name="my first skyport window",
    ....
)
```
You can create the game loop, and with skyport it's simple:
```python
#previous code like creating the display .....
 
display_manager.START_RENDERING_THREAD(fps=60) # <- this starts the rendering thread
 
while display_manager.running:
 
    display_manager.event_handler() # <- this handles window events and keybinds; if it is not in the game loop the window will not respond
 
    # this line (\/) is not needed, but it ensures that the game loop has consistent timing (in this case at 20 ticks per second)
    display_manager.tick(tps=20)
```

## keybinds and event handler :
there are 3 types of binds : key up , key down , key pressed 
these you can bind any function to any of the 3 types and you can have multiple functions on 1 key 
### adding and removing binds :
to add or to remove a bind you can call its add or remove method for the type 
```python
display_manager.add_keyup_bind(pygame.K_a,my_function)

display_manager.add_keydown_bind(pygame.K_s,lambda : print("this bind works"))

dislay_manager.add_keypressed_bind(pygame.K_e,[func1,func2,func3]) # <- you can add multiple functions to 1 key and it works for all bind types not just pressed keys
```
you can also remove binds 
```python
display_manager.remove_keyup_bind(pygame.K_a,my_function) # this will remove the function from the key bind of 'a' 
display_manager.remove_keydown_bind(pygame.K_s,function)

display_manager.remove_keypressed_bind(pygame.K_e,[func1,func2,func3]) #<- you can also remove multiple binds and this works on the other types as well
```
you might want to use mouse position on some of your games and to do that you would use display_manager.get_mouse_pos() and this would return a tuple of x and y of the mouse pos (not of actual pos but pos relative to the display not window)
```python
mouse_pos = display_manager.get_mouse_pos() # this returns (x,y)
```
### how binds get triggered :
for your keybinds to work in the game loop the event handler must be called
```python
import skyport
pygame = skyport.pygame

# ... other code ...

clock = pygame.time.Clock() # you dont have to use the Display_Manager's built in clock for your game loop

while display_manager.running:

    display_manager.event_handler() # this will take care of keybinds and other events

    clock.tick(20) # <-tps
```
### joysticks and gamepad and other input methods :
support for more input methods will come if future updates

## bliting and filling of the window :
note :
```text
there are 2 surfaces in the display manager 1: the window and 2: the display 
the display is the one that you will blit to (the display is scaled to the size of the window then the display is blitted to the window)
```
there are 3 main methods :
 - blit(self,source: "pygame.Surface", dest: "pygame.RectLike" = (0, 0), area: "pygame.RectLike" = None, special_flags: "int" = 0):
 - fill(self,color:"tuple"=(0,0,0,0),rect:"pygame.Rect"=None,special_flags:"int"=0):
 - get_display() -> display_manager_instance display
these three methods are currently all you have to work with but because you can get the display all pygame ops work 
```python
# .....
display = display_manager.get_display()

display.fill((100,0,0))

display_manager.blit(surf,(10,10)) # works just like the pygame blit (bc it is)

# .....
```
do take into acount that when you blit something to the display it will not go on to the window unless the rendering thread is started or you would have to call display_manager.update_window()
```python
# ... previos code /\
display_manager.blit(surf,(10,10)) # blit a surf to pos x=10,y=10

display_manager.update_window() # update window so what was just blitted to the display is now on the window

display_manager.START_RENDERING_THREAD(fps=60) # the rendering gthread automatically handles updating the display so after you start the rendering thread you should not call update_window()
#... game loop \/
```
## how to use the Loader :
note :
```text
the loader is made to pre load files so your game is not waiting on ssd to load your files
```
creating a Loader instance is vary easy 
```python

loader = skyport.Loader(__file__) # you need to pass this in or the loader might not use the correct base directory for relative paths 

```
to actually pre load your loader instance with files you will need to call loader.load_from_map
```python
loader = skyport.Loader(__file__)

loader.load_from_map(map_path="path/to/Loader_preload_map.json") 
``` 
when you call load_from_map the loader instance will look at that file dir and try to preload all the files that the loader map said to pre load 

note :
```text
to see how to make a Loader map go to the Loader section in the read me and in a later update there will be a tool to automatically create Loader maps for you 
```

### how to read files with the Loader :
the method for reading a file with the loader is loader.read
```python

image = loader.read(path="my_images/file.png") # this will return the files content and in this case its a image

data = loader.read(path="my_files/data.json",add_to_map=True) # in this case i want to load the json more than once so i will att it to the map which means next time you try to load it it will pull it from memory instead of disk 

```
there is also some other ways to read a file but these ways have an error asset tied to them so if your image fails to load you get an error image
```python 
skyport.Loader.init() # this will init the Loader class with the error assets

loader = skyport.Loader(__file__) # create a Loader instance to load files

img = loader.image(path="my_images/jeff.png") # if the loader cant load this file then it will return an error image 
sound = loader.sound(path="my_sounds/idk.mp3") # there is also an error sound

data = loader.data(path="my_data/dave.json") # there is only a error json (try to not use this one but it exsists)
```
the Loaders .image , .sound , .data methods all have the same parameters as loader.read but they will try to give you an error asset instead of None 
### saving files with the Loader :
you can save files with loader.save(path,map_key)
```python
img = pygame.Surface((100,100))
img.fill((100,100,100))

loader.save(img,"my_images/new_img.jpeg")

```

## more will come ...
as of the current version the documentation on how to get started with skyport is not complete and will be in later updates

# Content :

## Display_Manager:
The Display_Manager is made to automatically handle the window on a separate thread so that the rendering loop can be separate from the game loop.
Note :
```
the display manager has been mostly coverd in the getting started section but heare we will dive a bit deeper into what the Display_Manager actually can do
```

 
## Loader:
The Loader is made to pre-cache files in memory.
 
### How to make a Loader map:
```json
{
    "path":{"value":null,"type":null},
    ...
}
```
In the Loader_map format there are a couple of types, and each does different things.
 
TYPES:
- "r" / "replace": this type will read the file from where "value" says to, rather than the original path. Example: ```json "path/jeff.png":{"value":"replacement_path.jpg","type":"r"} ```
- "list": this mode allows you to load an entire file under one name by having "path" as the folder dir and then in "value" you would place a list of files you would like to load. Example: ```json "path/dave":{"value":["bob.png","sam/frend.json"...],"type":"list"} ``` How you would access this is: loader_instance.read(path)[index]
- "dict": this type allows you to load an entire folder under one name, slightly differently. The "path" would be the folder dir just like in "list", but this time "value" is filled with a dict of {"name":"file"} instead of a list. Example: ```json "assets/rand":{"value":{"dave":"dave.png","bob":"idk/jeff.csv"},"type":"dict"} ``` How you would access it is by: loader_instance.read(path)[name]
- null: this is the default, and it doesn't matter what the "type" is. This mode will load the "path" into the Loader map, and how you would access the file would be: loader_instance.read(path)
FULL FILE EXAMPLE:
```json
{
    "assets/jeff.png":{
        "value":null,
        "type":null
    },
    "assets/rand/":{
        "value":[
            "ball.json",
            "ball.png"
        ],
    "type":"list"
    },
    "assets/icons": {
        "type": "dict",
        "value": {
            "button1": "button_play.png",
            "coin": "coin.png",
            "button2": "button2.png"
        }
    },
    "assets/files/data.png":{
        "value":"texture_pack/file/data.png",
        "type":"replace"
    }
}
```
### How to use Loader in code:
The Loader is simple: you first create an instance and pass in `__file__` so that the Loader can resolve relative paths, then you can preload the Loader with a Loader map (this is optional), then you can use the Loader to read files whether they have been pre-cached or not. Example code:
```python
import skyport as sp
 
# you need to pass in __file__ so the Loader knows how to resolve relative paths
loader = sp.Loader(__file__)
# (optional) you can preload all the files you want into the Loader so you don't have to get them later
loader.load_from_map("loader_map_test1.json")
 
# to read the content of the file whether the Loader has pre-loaded it or not, you can call read()
file_data = loader.read(path="my_path/image.png",add_to_map=True)
# this method allows you to create more convenient names for your pre-loaded files
loader.create_alias("my_path/image.png","image")
# this returns the dict of supported types and their file handlers
loader.get_supported_types()
# you can add your own file types for the loader to support if the loader doesn't already support them
loader.add_new_file_handler(".idk",lambda path : open(path,"r"))
# this is for when you have two loaders or two name:file maps
loader.join_maps(map_a=,map_b=)
# this is for turning any path into an abs path
loader.resolve_path(path)
# this is for saving files that are in the Loader
loader.save(path,map_key)
# this is for saving the current in-memory file map
loader.save_map(path,map)
# this is for getting the Loader map
loader.get_map()
# this is for setting the Loader map
loader.set_map(map)
```
There are more methods in the loader, but they are not mentioned here.
 
### How to handle supported / unsupported file types:
There are two decorators for adding file type support: Load_file and Save_file.
Load_file takes in a lambda that takes in a file object and loads it, and Save_file takes in a lambda that takes in a file object and the data to save. For example:
```json
    ".txt": Load_file(lambda f: f.read()),
    ".json": Load_file(json.load)
```
And for saving:
```json
    ".jpeg": lambda p, d: pygame.image.save(d, p),
    ".txt": Save_file(lambda f, d: f.write(str(d)))
```
note : Load_file and Save_file are decorators that ensure that when the file is open it is safely closed 
 
## Util:
This is a utility class that holds random and potentially useful methods, such as:
- get_angle_and_dist(self,x1:"int",y1:"int",x:"int",y:"int")
- pryoraty(self,a=None,b=None): this function will return `a` if there is an `a`
- snap_cords_in_bounds(self,x:"int",y:"int",max_x:"int",max_y:"int",min_x:"int"=0,min_y:"int"=0): this snaps coordinates inside of a rectangular area
- couculate_dx_dy(self,dist:"int",angle:"float")
- couculate_angle_dist(self,dx:"int",dy:"int")
- play_sound(self,soud_obj:"pygame.mixer.Sound", volume=0.5,loops=0)
- play_sound_from_point(self,pf,sound_pos:list,listener_pos:list,volume:float=0.5,loops=0,distance_fade=0.5)
- warp_image(self,image:"pygame.Surface",sizex:"int",sizey:"int",angle:"float")
- rotate_image(self,image:"pygame.Surface",angle:"float")
- scale_image(self,image:"pygame.Surface",sizex:"int",sizey:"int")
- color_swap(self,surface: 'pygame.Surface', old_color: tuple, new_color: tuple) -> 'pygame.Surface'
How to use the Util class:
```python
import skyport as sp
 
util = sp.Util()
 
a = util.pryoraty(None,2) # a will be 2
 
print(a)
```

## Delta_timer:
This is for getting the delta time between the current call of `get_dt()` and the last one (there is one method -> get_dt()).
```python
dt = sp.Delta_timer()

time_dif = dt.get_dt() 

```
get_dt returns the difference in time from when the instance is created to the call of get_dt and then if you call it again it returns the difference in time from the last call to the current call 
 
## Render :
the render class is a data class holding data like rect,x,y,angle,surface and has a couple utilaty tools and it was made to be used like :
```python

class My_Obj(sp.Render):
    def __init__(self, x, y, width, height, angle, surf = None):
        super().__init__(x, y, width, height, angle, surf)
        # my objs data like health or max speed .......
   
    # rest of class .....

```
the Render class would just automatically handle image scaling and rotating 
Note
    most of the time image updating is automatic when you use set_angle or set_size but if you mod the OG image you will have to call my_class_instance.update_image() for it to update (this might change in a later update)

## Layer :
the layer can hold many objs that inherit the from Render class and then it will automaticly render them to the display every frame and it will call the update function of the Render class every frame 

```python
class my_class(skyport.Render):
    ...

my_layer = skyport.Layer(width=100,height=100)

# you can add layers in layers
my_layer.add_obj(skyport.Layer(...)) 

# you can also add any class that inherits from skyport.Render class
my_layer.add_obj(my_class)

# you can remove obj from a layer
my_layer.remove_obj(my_class)

# if u know the id of an obj u can get it from a layer 
my_layer.get_obj_from_id(1)

# there are more basic methods
```
to use layers and renders to their full potential and render them every frame you just need to put them in your display managers root_layer and then the Renders / Layers will auto update and auto render to the display every frame 
```python
my_layer.add_obj(my_obj)

#the obj and the layer will be drawn to the display and window every frame and it will call the update method of my_obj and my_layer every frame as well
display_manager.root_layer.add_obj(my_layer)
```

### methods :
some of the methods as of this update are :
    - get_surf : this returns the up to date surf 
    - get_pos : this returns -> (x,y)
    - get_size : this returns -> (width,height)
    - set_angle : this sets the angle and auto updates the surf 
    - set_size : this sets the size and auto updates the surf


## Chunked_Layer:
this has been updated but documentation will come in a later update
 
## Chunk:
this has been updated but documentation will come in a later update

 
## SDL2_Display_Manager :
Note:
    this is experimental and might not work on your OS and some features might be broken 
this is the same as Display_Manager but it uses pygames sdl2 to use your gpu (more documentation will come ...)
Note : 
```md
do not call the event handler when using the sdl2 display manager (it might freeze or crash)
```
other Note :
```md
the sdl2 display manager is not complete and has a lot of bugs like auto keybinds dont work and others so if you manage to fix any or just find some you can email me about them and if you can provide a potential fix plz do 
```


# dev_info:
email: matthew.le.robins+proj@gmail.com

    (please only email if you have found a bug and a way to fix it or have a suggestion , and please ensure I have a way to contact you about your suggested changes or requests)
