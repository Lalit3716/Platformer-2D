import pygame
from .game_over import Screen
from utils import Button
from settings import screen_width, screen_height
from global_ import Global

class Pause_Screen(Screen):
	def __init__(self, screen):
		super().__init__(screen)

		# Pause Font
		self.font_surface = self.font.render("Pause Menu", True, (0, 0, 0))

		self.restart_btn_pos = (screen_width//2, 300)
		self.restart_btn = Button(self.display_surface, self.restart_btn_pos, self.restart_btn_config)

		# Resume Button
		self.resume_btn_pos = self.restart_btn_pos + pygame.math.Vector2(0, -100)
		self.resume_btn_congif = {
			**self.restart_btn_config,
			"text": "Resume",
		}
		self.resume_btn = Button(self.display_surface, self.resume_btn_pos, self.resume_btn_congif)

		# Levels Button
		self.levels_btn_pos = self.restart_btn_pos + pygame.math.Vector2(0, +200)
		self.levels_btn_congif = {
			**self.restart_btn_config,
			"text": "Levels",
		}
		self.levels_btn = Button(self.display_surface, self.levels_btn_pos, self.levels_btn_congif)

		# Change Player Button
		self.change_btn_pos = self.restart_btn_pos + pygame.math.Vector2(0, +100)
		self.change_btn_congif = {
			**self.restart_btn_config,
			"text_size": 40,
			"text": "Change Player",
		}
		self.change_btn = Button(self.display_surface, self.change_btn_pos, self.change_btn_congif)

		# Quit Button
		self.quit_btn_pos = self.restart_btn_pos + pygame.math.Vector2(0, +300)
		self.quit_btn_congif = {
			**self.restart_btn_config,
			"text_size": 50,
			"text": "Quit",
		}
		self.quit_btn = Button(self.display_surface, self.quit_btn_pos, self.quit_btn_congif)

		# Back Button
		back_btn_image = pygame.transform.scale2x(pygame.image.load("../assets/Menu/Buttons/Back.png").convert_alpha())
		self.back_btn = Button(self.display_surface, (250, 100), image=back_btn_image)

	def on_resume_btn_clk(self):
		Global.state = "playing"

	def on_change_btn_clk(self):
		Global.history.append(Global.state)
		Global.state = "choose_player"

	def on_quit_btn_click(self):
		Global.state = "opening_scene"
		Global.level.reset()

	def on_levels_btn_clk(self):
		Global.history.append(Global.state)
		Global.state = "level_select"

	def on_back_btn_clk(self):
		Global.state = Global.history[-1]
		Global.history.pop()
		
	def run(self):
		super().run()

		# Resume Button
		self.resume_btn.active(self.on_resume_btn_clk)

		# Levels Button
		self.levels_btn.active(self.on_levels_btn_clk)

		# Change Player Button
		self.change_btn.active(self.on_change_btn_clk)

		# Quit Button
		self.quit_btn.active(self.on_quit_btn_click)

		# Back Button
		self.back_btn.active(self.on_back_btn_clk)