import pygame
from utils import Button
from settings import screen_width, screen_height
from global_ import Global

class Pause_Screen:
	def __init__(self, screen):
		self.key_pressed = True

		# Basic Setup
		self.display_surface = screen
		self.background = pygame.image.load("../assets/Background/Blue.png").convert_alpha()
		self.background = pygame.transform.scale(self.background, (screen_width, screen_height))

		# Pause Font
		self.font = pygame.font.Font("../assets/Menu/Font/3.otf", 50)
		self.font_surface = self.font.render("Pause Menu", True, (0, 0, 0))
		self.font_pos = self.font_surface.get_rect(center=(screen_width/2, 100))

		# Restart Button
		self.restart_btn_config = {
			"size": (250, 60),
			"color": (61, 178, 255),
			"border_radius": 20,
			"text": "Restart",
			"text_size": 50,
			"text_color": (0, 0, 0),
			"outline": 1,
			"hover": (0, 255, 0)
		}
		self.restart_btn_pos = (screen_width//2, 300)
		self.restart_btn = Button(self.display_surface, self.restart_btn_pos, self.restart_btn_config)

		# Resume Button
		self.resume_btn_congif = {
			**self.restart_btn_config,
			"text": "Resume",
		}
		self.resume_btn_pos = self.restart_btn_pos + pygame.math.Vector2(0, -100)
		self.resume_btn = Button(self.display_surface, self.resume_btn_pos, self.resume_btn_congif)

		# Levels Button
		self.levels_btn_congif = {
			**self.restart_btn_config,
			"text": "Levels",
		}
		self.levels_btn_pos = self.restart_btn_pos + pygame.math.Vector2(0, +200)
		self.levels_btn = Button(self.display_surface, self.levels_btn_pos, self.levels_btn_congif)

		# Change Player Button
		self.change_btn_congif = {
			**self.restart_btn_config,
			"text_size": 40,
			"text": "Change Player",
		}
		self.change_btn_pos = self.restart_btn_pos + pygame.math.Vector2(0, +100)
		self.change_btn = Button(self.display_surface, self.change_btn_pos, self.change_btn_congif)

		# Quit Button
		self.quit_btn_congif = {
			**self.restart_btn_config,
			"text_size": 50,
			"text": "Quit",
		}
		self.quit_btn_pos = self.restart_btn_pos + pygame.math.Vector2(0, +300)
		self.quit_btn = Button(self.display_surface, self.quit_btn_pos, self.quit_btn_congif)

		# Back Button
		back_btn_image = pygame.transform.scale2x(pygame.image.load("../assets/Menu/Buttons/Back.png").convert_alpha())
		self.back_btn = Button(self.display_surface, (250, 100), image=back_btn_image)

		# Buttons List
		self.btns = [self.resume_btn, self.restart_btn, self.change_btn, self.levels_btn, self.quit_btn]
		self.current_index = -1
		self.btn_selected = None

	def on_resume_btn_clk(self):
		self.key_pressed = True
		Global.state = "playing"

	def on_restart_btn_click(self):
		self.key_pressed = True
		Global.state = "playing"
		Global.level.reset()

	def on_change_btn_clk(self):
		self.key_pressed = True
		Global.history.append(Global.state)
		Global.state = "choose_player"

	def on_quit_btn_click(self):
		self.key_pressed = True
		Global.state = "opening_scene"
		Global.level.reset()
		Global.history.clear()

	def on_levels_btn_clk(self):
		self.key_pressed = True
		Global.history.append(Global.state)
		Global.state = "level_select"

	def on_back_btn_clk(self):
		self.key_pressed = True
		Global.state = Global.history[-1]
		Global.history.pop()
		
	def input(self):
		keys = pygame.key.get_pressed()
		
		if keys[pygame.K_DOWN] and not self.key_pressed:
			self.key_pressed = True
	
			if self.current_index < len(self.btns)-1:
				self.current_index += 1
			else:
				self.current_index = 0
	
			self.btns[self.current_index].focus()
			self.btns[self.current_index - 1].unfocus()
			self.btn_selected = self.btns[self.current_index]

		if keys[pygame.K_UP] and not self.key_pressed:
			self.key_pressed = True
	
			if self.current_index > 0:
				self.current_index -= 1
			else:
				self.current_index = len(self.btns) - 1
	
			self.btns[self.current_index].focus()
	
			if self.current_index + 1 > len(self.btns) - 1:
				self.btns[0].unfocus()
			else:
				self.btns[self.current_index+1].unfocus()
	
			self.btn_selected = self.btns[self.current_index]

		if keys[pygame.K_ESCAPE] and not self.key_pressed:
			self.key_pressed = True
			self.back_btn.press()
			
		if keys[pygame.K_RETURN] and not self.key_pressed:
			self.key_pressed = True
			if self.btn_selected:
				self.btn_selected.press()

		if not any(keys) and self.key_pressed:
			self.key_pressed = False

	def run(self):
		# Background
		self.display_surface.blit(self.background, (0, 0))	

		# Title
		self.display_surface.blit(self.font_surface, self.font_pos)
		
		# Handle KeyBoard Inputs
		self.input()

		# Resume Button
		self.resume_btn.active(self.on_resume_btn_clk)

		# Restart Button
		self.restart_btn.active(self.on_restart_btn_click)

		# Levels Button
		self.levels_btn.active(self.on_levels_btn_clk)

		# Change Player Button
		self.change_btn.active(self.on_change_btn_clk)

		# Quit Button
		self.quit_btn.active(self.on_quit_btn_click)

		# Back Button
		self.back_btn.active(self.on_back_btn_clk)