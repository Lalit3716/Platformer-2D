import pygame
from settings import screen_width, screen_height
from utils import Button
from global_ import Global

class Screen:
	def __init__(self, screen):
		self.key_pressed = True

		# Display
		self.display_surface = screen
		self.background = pygame.image.load("../assets/Background/Blue.png").convert_alpha()
		self.background = pygame.transform.scale(self.background, (screen_width, screen_height))

		# Font
		self.font = pygame.font.Font("../assets/Menu/Font/3.otf", 50)
		self.font_surface = self.font.render("Game Over", True, (0, 0, 0))
		self.font_pos = self.font_surface.get_rect(center=(screen_width/2, 100))

		# Restart Button
		self.restart_btn_pos = (screen_width/2, screen_height/2)
		self.restart_btn_config = {
			"size": (250, 60),
			"color": (61, 178, 255),
			"border_radius": 20,
			"text": "Restart",
			"text_size": 50,
			"text_color": (0, 0, 0),
			"outline": 1,
			"hover": (0, 255, 0)
		}
		self.restart_btn = Button(self.display_surface, self.restart_btn_pos, self.restart_btn_config)

	def on_restart_btn_click(self):
		self.key_pressed = True
		Global.state = "playing"
		Global.level.reset()

	def input(self):
		keys = pygame.key.get_pressed()

		if keys[pygame.K_RETURN]:
			self.key_pressed = True
			self.restart_btn.press()

		elif not any(keys) and self.key_pressed:
			self.key_pressed = False

	def run(self):
		# Background
		self.display_surface.blit(self.background, (0, 0))	

		# Font
		self.display_surface.blit(self.font_surface, self.font_pos)

		# Input
		self.input()

		# Restart Button
		self.restart_btn.active(self.on_restart_btn_click)