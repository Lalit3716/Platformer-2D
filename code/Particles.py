import pygame
from utils import import_folder

class ParticleEffect(pygame.sprite.Sprite):
	def __init__(self, pos, type):
		super().__init__()
		if type == "jump":
			self.frames = import_folder("../assets/Main Characters/dust_particles/jump")
		elif type == "land":
			self.frames = import_folder("../assets/Main Characters/dust_particles/land")

		self.index = 0
		self.image = self.frames[self.index]
		self.rect = self.image.get_rect(center=pos)

	def animate(self, speed=0.4):
		self.index += speed
		
		if self.index >= len(self.frames):
			self.kill()
		else:
			self.image = self.frames[int(self.index)]

	def update(self, world_shift_x):
		self.rect.x += world_shift_x
		self.animate(0.2)