from utils import import_level

levels = {
	1: {"level_data": import_level("../TileMaps/0"), "color": "Yellow", "status": "unlocked"}, 
	2: {"level_data": import_level("../TileMaps/1"), "color": "Green", "status": "unlocked"}}

tile_size = 16
screen_width = 1024
screen_height = len(levels[1]["level_data"]["terrain"]) * tile_size