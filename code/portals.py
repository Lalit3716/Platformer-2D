import pygame
from utils import import_sprite_sheet
from global_ import Global

class Portal(pygame.sprite.Sprite):
	def __init__(self, pos, type):
		super().__init__()
		self.display_surface = pygame.display.get_surface()
		self.image = pygame.image.load("../assets/Other/Transition.png").convert_alpha()
		self.rect = self.image.get_rect(center=pos)
		self.index = 0
		self.timer = 30
		self.allowed = False
		self.type = type
		if self.type == "appearing":
			self.frames = import_sprite_sheet("../assets/Main Characters/Appearing (96x96).png", (96, 96))
		elif self.type == "disappearing":
			self.frames = import_sprite_sheet("../assets/Main Characters/Desappearing (96x96).png", (96, 96))
		
	def animate(self, speed=0.4):
		self.index += speed
		if self.index >= len(self.frames):
			self.index = 0
			if self.type == "appearing":
				Global.level.level_just_started = False
			elif self.type == "disappearing":
				self.allowed = True
			self.kill()
		self.frame = self.frames[int(self.index)]
		self.display_surface.blit(self.frame, (self.rect.center[0]-50, self.rect.center[1]-50))

	def update(self, world_shift_x, world_shift_y):
		self.rect.centerx += world_shift_x
		self.rect.centery += world_shift_y
		self.timer -= 1
		if self.timer <= 0 and self.type=="appearing":
			self.animate(0.2)