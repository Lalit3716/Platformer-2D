import pygame
from settings import screen_width, screen_height
from utils import Button
from global_ import Global
from player import Player

class PlayerAnimation(Player):
	def __init__(self, pos, scale, player="Virtual Guy"):
		super().__init__(pos, scale, player)

	def base(self):
		if self.rect.y >= 200:
			self.on_ground = True
			self.rect.y = 200
			self.direction.y = 0

	def get_jump_states(self):
		keys = pygame.key.get_pressed()

		if keys[pygame.K_SPACE] and self.on_ground:
			self.direction.y = -10
			self.state = "Jump"

	def update(self):
		if Global.level:
			self.create_jump_particles = Global.level.create_jump_particles
		self.get_input()
		self.get_state()
		self.get_jump_states()
		self.apply_gravity()
		self.animate(0.3)
		self.base()

class Screen:
	def __init__(self, screen):
		self.key_pressed = True

		# Basic Setup
		self.display_surface = screen
		self.font = pygame.font.Font("../assets/Menu/Font/3.otf", 70)
		self.font_surface = self.font.render("Controls", True, (0, 0, 0))
		self.font_pos = self.font_surface.get_rect(center=(screen_width//2, 100))
		self.background = pygame.image.load("../assets/Background/Brown.png").convert_alpha()
		self.background = pygame.transform.scale(self.background, (screen_width, screen_height))

		# Player
		player = PlayerAnimation((screen_width/2+300, 300), (200, 200), player="Pink Man")
		self.player = pygame.sprite.GroupSingle(player)

		# Back Button
		back_btn_image = pygame.transform.scale2x(pygame.image.load("../assets/Menu/Buttons/Back.png").convert_alpha())
		self.back_btn = Button(self.display_surface, (200, 100), image=back_btn_image)

		# Controls Images
		self.spacebar = pygame.image.load("../assets/Menu/spacebar.png").convert_alpha()
		self.enter = pygame.image.load("../assets/Menu/enter.png").convert_alpha()
		self.left_arrow_key = pygame.image.load("../assets/Menu/left_arrow_key.png").convert_alpha()
		self.right_arrow_key = pygame.image.load("../assets/Menu/right_arrow_key.png").convert_alpha()
		self.esc_key = pygame.image.load("../assets/Menu/esc_key.png").convert_alpha()

		# Instruction Fonts
		self.small_font = pygame.font.Font("../assets/Menu/Font/3.otf", 20)
		self.create_instructions()

	def create_instructions(self):
		self.move_x_text = self.small_font.render("Move Left/Right", False, (0, 0, 0))
		self.move_x_text_pos = self.move_x_text.get_rect(topleft=(350, 260))
		self.jump_text = self.small_font.render("Jump", False, (0, 0, 0))
		self.jump_text_pos = self.jump_text.get_rect(topleft=(360, 310))
		self.back_text = self.small_font.render("Go Back In Menu's / Pause", False, (0, 0, 0))
		self.back_text_pos = self.back_text.get_rect(topleft=(350, 360))
		self.select_text = self.small_font.render("Select Options In Menu's", False, (0, 0, 0))
		self.select_text_pos = self.select_text.get_rect(topleft=(350, 410))

	def blit_instructions(self):
		self.display_surface.blit(self.move_x_text, self.move_x_text_pos)
		self.display_surface.blit(self.jump_text, self.jump_text_pos)
		self.display_surface.blit(self.back_text, self.back_text_pos)
		self.display_surface.blit(self.select_text, self.select_text_pos)

	def blit_controls(self):
		self.display_surface.blit(self.left_arrow_key, (250, 250))
		self.display_surface.blit(self.right_arrow_key, (280, 250))
		self.display_surface.blit(self.spacebar, (200, 300))
		self.display_surface.blit(self.esc_key, (250, 350))
		self.display_surface.blit(self.enter, (250, 400))

	def on_back_btn_clk(self):
		self.key_pressed = True
		Global.state = Global.history[-1]
		Global.history.pop()

	def input(self):
		keys = pygame.key.get_pressed()

		if keys[pygame.K_ESCAPE] and not self.key_pressed:
			self.key_pressed = True
			self.back_btn.press()

		if not any(keys) and self.key_pressed:
			self.key_pressed = False

	def run(self):
		# Background And Font
		self.display_surface.blit(self.background, (0, 0))
		self.display_surface.blit(self.font_surface, self.font_pos)

		# Input
		self.input()

		# Animations
		self.player.draw(self.display_surface)
		self.player.update()
		
		# Back Button
		self.back_btn.active(self.on_back_btn_clk)

		# Blit Controls
		self.blit_controls()
		self.blit_instructions()