import pygame
from global_ import Global
from settings import screen_width, screen_height

class Hud:
	def __init__(self):
		# Font
		self.font_obj = pygame.font.Font(None, 35)

		# Pannel and Display
		self.display_surface = pygame.display.get_surface()
		
		# Score
		self.score_img = pygame.image.load("../assets/Items/Fruits/Apple_Tile.png").convert_alpha()
		self.score_img = pygame.transform.scale2x(self.score_img)

		# Lives
		self.heart_img = pygame.image.load("../assets/Menu/Font/emoji2.png").convert_alpha()
		self.heart_img = pygame.transform.scale(self.heart_img, (30, 30))

	def draw_score(self):
		self.score = Global.score
		score_font = self.font_obj.render(f"X {self.score}", True, (0, 0, 0))
		score_font_pos = score_font.get_rect(topleft=(70, 45))
		self.display_surface.blit(self.score_img, (15, 25))
		self.display_surface.blit(score_font, score_font_pos)
		
	def draw_health(self):
		current_level_font = self.font_obj.render(f"Level - {Global.current_level}", True, (0, 0, 0))
		self.lives = Global.lives
		lives_font = self.font_obj.render(f"X {self.lives}", True, (0, 0, 0))
		lives_font_pos = lives_font.get_rect(topleft=(screen_width//2 + 40, 45))
		self.display_surface.blit(self.heart_img, (screen_width//2, 40))
		self.display_surface.blit(lives_font, lives_font_pos)
		self.display_surface.blit(current_level_font, (screen_width//2, 80))

	def draw(self):		
		self.draw_score()
		self.draw_health()