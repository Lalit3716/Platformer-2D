import pygame, os
from utils import import_character, import_folder
from settings import levels
from global_ import Global

class Player(pygame.sprite.Sprite):
	def __init__(self, pos, scale=(50, 50), player="Virtual Guy"):
		super().__init__()
		self.display_surface = pygame.display.get_surface()

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
		self.collideable = True
		self.gravity = 1
		self.direction = pygame.math.Vector2(0, 0)
		self.speed = 5
		self.hit = False
		self.hit_cooldown = 10

		# Run Particles
		self.run_particles_frames = import_folder("../assets/Main Characters/dust_particles/run")
		self.run_particles_index = 0

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
			if self.state == "Hit":
				self.frame_index = len(self.animations["Hit"]) - 1

		self.image = self.animations[self.state][int(self.frame_index)]
		self.image = pygame.transform.flip(self.image, self.flip, False)

	def run_particles_animate(self, speed=0.4):
		self.run_particles_index += speed

		if self.run_particles_index >= len(self.run_particles_frames):
			self.run_particles_index = 0

		self.run_particle = self.run_particles_frames[int(self.run_particles_index)]
		self.run_particle = pygame.transform.flip(self.run_particle, self.flip, False)

	def create_run_particles(self):
		if self.flip:
			pos = self.rect.midright + pygame.math.Vector2(0, 14)
		else:
			pos = self.rect.midleft + pygame.math.Vector2(-5, 14)

		self.display_surface.blit(self.run_particle, pos)

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
			self.create_jump_particles(self.rect.midbottom)
			self.jump()

	def jump(self, jump_force=-19):
		self.direction.y = jump_force
		self.on_ground = False
		self.on_ceiling = False

	def move(self):
		self.rect.x += self.direction.x * self.speed

	def take_hit(self, *groups):
		if not self.hit:
			for group in groups:
				for sprite in group.sprites():
					if sprite.rect.colliderect(self.rect):
						self.frame_index = 0
						self.hit = True
						self.direction.x = 0
						if self.direction.y < 0 or (self.direction.y == 0 and not self.on_ground):
							self.jump(5)
							self.collideable = False

						elif self.direction.y > 0 or (self.direction.y == 0 and self.on_ground):
							self.jump(-15)
							self.collideable = False

	def update(self):
		# Particles
		if Global.level:
			self.create_jump_particles = Global.level.create_jump_particles
		
		if not self.hit:
			self.get_input()

		if self.state == "Run" and self.on_ground:
			self.run_particles_animate()
			self.create_run_particles()

		self.get_state()

		self.animate(0.4)