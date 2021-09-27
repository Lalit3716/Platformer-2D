import pygame
from utils import Button
from global_ import Global
from level import Level
from settings import screen_width, screen_height, levels

class Screen:
	def __init__(self, screen):
		self.key_pressed = True
		
		# sfx
		self.click_sound = pygame.mixer.Sound("../assets/Audio/Interface/click_003.ogg")
		self.back_sound = pygame.mixer.Sound("../assets/Audio/Interface/tick_002.ogg")
		self.drop_sound = pygame.mixer.Sound("../assets/Audio/Interface/drop_003.ogg")

		# Basic Setup
		self.display_surface = screen
		self.background = pygame.image.load("../assets/Background/Blue.png").convert_alpha()
		self.background = pygame.transform.scale(self.background, (screen_width, screen_height))

		# Title
		self.font_obj = pygame.font.Font("../assets/Menu/Font/3.otf", 70)
		self.title = self.font_obj.render("Select Level",  True, (0, 0, 0))
		self.title_rect = self.title.get_rect(center=(screen_width//2, 100))

		# Level Buttons
		self.unlocked_levels = 0
		self.locked_img = pygame.image.load("../assets/Menu/locked.png").convert_alpha()
		self.btns = []
		self.fns = []
		self.selected_btn = -1
		self.create_levels_buttons()
		self.create_on_clk_fns()
		self.btns[self.selected_btn].focus()

		# Back Button
		back_btn_image = pygame.transform.scale2x(pygame.image.load("../assets/Menu/Buttons/Back.png").convert_alpha())
		self.back_btn = Button(self.display_surface, (50, 100), image=back_btn_image)

	def create_levels_buttons(self):
		self.btns.clear()
		self.unlocked_levels = 0
		offset_x = 350
		offset_y = 200
		margin = 80
		for i in range(1, 42):
			
			level = f"{i}".zfill(2)
			image = pygame.image.load(f"../assets/Menu/Levels/{level}.png").convert_alpha() 

			if i > Global.max_level:
				image = pygame.transform.scale(image, (57, 51))
				tint_surface = image.copy()
				tint_surface.fill("#000000AA", None, pygame.BLEND_RGBA_MULT)
				image.blit(tint_surface, (0, 0))
				x = ((i - (i//7)*7) - 1)*margin
				y = (i // 7) * margin
				button = Button(self.display_surface, (offset_x + x, offset_y + y), image=image)
				button.on = False
				self.btns.append(button)
				continue
			
			path = f"../assets/Menu/Levels/{level}_hover.png"
			hover_image = pygame.image.load(path).convert_alpha()
			hover_image = pygame.transform.scale(hover_image, (57, 51))

			if levels[i]["status"] == "locked":
				image.blit(self.locked_img, (0, 0))

			x = ((i - (i//7)*7) - 1)*margin
			y = (i // 7) * margin
			image = pygame.transform.scale(image, (57, 51))
			button = Button(self.display_surface, (offset_x + x, offset_y + y), image=image, hover_image=hover_image)
			button.on = True

			if levels[i]["status"] == "unlocked":
				self.unlocked_levels += 1

			if levels[i]["status"] == "locked":
				button.on = False
			
			self.btns.append(button)

	def create_on_clk_fns(self):
		for i in range(len(self.btns)):
			on_click_fn = self.make_clk_func(i + 1)
			self.fns.append(on_click_fn)

	def make_clk_func(self, i):
		def inner():
			self.click_sound.play()
			self.key_pressed = True
			Global.level = Level(i)
			Global.history.append(Global.state)
			Global.state = "choose_player"
			Global.current_level = i
			Global.lives = 3

		return inner

	def draw_btns(self):
		for btn in self.btns:
			btn.active(self.fns[self.btns.index(btn)])

	def on_back_btn_clk(self):
		self.back_sound.play()
		self.key_pressed = True
		Global.state = Global.history[-1]
		Global.history.pop()

	def input(self):
		keys = pygame.key.get_pressed()

		if keys[pygame.K_ESCAPE] and not self.key_pressed:
			self.key_pressed = True
			self.back_btn.press()

		if keys[pygame.K_RIGHT] and not self.key_pressed:
			self.drop_sound.play()
			self.key_pressed = True
			if self.selected_btn < self.unlocked_levels - 1:
				self.selected_btn += 1
			else:
				self.selected_btn = 0

			for i in range(self.unlocked_levels):
				if i == self.selected_btn:
					self.btns[i].focus()
				else:
					self.btns[i].unfocus()

		if keys[pygame.K_LEFT] and not self.key_pressed:
			self.drop_sound.play()
			self.key_pressed = True
			if self.selected_btn > 0:
				self.selected_btn -= 1
			else:
				self.selected_btn = self.unlocked_levels - 1

			for i in range(self.unlocked_levels):
				if i == self.selected_btn:
					self.btns[i].focus()
				else:
					self.btns[i].unfocus()

		if keys[pygame.K_RETURN] and not self.key_pressed:
			self.key_pressed = True
			self.btns[self.selected_btn].press()

		if (not any(keys)) and self.key_pressed:
			self.key_pressed = False

	def run(self):

		# Background
		self.display_surface.blit(self.background, (0, 0))

		# Title
		self.display_surface.blit(self.title, self.title_rect)

		# Input
		self.input()

		# Level Buttons
		self.draw_btns()

		# Back Button
		self.back_btn.active(self.on_back_btn_clk)

		# Add it to Global to control level buttons from anywhere
		Global.level_menu = self