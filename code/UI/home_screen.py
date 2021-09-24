import pygame
from settings import screen_width, screen_height
from utils import Button, import_sprite_sheet
from player import Player
from global_ import Global

class PlayerAnimation(Player):
	def __init__(self, pos, scale, player="Virtual Guy"):
		super().__init__(pos, scale, player)
		self.on_ground = True
 
	def update(self):
		self.animate(0.4)
			
class Screen(pygame.sprite.Sprite):
	def __init__(self, display_surface):
		super().__init__()
		self.key_pressed = True

		# Basic Setup
		font = pygame.font.Font("../assets/Menu/Font/3.otf", 70)
		self.font = font.render("Platformer 2D", True, (0, 0, 0))
		self.background = pygame.image.load("../assets/Background/Blue.png").convert_alpha()
		self.background = pygame.transform.scale(self.background, (screen_width, screen_height))
		self.display_surface = display_surface
		pos_x = screen_width / 2
		pos_y = screen_height - 200
		btn_config = {
			"size": (250, 60),
			"color": (61, 178, 255),
			"border_radius": 20,
			"text": "Click To Play",
			"text_size": 50,
			"text_color": (0, 0, 0),
			"outline": 1,
			"hover": (0, 255, 0)
		}
		self.play_btn = Button(self.display_surface, (pos_x, pos_y), btn_config)

		# Player
		player = PlayerAnimation((screen_width/2, 300), (150, 150), player="Pink Man")
		self.player = pygame.sprite.GroupSingle(player)

	def play_btn_clk(self):
		self.key_pressed = True
		Global.history.append(Global.state)
		Global.state = "level_select"

	def input(self):
		keys = pygame.key.get_pressed()

		if keys[pygame.K_RETURN] and not self.key_pressed:
			self.key_pressed = True
			self.play_btn.press()

		elif not any(keys) and self.key_pressed:
			self.key_pressed = False

	def run(self):
		# Background
		self.display_surface.blit(self.background, (0, 0))

		# Heading
		pos = self.font.get_rect(center=(screen_width/2, 100))
		self.display_surface.blit(self.font, pos)

		# Keyboard Input
		self.input()

		# Play Button
		self.play_btn.active(self.play_btn_clk)

		# Player Animation
		self.player.draw(self.display_surface)
		self.player.update()