import pygame
from utils import import_sprite_sheet
from settings import screen_height, tile_size

class AnimatedSprite(pygame.sprite.Sprite):
	def __init__(self, pos, path, size, scale):
		super().__init__()
		self.path = path
		self.size_of_one_frame = size
		self.scale = scale
		self.frames = import_sprite_sheet(
			self.path, 
			self.size_of_one_frame,
			scale=self.scale
			)
		self.index = 0
		self.image = self.frames[self.index]
		self.rect = self.image.get_rect(center=pos)
		self.rect.size = (self.rect.size[0]-10, self.rect.size[1])

	def animate(self, speed):
		self.index += speed
		if self.index >= len(self.frames):
			self.index = 0
		self.image = self.frames[int(self.index)]

	def update(self, world_shift_x, world_shift_y):
		self.rect.centerx += world_shift_x
		self.rect.centery += world_shift_y
		self.animate(0.4)

class Fruit(AnimatedSprite):
	def __init__(self, pos, fruit):
		offset = pygame.math.Vector2(tile_size//2, -tile_size//2)
		pos = pos + offset
		path = f"../assets/Items/Fruits/{fruit}.png"
		size = (32, 32)
		scale = (30, 30)
		super().__init__(pos, path, size, scale)

class SawTrap(AnimatedSprite):
	def __init__(self, pos):
		super().__init__(pos, "../assets/Traps/Saw/On (38x38).png", (38, 38), (38, 38))
		self.speed = pygame.math.Vector2(3, 0)
		self.dying = False
		self.name = "SawTrap"

	def move(self):
		self.rect.x += self.speed.x
		self.rect.y += self.speed.y

	def check_platforms(self, platforms):
		for sprite in platforms.sprites():
			if sprite.rect.colliderect(self.rect):
				if sprite.type == "topright":
					self.speed.x = 0
					self.speed.y = 3
				if sprite.type == "bottomright":
					self.speed.x = -3
					self.speed.y = 0
				if sprite.type == "bottomleft":
					self.speed.x = 0
					self.speed.y = -3
				if sprite.type == "topleft":
					self.speed.x = 3
					self.speed.y = 0

	def update(self, world_shift_x, world_shift_y, platforms):
		super().update(world_shift_x, world_shift_y)
		self.move()
		self.check_platforms(platforms)

class FallingTrap(AnimatedSprite):
	def __init__(self, pos):
		super().__init__(pos, "../assets/Traps/Falling Platforms/On (32x10).png", (32, 10), (32, 10))
		self.gravity = 15
		self.timer = 10
		self.activate_timer = False

	def fall(self):
		self.activate_timer = True

	def countdown(self):
		self.timer -= 1

	def destroy(self):
		if self.rect.y >= screen_height:
			self.kill()

	def update(self, world_shift_x, world_shift_y):
		super().update(world_shift_x, world_shift_y)
		if self.activate_timer:
			self.countdown()
		if self.timer <= 0:
			self.rect.y += self.gravity
		self.destroy()