import pygame, os
from utils import import_character
from settings import screen_height

class Enemy(pygame.sprite.Sprite):
	def __init__(self, pos, states, character, size, scale=None):
		super().__init__()
		self.dying = False
		self.states = states
		self.animations = import_character(self.states, (character[0], character[1]), size, scale)
		self.state = "Idle"
		self.index = 0
		self.image = self.animations[self.state][int(self.index)]
		self.rect = self.image.get_rect(center=pos)
		self.animate_speed = 0.2
		self.shrink = False

	def apply_shrink(self, shrink):
		shrink_vector = pygame.math.Vector2(shrink, shrink)
		self.scale = self.rect.size - shrink_vector
		self.scale = (int(self.scale.x), int(self.scale.y))
		if self.scale[0] >= 0 and self.scale[1] >= 0: 
			self.image = pygame.transform.scale(self.image, self.scale)
		else:
			self.kill()
		self.rect = self.image.get_rect(center = self.rect.center)

	def take_hit(self):
		self.state = "Hit"
		self.animate_speed = 0.1
		self.dying = True

	def on_hit_animation_finished(self):
		pass

	def animate(self):
		self.index += self.animate_speed
		if self.index >= len(self.animations[self.state]):
			self.index = 0
			if self.state == "Hit" or self.state == "Hit 1" or self.state=="Hit 2":
				self.on_hit_animation_finished()
		self.image = self.animations[self.state][int(self.index)]

class Rino(Enemy):
	def __init__(self, pos):
		states = {"Hit": [], "Hit Wall": [], "Idle": [], "Run": []}
		super().__init__(pos, states, ("Enemies", "Rino"), (52, 34))
		self.speed = 1
		self.flip = False
		self.state = "Run"
		self.name = "Rino"

	def move(self, limits):
		self.rect.x += self.speed
		for limit in limits.sprites():
			if limit.rect.colliderect(self.rect):
				if abs(self.rect.left-limit.rect.right) <= 5 and self.speed < 0:
					self.speed *= -1
				if abs(self.rect.right-limit.rect.left) <= 5 and self.speed > 0:
					self.speed *= -1
		if self.speed < 0:
			self.flip = False
		else:
			self.flip = True
		self.image = pygame.transform.flip(self.image, self.flip, False)	

	def on_hit_animation_finished(self):
		self.shrink = True
		self.speed = 0

	def update(self, world_shift_x, world_shift_y, limits):
		self.rect.centerx += world_shift_x
		self.rect.centery += world_shift_y
		self.animate()
		self.move(limits)
		if self.shrink:
			self.apply_shrink(1)

class AngryPig(Enemy):
	def __init__(self, pos):
		states = {"Hit 1": [], "Hit 2": [], "Idle": [], "Run": [], "Walk": []}
		super().__init__(pos, states, ("Enemies", "AngryPig"), (36, 30))
		self.dying = False
		self.speed = 1
		self.flip = False
		self.hitpoints = 0
		self.state = "Walk"
		self.name = "AngryPig"

	def move(self, limits):
		self.rect.x += self.speed
		for limit in limits.sprites():
			if limit.rect.colliderect(self.rect):
				if abs(self.rect.left-limit.rect.right) <= 5 and self.speed < 0:
					self.speed *= -1
				if abs(self.rect.right-limit.rect.left) <= 5 and self.speed > 0:
					self.speed *= -1	

		if self.speed < 0:
			self.flip = False
		else:
			self.flip = True
		self.image = pygame.transform.flip(self.image, self.flip, False)	

	def take_hit(self):
		self.hitpoints += 1
		if self.hitpoints==1:
			self.state = "Hit 1"
			self.animate_speed = 0.1
			self.speed = self.speed * 4
		elif self.hitpoints==2:
			self.state = "Hit 2"
			self.dying = True
			self.animate_speed = 0.1
	
	def on_hit_animation_finished(self):
		if self.hitpoints >= 2:
			self.shrink = True
			self.speed = 0
		else:
			self.animate_speed = 0.2
			self.state = "Run"

	def update(self, world_shift_x, world_shift_y, limits):
		self.rect.centerx += world_shift_x
		self.rect.centery += world_shift_y
		self.animate()
		self.move(limits)
		if self.shrink:
			self.apply_shrink(1)

class Trunk(Enemy):
	def __init__(self, pos, flip):
		states = {"Hit": [], "Attack": [], "Idle": [], "Run": []}
		super().__init__(pos, states, ("Enemies", "Trunk"), (64, 32))
		self.flip = flip

	def update(self, world_shift_x, world_shift_y, limits=None):
		self.rect.centerx += world_shift_x
		self.rect.centery += world_shift_y