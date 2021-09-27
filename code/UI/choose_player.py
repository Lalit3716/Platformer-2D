import pygame
from settings import screen_width, screen_height
from player import Player
from utils import Button
from global_ import Global

class CharacterCard(pygame.sprite.Sprite):
	def __init__(self, size, pos, character):
		super().__init__()

		# Font
		font = pygame.font.Font("../assets/Menu/Font/3.otf", 20)
		self.font = font.render(character, False, (0, 0, 0))

		# Card
		self.image = pygame.Surface(size, flags = pygame.SRCALPHA)
		self.rect = self.image.get_rect(center = pos)
		self.color = "grey"
		self.clicked = False
	
		# Player
		self.character = character
		self.player = pygame.sprite.GroupSingle()
		self.add_player()

	def add_player(self):
		# Font
		self.font_pos = self.font.get_rect(center=self.rect.center + pygame.math.Vector2(0, 100))

		# Player
		pos = self.rect.center
		player = Player(pos, scale=(100, 100), player=self.character)
		self.player.add(player)

	def check_hover(self):
		if self.rect.collidepoint(pygame.mouse.get_pos()):
			if not self.clicked:
				self.color = "pink"
				self.player.sprite.state = "Run"
			elif self.clicked:
				self.color = "green"
				self.player.sprite.state = "Idle"
			self.player.sprite.animate(0.3)
		
		else:
			if not self.clicked:
				self.color = "grey"
			elif self.clicked:
				self.color = "green"

			self.player.sprite.state = "Idle"
			self.player.sprite.animate(0.3)

	def update(self, surface):
		# Card
		pygame.draw.rect(surface, self.color, self.rect, border_radius=20)
		pygame.draw.rect(surface, "black", self.rect, border_radius=20, width=2)
		self.check_hover()

		# Player
		self.player.draw(surface)

		# Font
		surface.blit(self.font, self.font_pos)

class Screen:
	def __init__(self, display_surface):
		self.key_pressed = True
		self.clicked = False

		# sfx
		self.click_sound = pygame.mixer.Sound("../assets/Audio/Interface/click_003.ogg")
		self.back_sound = pygame.mixer.Sound("../assets/Audio/Interface/tick_002.ogg")
		self.drop_sound = pygame.mixer.Sound("../assets/Audio/Interface/drop_003.ogg")

		# Font
		font = pygame.font.Font("../assets/Menu/Font/3.otf", 50)
		self.font = font.render("Select Your Character", True, (0, 0, 0))
		self.font_pos = self.font.get_rect(center=(screen_width/2, 100))

		# Dislay
		self.display_surface = display_surface
		self.background = pygame.image.load("../assets/Background/Blue.png").convert_alpha()
		self.background = pygame.transform.scale(self.background, (screen_width, screen_height))

		# Characters
		self.characters = pygame.sprite.Group()
		self.add_characters()
		self.current_index = -1		# For keyboard inputs
		self.selected_player = ""

		# Play Button
		btn_config = {
			"size": (250, 60),
			"color": (61, 178, 255),
			"border_radius": 20,
			"text": "Play",
			"text_size": 50,
			"text_color": (0, 0, 0),
			"outline": 1,
			"hover": (0, 255, 0)
		}
		self.play_btn = Button(self.display_surface, (screen_width/2, screen_height/2 + 200), btn_config)

		# Back Button
		back_btn_image = pygame.transform.scale2x(pygame.image.load("../assets/Menu/Buttons/Back.png").convert_alpha())
		self.back_btn = Button(self.display_surface, (100, 150), image=back_btn_image)

	def add_characters(self):
		x = screen_width/2
		y = screen_height/2
		self.characters.add(CharacterCard((200, 300), (x-350, y), "Mask Dude"))
		self.characters.add(CharacterCard((200, 300), (x-115, y), "Pink Man"))
		self.characters.add(CharacterCard((200, 300), (x+115, y), "Virtual Guy"))
		self.characters.add(CharacterCard((200, 300), (x+350, y), "Ninja Frog"))

	def check_clicks(self):
		left_click = pygame.mouse.get_pressed()[0]
		if left_click and not self.clicked:
			self.clicked = True

			for index, character in enumerate(self.characters.sprites()):
				if character.rect.collidepoint(pygame.mouse.get_pos()):
					self.click_sound.play()
					self.current_index = index
					character.clicked = True
					self.selected_player = character.character
				else:
					character.clicked = False

		elif not left_click and self.clicked:
			self.clicked = False

	def on_play_btn_click(self):
		self.click_sound.play()
		self.key_pressed = True
		if self.selected_player == "":
			self.selected_player = "Virtual Guy"
		Global.level.set_player(self.selected_player)
		Global.history.append(Global.state)
		Global.state = "playing"

	def on_back_btn_clk(self):
		self.back_sound.play()
		self.key_pressed = True
		Global.state = Global.history[-1]
		Global.history.pop()

	def input(self):
		keys = pygame.key.get_pressed()

		if keys[pygame.K_ESCAPE] and not self.key_pressed:
			self.key_pressed = True
			self.back_btn.press()

		elif keys[pygame.K_RETURN] and not self.key_pressed:
			self.key_pressed = True
			self.play_btn.press()

		elif keys[pygame.K_RIGHT] and not self.key_pressed:
			self.drop_sound.play()
			self.key_pressed = True
			characters = self.characters.sprites()
			
			if self.current_index < len(characters) - 1:
				self.current_index += 1
			else:
				self.current_index = 0

			for i in range(len(characters)):
				if i == self.current_index:
					characters[i].clicked = True
				else:
					characters[i].clicked = False

			self.selected_player = characters[self.current_index].character

		elif keys[pygame.K_LEFT] and not self.key_pressed:
			self.drop_sound.play()
			self.key_pressed = True
			characters = self.characters.sprites()
			
			if self.current_index > 0:
				self.current_index -= 1
			else:
				self.current_index = len(characters) - 1
			
			for i in range(len(characters)):
				if i == self.current_index:
					characters[i].clicked = True
				else:
					characters[i].clicked = False

			self.selected_player = characters[self.current_index].character

		elif not any(keys) and self.key_pressed:
			self.key_pressed = False

	def run(self):
		# Background
		self.display_surface.blit(self.background, (0, 0))

		# Heading
		self.display_surface.blit(self.font, self.font_pos)

		# Add Cards
		self.characters.draw(self.display_surface)
		self.characters.update(self.display_surface)
		self.check_clicks()

		# Keyboard Input
		self.input()

		# Play Button
		self.play_btn.active(self.on_play_btn_click)
		
		if not any([character.clicked for character in self.characters.sprites()]):
			self.play_btn.grey_out()
		else:
			self.play_btn.normal()

		# Back Button
		self.back_btn.active(self.on_back_btn_clk)