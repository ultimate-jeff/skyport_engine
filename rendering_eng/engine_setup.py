import pygame
import json
import os


print("[SETUP] Creating minimal engine filesystem...")

# -------------------------------------------------
# REQUIRED FOLDERS (including empty asset folders)
# -------------------------------------------------
folders = [
    "data",
    "data/GFmaps",
    "data/texture_maps",
    "images",

    # empty but required game asset folders
    "props",
    "planes",
    "Paricals",
    "wepons",

    # their stats folders
    "props/stats",
    "planes/stats",
    "Paricals/stats",
    "wepons/wepon_stats"
]

for f in folders:
    if not os.path.exists(f):
        os.makedirs(f)
        print(f"[SETUP] Created folder: {f}")

# -------------------------------------------------
# REQUIRED JSON FILES WITH MINIMAL VALID CONTENT
# (engine will crash without these)
# -------------------------------------------------

# death messages
death_msgs = {
    "shot_down": "You were shot down by {player}",
    "out_of_bounds": "You went out of bounds",
    "crashed": "You crashed"
}

# settings
settings = {
    "xpp": 4,
    "volume": 1.0,
    "death_songs": []
}

# GF map (points to essential JSON files)
gf_map = {
    "data/death_msgs.json": False,
    "data/settings.json": False
}

# texture map (only watter.png is required)
texture_map = {
    "images/watter.png": False
}

json_files = {
    "data/death_msgs.json": death_msgs,
    "data/settings.json": settings,
    "data/GFmaps/Main.json": gf_map,
    "data/texture_maps/D1.json": texture_map
}

for path, content in json_files.items():
    if not os.path.exists(path):
        with open(path, "w") as f:
            json.dump(content, f, indent=4)
        print(f"[SETUP] Created file: {path}")

# -------------------------------------------------
# DEFAULT WATER PNG
# -------------------------------------------------
water_path = "images/watter.png"
if not os.path.exists(water_path):
    pygame.init()
    surf = pygame.Surface((32, 32))
    surf.fill((50, 100, 255))  # basic blue
    pygame.image.save(surf, water_path)
    print(f"[SETUP] Created default image: {water_path}")

print("[SETUP] Minimal filesystem complete!")
