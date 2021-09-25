import pygame, random
from settings import *
from utils import Button
from Particles import ParticleEffect
from terrain import TerrainTile, LimitTile
from player import Player
from portals import Portal
from items import Fruit, FallingTrap, SawTrap, Spikes
from hud import Hud
from global_ import Global

# Caution! Very Long Class!
class Level(pygame.sprite.Sprite):
	def __init__(self, level):
		super().__init__()
		self.key_pressed = True

		# World Variables
		self.display_surface = pygame.display.get_surface()
		background_color = levels[level]["color"]
		self.background = pygame.image.load(f"../assets/Background/{background_color}.png").convert_alpha()
		self.background = pygame.transform.scale(self.background, (screen_width, screen_height))
		self.background2 = self.background.copy()
		self.bg_y = 0
		self.world_shift_x = 0
		self.world_shift_y = 0
		self.world_stop = False
		self.level_just_started = True
		self.level_ended = False
		self.scrolled_distance = 0

		# Terrain
		self.layout = levels[level]["level_data"]
		self.tiles = pygame.sprite.Group()
		
		# Portals
		self.appearing_portal = pygame.sprite.GroupSingle()
		self.disappearing_portal = pygame.sprite.GroupSingle()

		# Player
		self.player = pygame.sprite.GroupSingle()
		self.died = False
		self.player_was_on_ground = False

		# Particles
		self.particles = pygame.sprite.GroupSingle()

		# Fruits
		self.fruits = pygame.sprite.Group()

		# Traps
		self.saw_traps = pygame.sprite.Group()
		self.falling_traps = pygame.sprite.Group()
		self.spikes = pygame.sprite.Group()

		# Platforms Limits
		self.platform_limits = pygame.sprite.Group()

		# World_Limits
		self.world_limit_left = pygame.sprite.GroupSingle()
		self.world_limit_right = pygame.sprite.GroupSingle()

		# Create Whole Level At Once
		self.create()

		# Pause Button
		pause_btn_image = pygame.image.load("../assets/Menu/Buttons/Pause.png").convert_alpha()
		pause_btn_image = pygame.transform.scale2x(pause_btn_image)
		self.pause_btn = Button(self.display_surface, (screen_width - 50, 50), image=pause_btn_image)

		# Controls Button
		controls_btn_image = pygame.image.load("../assets/Menu/Buttons/Controls.png").convert_alpha()
		controls_btn_image = pygame.transform.scale2x(controls_btn_image)
		self.controls_btn = Button(self.display_surface, (screen_width - 100, 50), image=controls_btn_image)

		# Hud
		Global.score = 0
		self.hud = Hud()

	def on_pause_btn_clk(self):
		self.key_pressed = True
		if Global.history[-1] != "playing":
			Global.history.append(Global.state)
		Global.state = "pause"

	def on_controls_btn_clk(self):
		self.key_pressed = True
		if Global.history[-1] != "playing":
			Global.history.append(Global.state)
		Global.state = "controls"

	# Particles
	def create_jump_particles(self, pos):
		offset = pygame.math.Vector2(0, -10)
		jump_particles = ParticleEffect(pos+offset, "jump")
		self.particles.add(jump_particles)

	def create_land_particles(self):
		if not self.player_was_on_ground and self.player.sprite.on_ground and not self.particles.sprites():
			pos = self.player.sprite.rect.midbottom + pygame.math.Vector2(0, -20)
			land_particles = ParticleEffect(pos, "land")
			self.particles.add(land_particles)

	def create(self):
		for type, data in self.layout.items():
			for row_index, row in enumerate(data): 
				for col_index, cell in enumerate(row):
					x = col_index * tile_size
					y = row_index * tile_size
					if type == "terrain":
						if cell != "-1": 
							self.tiles.add(TerrainTile((x, y), tile=cell))
					
					if type == "player":
						if cell == "1":
							self.player_x = x
							self.player_y = y
							self.starting_player_x = x
							self.starting_player_y = y
							self.appearing_portal.add(Portal((x, y), "appearing"))
						elif cell == "2":
							self.disappearing_portal.add(Portal((x, y), "disappearing"))
				
					if type == "fruit":
						if cell == "1":
							self.fruits.add(Fruit((x, y), "Apple"))
						elif cell == "2":
							self.fruits.add(Fruit((x, y), "Bananas"))
						elif cell == "3":
							self.fruits.add(Fruit((x, y), "Cherries"))		
						elif cell == "4":
							self.fruits.add(Fruit((x, y), "Strawberry"))
						elif cell == "6":
							self.fruits.add(Fruit((x, y), "Pineapple"))
				
					if type == "trap":
						if cell == "0":
							self.falling_traps.add(FallingTrap((x, y)))
						elif cell == "3":
							self.saw_traps.add(SawTrap((x, y)))
						elif cell == "5":
							self.spikes.add(Spikes((x, y)))

					if type == "limit":
						if cell == "0":
							self.world_limit_left.add(LimitTile((x, y), type="world_limit_left"))
						elif cell == "1":
							self.world_limit_right.add(LimitTile((x, y), type="world_limit_right"))
						elif cell == "2":
							self.platform_limits.add(LimitTile((x, y), type="topleft"))
						elif cell == "3":
							self.platform_limits.add(LimitTile((x, y), type="bottomleft"))
						elif cell == "4":
							self.platform_limits.add(LimitTile((x, y), type="bottomright"))
						elif cell == "5":
							self.platform_limits.add(LimitTile((x, y), type="topright"))
	
	def check_player_on_ground(self):
		if self.player.sprite.on_ground:
			self.player_was_on_ground = True
		else:
			self.player_was_on_ground = False

	def horizontal_collisions(self):
		player = self.player.sprite
		player.move()
		if self.player.sprite.collideable:
			for tile in self.tiles.sprites() + self.falling_traps.sprites():
				if tile.rect.colliderect(player.rect):
					if player.direction.x > 0:
						player.rect.right = tile.rect.left
					elif player.direction.x < 0:
						player.rect.left = tile.rect.right

	def vertical_collisions(self):
		player = self.player.sprite
		player.apply_gravity()
		if self.player.sprite.collideable:
			for tile in self.tiles.sprites() + self.falling_traps.sprites():
				if tile.rect.colliderect(player.rect):
					if player.direction.y > 0: 
						player.rect.bottom = tile.rect.top
						player.direction.y = 0
						player.on_ground = True
						if tile in self.falling_traps.sprites():
							tile.fall()

					elif player.direction.y < 0:
						player.rect.top = tile.rect.bottom
						player.direction.y = 0
						player.on_ceiling = True
										
	def scroll_x(self):
		player = self.player.sprite
		world_limit_left = self.world_limit_left.sprite
		world_limit_right = self.world_limit_right.sprite	
		if world_limit_left.rect.x >= player.rect.x or world_limit_right.rect.x <= player.rect.x:
			self.world_stop = True
		else:
			self.world_stop = False

		if (player.rect.right > (screen_width - (screen_width / 5)) and player.direction.x > 0) and not self.world_stop:
			player.speed = 0
			self.world_shift_x = -5
			
		elif (player.rect.x < (screen_width / 5) and player.direction.x < 0) and not self.world_stop:
			player.speed = 0
			self.world_shift_x = 5
			
		else:
			self.world_shift_x = 0
			player.speed = 5

		self.scrolled_distance += self.world_shift_x

	def scroll_back(self):
		speed = 15
		if self.scrolled_distance > 0:
			self.scrolled_distance -= speed
			if self.scrolled_distance <= 0:
				self.died = False
				self.appearing_portal.add(Portal((self.starting_player_x, self.starting_player_y), "appearing"))
				self.appearing_portal.sprite.hide()
				self.world_shift_x = 0
			else:
				self.world_shift_x = -speed

		else:
			self.scrolled_distance += speed
			if self.scrolled_distance >= 0:
				self.died = False
				self.appearing_portal.add(Portal((self.starting_player_x, self.starting_player_y), "appearing"))
				self.appearing_portal.sprite.hide()
				self.world_shift_x = 0
			else:
				self.world_shift_x = speed

	def scroll_background(self, speed):
		self.display_surface.blit(self.background, (0, self.bg_y))
		self.display_surface.blit(self.background2, (0, self.bg_y-screen_height))
		self.bg_y += speed
		if self.bg_y >= screen_height:
			self.bg_y = 0

	def set_player(self, character):
		self.character = character
		self.player.add(Player((self.player_x, self.player_y), scale=(50, 50), player=character))

	def collect_fruits(self):
		if self.player.sprite.collideable:
			for fruit in self.fruits.sprites():
				if fruit.rect.colliderect(self.player.sprite.rect):
					fruit.kill()
					Global.score += 1
					if Global.score % 50 == 0:
						Global.lives += 1

	def check_game_over(self):
		player = self.player.sprite
		if player.rect.y > screen_height:
			Global.lives -= 1
			
			if Global.lives == 0:
				Global.state = "game_over"
			
			else:
				self.died = True
				self.smooth_reset()

	def destroy_level(self):
		for sprite in self.tiles.sprites() + self.fruits.sprites() + self.falling_traps.sprites() + self.saw_traps.sprites():
			sprite.kill()
		self.spikes.empty()
		self.platform_limits.empty()
		self.world_limit_left.sprite.kill()
		self.world_limit_right.sprite.kill()
		self.appearing_portal.empty()
		self.disappearing_portal.empty()

	def smooth_reset(self):
		self.player.sprite.kill()
		x, y = self.starting_player_x, self.starting_player_y
		self.player.add(Player((x, y), scale=(50, 50), player=self.character))
		self.level_just_started = True

	def reset(self):
		Global.score = 0
		Global.lives = 3
		self.player.sprite.kill()
		self.destroy_level()
		self.create()
		self.level_just_started = True
		self.scrolled_distance = 0
		self.player.add(Player((self.player_x, self.player_y), scale=(50, 50), player=self.character))

	# Get Game States
	def input(self):
		keys = pygame.key.get_pressed()

		if keys[pygame.K_ESCAPE] and not self.key_pressed:
			self.key_pressed = True
			self.pause_btn.press()

		elif not any(keys) and self.key_pressed:
			self.key_pressed = False
			
	def win(self):
		portal = self.disappearing_portal.sprite
		if portal.rect.colliderect(self.player.sprite.rect):
			self.level_ended = True
			self.player.sprite.direction.x = 0
			portal.animate(0.2)
			if portal.allowed:
				next_level = Global.current_level + 1
				if next_level <= Global.max_level:
					levels[next_level]["status"] = "unlocked"
					Global.level_menu.create_levels_buttons()
					Global.level = Level(next_level)
					Global.level.set_player(self.character)
					Global.current_level = next_level
					self.kill()
				else:
					Global.state = "game_ended"
					self.kill()
			
	# Draw/Update all the stuff here ==>
	def run(self):
		# Background
		self.scroll_background(1.5)

		# Check states
		self.input()
		self.check_game_over()

		# Particles
		self.particles.update(self.world_shift_x)
		self.particles.draw(self.display_surface)

		# Traps
		self.saw_traps.update(self.world_shift_x, self.world_shift_y, self.platform_limits)
		self.saw_traps.draw(self.display_surface)
		self.falling_traps.update(self.world_shift_x, self.world_shift_y)
		self.falling_traps.draw(self.display_surface)
		self.spikes.update(self.world_shift_x)
		self.spikes.draw(self.display_surface)

		# Terrain
		self.tiles.update(self.world_shift_x, self.world_shift_y, self.display_surface)
		self.tiles.draw(self.display_surface)
		if not self.died:
			self.scroll_x()
		elif self.died:
			self.scroll_back()

		# Fruits
		self.fruits.update(self.world_shift_x, self.world_shift_y)
		self.fruits.draw(self.display_surface)
		self.collect_fruits()

		# Portals
		self.appearing_portal.update(self.world_shift_x, self.world_shift_y)
		self.disappearing_portal.update(self.world_shift_x, self.world_shift_y)
		self.appearing_portal.draw(self.display_surface)
		self.disappearing_portal.draw(self.display_surface)

		# Collisions
		if not self.died and not (self.level_just_started or self.level_ended):
			self.horizontal_collisions()
			self.check_player_on_ground()
			self.vertical_collisions()
			self.create_land_particles()

		# Player
		if not (self.level_just_started or self.level_ended):
			self.player.update()
			self.player.sprite.take_hit(self.saw_traps, self.spikes)
			self.player.draw(self.display_surface)

		# Update Player Position
		self.player_x = self.player.sprite.rect.centerx
		self.player_y = self.player.sprite.rect.centery	

		# Limits
		self.world_limit_left.update(self.world_shift_x, self.world_shift_y)
		self.world_limit_right.update(self.world_shift_x, self.world_shift_y)
		self.platform_limits.update(self.world_shift_x, self.world_shift_y)

		# Pause Button
		self.pause_btn.active(self.on_pause_btn_clk)

		# Controls Button
		self.controls_btn.active(self.on_controls_btn_clk)

		# Win
		self.win()

		# Hud
		self.hud.draw()