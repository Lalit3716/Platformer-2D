from settings import levels

class Global:
	state = "opening_scene"
	level = None
	current_level = 1
	max_level = len(levels)
	history = []