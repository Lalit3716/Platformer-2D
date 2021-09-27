import pygame
from settings import screen_width, screen_height
from global_ import Global
from utils import Button

class Screen:
	def __init__(self, surface):
		self.key_pressed = False

		# sfx
		self.click_sound = pygame.mixer.Sound("../assets/Audio/Interface/click_003.ogg")

		# Setup
		self.display_surface = surface
		self.background = pygame.image.load("../assets/Background/Blue.png").convert_alpha()
		self.background = pygame.transform.scale(self.background, (screen_width, screen_height))

		# Title
		self.font = pygame.font.Font("../assets/Menu/Font/3.otf", 45)
		self.font_surface1 = self.font.render("No More Levels Yet", True, (0, 0, 0))
		self.font1_pos = self.font_surface1.get_rect(center=(screen_width//2, 100))
		self.emoji1 = pygame.image.load("../assets/Menu/Font/emoji1.png").convert_alpha()
		self.emoji1_rect = self.emoji1.get_rect(center=(screen_width//2, 170))

		self.font_surface2 = self.font.render("But Thank You For Playing!", True, (0, 0, 0))
		self.font2_pos = self.font_surface2.get_rect(center=(screen_width//2, 250))

		self.font_surface3 = self.font.render("Made With", True, (0, 0, 0))
		self.font3_pos = self.font_surface3.get_rect(center=(screen_width//2, 600))
		self.emoji2 = pygame.image.load("../assets/Menu/Font/emoji2.png").convert_alpha()
		self.emoji2_rect = self.emoji2.get_rect(center=(screen_width//2+220, 600))

		# Menu Button
		self.main_btn_config = {
			"size": (150, 60),
			"color": (61, 178, 255),
			"border_radius": 20,
			"text": "Home",
			"text_size": 50,
			"text_color": (0, 0, 0),
			"outline": 1,
			"hover": (0, 255, 0)
		}
		self.main_menu_btn = Button(self.display_surface, (screen_width//2, screen_height//2+80), self.main_btn_config)

	def on_main_menu_btn_clk(self):
		self.key_pressed = True
		self.click_sound.play()
		Global.state = "opening_scene"

	def input(self):
		keys = pygame.key.get_pressed()

		if keys[pygame.K_RETURN]:
			self.key_pressed = True
			self.main_menu_btn.press()

		elif not any(keys) and self.key_pressed:
			self.key_pressed = False

	def run(self):
		# Background
		self.display_surface.blit(self.background, (0, 0))

		# Input
		self.input()

		# Text
		self.display_surface.blit(self.font_surface1, self.font1_pos)
		self.display_surface.blit(self.emoji1, self.emoji1_rect)
		self.display_surface.blit(self.font_surface2, self.font2_pos)
		self.display_surface.blit(self.font_surface3, self.font3_pos)
		self.display_surface.blit(self.emoji2, self.emoji2_rect)

		# Button
		self.main_menu_btn.active(self.on_main_menu_btn_clk)