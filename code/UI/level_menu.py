import pygame
from utils import Button
from global_ import Global
from level import Level
from settings import screen_width, screen_height, levels

class Screen:
	def __init__(self, screen):
		# Basic Setup
		self.display_surface = screen
		self.background = pygame.image.load("../assets/Background/Blue.png").convert_alpha()
		self.background = pygame.transform.scale(self.background, (screen_width, screen_height))

		# Title
		self.font_obj = pygame.font.Font("../assets/Menu/Font/3.otf", 70)
		self.title = self.font_obj.render("Select Level",  True, (0, 0, 0))
		self.title_rect = self.title.get_rect(center=(screen_width//2, 100))

		# Level Buttons
		self.locked_img = pygame.image.load("../assets/Menu/locked.png").convert_alpha()
		self.btns = []
		self.create_levels_buttons()

		# Back Button
		back_btn_image = pygame.transform.scale2x(pygame.image.load("../assets/Menu/Buttons/Back.png").convert_alpha())
		self.back_btn = Button(self.display_surface, (50, 100), image=back_btn_image)

	def create_levels_buttons(self):
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
				button.id = i
				button.locked = True
				self.btns.append(button)
				continue

			if levels[i]["status"] == "locked":
				image.blit(self.locked_img, (0, 0))

			x = ((i - (i//7)*7) - 1)*margin
			y = (i // 7) * margin
			image = pygame.transform.scale(image, (57, 51))
			button = Button(self.display_surface, (offset_x + x, offset_y + y), image=image)
			button.id = i
			button.locked = False

			if levels[i]["status"] == "locked":
				button.locked = True
			
			self.btns.append(button)

	def draw_btns(self):
		for btn in self.btns:
			
			def on_btn_clk():
				Global.level = Level(btn.id)
				Global.history.append(Global.state)
				Global.state = "choose_player"
				Global.current_level = btn.id

			if not btn.locked:
				btn.active(on_btn_clk)
			else:
				btn.draw()

	def on_back_btn_clk(self):
		Global.state = Global.history[-1]
		Global.history.pop()

	def run(self):

		# Background
		self.display_surface.blit(self.background, (0, 0))

		# Title
		self.display_surface.blit(self.title, self.title_rect)

		# Level Buttons
		self.draw_btns()

		# Back Button
		self.back_btn.active(self.on_back_btn_clk)

		# Add it to Global to control level buttons from anywhere
		Global.level_menu = self