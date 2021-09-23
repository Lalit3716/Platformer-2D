import pygame, sys
from settings import *
from level import Level
from global_ import Global
from UI import home_screen, choose_player, game_over, pause_menu, level_menu, end_scene
from utils import Button

# Initialize Pygame
pygame.init()

class Game:
	def __init__(self):
		# Screens
		self.opening_screen = home_screen.Screen(screen)
		self.choose_player_screen = choose_player.Screen(screen)
		self.game_over_screen = game_over.Screen(screen)
		self.pause_screen = pause_menu.Pause_Screen(screen)
		self.level_select_screen = level_menu.Screen(screen)
		self.end_screen = end_scene.Screen(screen)
		
	def run(self):
		if Global.level:
			self.level = Global.level
		state = Global.state
		
		if state == "playing": self.level.run()
		elif state == "opening_scene": self.opening_screen.run()
		elif state == "level_select": self.level_select_screen.run()
		elif state == "choose_player": self.choose_player_screen.run()
		elif state == "game_over": self.game_over_screen.run()	
		elif state == "pause": self.pause_screen.run()
		elif state == "game_ended": self.end_screen.run()

# Create Display Surface + Clock Object
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Platformer-2D")
clock = pygame.time.Clock()
FPS = 60

# Initiate Game
game = Game()

# Main Loop
while True:
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

	game.run()
	

	clock.tick(FPS)
	pygame.display.update()