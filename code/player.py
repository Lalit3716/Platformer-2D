import pygame, os
from utils import import_character
from settings import levels
from global_ import Global

class Player(pygame.sprite.Sprite):
	def __init__(self, pos, scale=(50, 50), player="Virtual Guy"):
		super().__init__()
		# Animations
		self.player = player
		self.scale = scale
		self.states = {"Idle": [], "Run": [], "Fall": [], "Jump": [], "Hit": []}
		self.state = "Idle"
		self.animations = import_character(self.states, ("Main Characters", self.player), (32, 32), self.scale)
		self.frame_index = 0
		self.flip = False

		# Image
		self.image = self.animations[self.state][self.frame_index]
		self.rect = self.image.get_rect(center=pos)
		self.rect.size = (self.rect.size[0]-10,self.rect.size[1])

		# Positions
		self.on_ground = False
		self.on_ceiling = False

		# Movements
		self.gravity = 1
		self.direction = pygame.math.Vector2(0, 0)
		self.speed = 5
		self.jump_force = -19
		self.hit = False
		self.hit_cooldown = 10

	def get_state(self):
		if self.hit:
			self.state = "Hit"
			return

		if self.direction.x != 0:
			self.state = "Run"
			
		else:
			self.state = "Idle"

		if self.direction.y >= self.gravity:
			self.state = "Fall"
			self.on_ground = False
		elif self.direction.y < 0:
			self.state = "Jump"

	def animate(self, speed):
		self.frame_index += speed
		if self.frame_index >= len(self.animations[self.state]):
			self.frame_index = 0
		self.image = self.animations[self.state][int(self.frame_index)]
		self.image = pygame.transform.flip(self.image, self.flip, False)

	def apply_gravity(self):
		self.direction.y += self.gravity
		self.rect.y += self.direction.y

	def get_input(self):
		keys = pygame.key.get_pressed()
		
		if keys[pygame.K_RIGHT]:
			self.direction.x = 1
			self.flip = False

		elif keys[pygame.K_LEFT]:
			self.direction.x = -1
			self.flip = True

		else:
			self.direction.x = 0

		if keys[pygame.K_SPACE] and self.on_ground:
			self.jump()

	def jump(self):
		self.direction.y = self.jump_force	
		self.on_ground = False
		self.on_ceiling = False

	def move(self):
		self.rect.x += self.direction.x * self.speed

	def take_hit(self, groups):
		for group in groups:
			for sprite in group.sprites():
				if sprite.rect.colliderect(self.rect):
					if not self.direction.y > 0 and not sprite.dying:
						self.hit = True
		
	def update(self):
		self.get_input()
		self.get_state()
		self.animate(0.4)
		if self.hit:
			self.hit_cooldown -= 1
			if self.hit_cooldown <= 0:
				self.hit = False
				self.hit_cooldown = 30