import pygame
from utils import import_sprite_sheet
from settings import tile_size

class TerrainTile(pygame.sprite.Sprite):
	def __init__(self, pos, tile=None):
		super().__init__()
		self.tile_no = int(tile)
		self.tiles = import_sprite_sheet("../assets/Terrain/Terrain (16x16).png", (16, 16))
		self.image = pygame.Surface((tile_size, tile_size))
		self.image.set_colorkey((0, 0, 0))
		self.image.blit(self.tiles[self.tile_no], (0, 0))
		self.rect = self.image.get_rect(topleft=pos)
		
	def update(self, world_shift_x, world_shift_y, surface):
		self.rect.centerx += world_shift_x
		self.rect.centery += world_shift_y

class LimitTile(pygame.sprite.Sprite):
	def __init__(self, pos, type):
		super().__init__()
		self.type = type
		self.image = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
		self.rect = self.image.get_rect(topleft=pos)

	def update(self, world_shift_x, world_shift_y):
		self.rect.centerx += world_shift_x
		self.rect.centery += world_shift_y