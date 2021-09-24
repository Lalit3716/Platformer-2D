import pygame, csv, os

class Button:
	def __init__(self, surface, pos, config=None, image=None, hover_image=None):
		# Basic Setup
		self.display_surface = surface
		self.config = config
		self.image = image
		self.hover_image = hover_image
		self.clicked = False
		self.focused = None
		self.on = True

		# Button Surface
		if image:
			self.button = image
		
		else:
			self.button = pygame.Surface(config["size"])
			self.button.set_colorkey((0, 0, 0))
			# Text
			if config["text"]:
				self.font = pygame.font.Font(None, config["text_size"])
			else:
				self.config["text"] = None

			# Colors
			self.color = config["color"]
			
			if config["hover"]:
				self.hover = config["hover"]

		self.button_orginal_copy = self.button.copy()
		self.rect = self.button.get_rect(center=pos)
		
	def check_click(self, onClick):
		left_click = pygame.mouse.get_pressed()[0]
		
		if not self.image:
			if self.config["hover"] and self.on:
				if self.rect.collidepoint(pygame.mouse.get_pos()):
					self.config["color"] = self.hover
				elif not self.focused:
					self.config["color"] = self.color

		if left_click and not self.clicked:
			self.clicked = True
			if self.rect.collidepoint(pygame.mouse.get_pos()):
				if onClick and self.on:
					onClick()
		
		elif not left_click and self.clicked:
			self.clicked = False

	def hover_for_image_btn(self):
		if self.rect.collidepoint(pygame.mouse.get_pos()):
			self.image.blit(self.hover_image, (0, 0))
		elif not self.focused:
			self.image.blit(self.button_orginal_copy, (0, 0))

	def focus(self):
		if self.config:
			self.focused = True
			self.config["color"] = self.hover
		elif self.hover_image:
			self.focused = True
			self.button.blit(self.hover_image, (0, 0))

	def unfocus(self):
		
		if self.config:
			self.focused = False
			self.config["color"] = self.color

		elif self.hover_image:
			self.focused = False
			self.button.blit(self.button_orginal_copy, (0, 0))

	def press(self):
		if self.on:
			self.onClick()

	def grey_out(self):
		self.config["color"] = "grey"
		self.on = False

	def normal(self):
		self.config["color"] = self.color
		self.on = True

	def draw(self):
		btn = self.config
		
		if not self.image:
			pygame.draw.rect(self.display_surface, btn["color"], self.rect, border_radius=btn["border_radius"])
			if btn["outline"]:
				pygame.draw.rect(self.display_surface, (0, 0, 0), self.rect, border_radius=btn["border_radius"], width=btn["outline"])

			# Text
			if btn["text"]:
				text_surface = self.font.render(btn["text"], False, btn["text_color"])
				pos = text_surface.get_rect(center = self.rect.center)
				self.display_surface.blit(text_surface, pos)

		else:
			self.display_surface.blit(self.button, self.rect)

	def active(self, onClick=None):
		self.onClick = onClick
		self.check_click(onClick)
		self.draw()
		if self.hover_image and self.on:
			self.hover_for_image_btn()

def import_sprite_sheet(path, size_of_one_frame, scale=None):
	size = size_of_one_frame
	frames = []
	sprite_sheet = pygame.image.load(path).convert_alpha()
	width = sprite_sheet.get_width()
	height = sprite_sheet.get_height()
	rows = int(height / size[1])
	
	for row in range(rows):
		frame_no = 0
		while frame_no * size[0] < width:
			frame = pygame.Surface(size)
			rect = (frame_no * size[0], row * size[1], size[0], size[1])
			frame.blit(sprite_sheet, (0, 0), rect)
			frame.set_colorkey((0, 0, 0))
			if scale:
				frame = pygame.transform.scale(frame, scale)
			frames.append(frame)
			frame_no += 1

	return frames

def import_csv(path):
	map = []
	with open(path) as f:
		data = csv.reader(f, delimiter=",")
		for row in data:
			map.append(list(row))		
	return map

def import_level(path):
	level_data = {}
	for _, __, file in os.walk(path):
		for i in range(len(file)):
			file_path = path + "/" + file[i]
			data = import_csv(file_path)
			level_data[file[i].rstrip(".csv").replace("map_", "")] = data

	return level_data		

def import_character(states, character, size, scale=None):
	animations = {}
	size_str = str(size).replace(", ", "x")
	for animation in states.keys():
		path = os.path.join("../assets", character[0], character[1], f"{animation} {size_str}.png")
		animations[animation] = import_sprite_sheet(path, size, scale)
	return animations