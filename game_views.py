import arcade
from arcade import gui
from meteors import Meteor
from laser import Laser
from ship import Ship
from dashboard import Dashboard
from explosion import Explosion
from explosion import createExplosionTextureList
from client import *
from globals import *
from typing import Optional, Dict, cast
from arcade.gui import UIElement,  MOUSE_PRESS, UIEvent
from arcade.gui.core import MOUSE_MOTION

class Gui(arcade.gui.UIManager):
	def __init__(self, window):
		"""
		Initializer
		"""
		# Open a window in full screen mode. Remove fullscreen=True if
		# you don't want to start this way.
		super().__init__(window)
		
	def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
		"""
		Dispatches :py:meth:`arcade.View.on_mouse_press()` as :py:class:`arcade.gui.UIElement`
		with type :py:attr:`arcade.gui.MOUSE_PRESS`
		"""
		#Get the ratio of the screen when it resizes to better track events on different screen sizes
		ratio_x = 1
		ratio_y = 1
		width, height = self.window.get_size()
		if(SCREEN_HEIGHT != height):
			ratio_y = height / SCREEN_HEIGHT
		if(SCREEN_WIDTH != width):
			ratio_x = width / SCREEN_WIDTH

		eventX = x / ratio_x
		eventY = y / ratio_y
		self.dispatch_ui_event(UIEvent(MOUSE_PRESS, x=eventX, y=eventY, button=button, modifiers=modifiers))

	def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
		"""
		Dispatches :py:meth:`arcade.View.on_mouse_motion()` as :py:class:`arcade.gui.UIElement`
		with type :py:attr:`arcade.gui.MOUSE_MOTION`
		"""
		#Get the ratio of the screen when it resizes to better track events on different screen sizes
		ratio_x = 1
		ratio_y = 1
		width, height = self.window.get_size()
		if(SCREEN_HEIGHT != height):
			ratio_y = height / SCREEN_HEIGHT
		if(SCREEN_WIDTH != width):
			ratio_x = width / SCREEN_WIDTH

		eventX = x / ratio_x
		eventY = y / ratio_y
		self.dispatch_ui_event(UIEvent(MOUSE_MOTION, x=eventX, y=eventY, dx=dx, dy=dy))

class MainWindow(arcade.Window):
	""" Main application class. """
	def __init__(self):
		"""
		Initializer
		"""
		# Open a window in full screen mode. Remove fullscreen=True if
		# you don't want to start this way.
		super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, fullscreen=False)

		# This will get the size of the window, and set the viewport to match.
		# So if the window is 1000x1000, then so will our viewport. If
		# you want something different, then use those coordinates instead.
		width, height = self.get_size()
		self.set_viewport(0, width, 0, height)

class MenuView(arcade.View):
	""" Class that manages the 'menu' view. """
	def __init__(self):
		super().__init__()
		self.background = arcade.load_texture("images/space.jpeg")

	def on_draw(self):
		""" Draw the menu """
		arcade.start_render()

		# Draw the background texture
		arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)

		arcade.draw_text("3", SCREEN_WIDTH/2, SCREEN_HEIGHT/2-100,
						 arcade.color.DARK_RED, font_size=200, anchor_x="center")
		arcade.draw_text("Math   Blaster", SCREEN_WIDTH/2+15, SCREEN_HEIGHT/2,
						 arcade.color.WHITE, font_size=60, anchor_x="center")
		arcade.draw_text("Click 'F1' for full screen or any key to advance", SCREEN_WIDTH/2, SCREEN_HEIGHT/2-120,
						 arcade.color.WHITE, font_size=20, anchor_x="center")
		

	def on_mouse_press(self, _x, _y, _button, _modifiers):
		""" Use a mouse press to advance to the 'game' view. """
		game_view = GameView() 
		self.window.show_view(game_view)

	def on_key_press(self, symbol, modifiers):
		if symbol == arcade.key.F1:
			# User hits s. Flip between full and not full screen.
			self.window.set_fullscreen(not self.window.fullscreen)
			# Instead of a one-to-one mapping, stretch/squash window to match the
			# constants. This does NOT respect aspect ratio. You'd need to
			# do a bit of math for that.
			self.window.set_viewport(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT)
		else:
			game_view = GameView() 
			self.window.show_view(game_view)
			return super().on_key_press(symbol, modifiers)

class GameView(arcade.View):
	def __init__(self):
		"""
		Sets up the initial conditions of the game
		:param width: Screen width
		:param height: Screen height
		"""
		super().__init__()
		self.background = arcade.load_texture("images/space1.png")
		self._keys = set()
		self.score = 0
		self.lives = PLAYER_LIVES

		self.delay = START_DELAY
		
		self.window.set_mouse_visible(False)
		#Objects
		self.dashboard = Dashboard()
		self.ship = Ship()

		# bullet Sprites
		self.bullets = SpriteList()
		# how many bullets you're allowed to make
		self.ammo = 5

		self.meteors = SpriteList()	
		self.animations = SpriteList()
		self.lifeList = SpriteList()

		#Explosion Frames
		self.explosion_texture_list =  createExplosionTextureList()
		self.animationsLoaded = False
		self.load_animantion_frames()
		
		# Load sounds. Sounds from kenney.nl
		self.gun_sound = arcade.sound.load_sound(":resources:sounds/laser2.wav")
		self.hit_sound = arcade.sound.load_sound(":resources:sounds/explosion2.wav")

		arcade.set_background_color(arcade.color.ARSENIC)

		#This is for the lives 
		start_x = 20
		x = 0
		start_y = SCREEN_HEIGHT - 125
		for life in range(self.lives):
			heart = Sprite('images/heart.png')
			heart.scale = 0.1
			x =  start_x + (life * (heart.width / 2) + 10)
			heart.center_x = x
			heart.center_y = start_y
			
			self.lifeList.append(heart)

	def on_draw(self):
		"""
		Called automatically by the arcade framework.
		Handles the responsiblity of drawing all elements.
		"""
		# clear the screen to begin drawing
		arcade.start_render()
		arcade.draw_lrwh_rectangle_textured(0,0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
		self.dashboard.draw()
		self.draw_score()
		self.bullets.draw()
		self.meteors.draw()
		#Check if the ship is still alive 
		if(self.ship.alive):
			self.ship.draw()

		#Render current animations
		self.animations.draw()

		#Verify if animations have been loaded else display a "get ready" message
		if(not self.animationsLoaded):
			self.draw_get_ready()

		#Draw the hearts on the screen 
		self.lifeList.draw()

	def draw_score(self):
		"""
		Puts the current score on the screen
		"""
		score_text = f"Score: {self.score}"
		start_x = 20
		start_y = SCREEN_HEIGHT - 100
		
		arcade.draw_rectangle_filled(self.dashboard.right//2,SCREEN_HEIGHT - 70,self.dashboard.right + 1,140,arcade.color.DARK_MIDNIGHT_BLUE)
		arcade.draw_text(score_text, start_x=start_x, start_y=start_y,
						 font_size=30, color=arcade.color.WHITE)

		text = f"Ammo: {self.ammo}"
		arcade.draw_text(text, start_x, SCREEN_HEIGHT - (SCREEN_HEIGHT//1.10), font_size=30, color=arcade.color.WHITE)
			
	def draw_get_ready(self):
		"""
		Writes a get ready message on the screen 
		"""
		arcade.draw_text("Get ready", ((SCREEN_WIDTH - DASHBOARD_WIDTH) /2 ) + DASHBOARD_WIDTH, SCREEN_HEIGHT/2,
						arcade.color.WHITE, font_size=30, anchor_x="center")

	def update(self, delta_time):
		"""
		Update each object in the game.
		:param delta_time: tells us how much time has actually elapsed
		"""

		# Check to see if keys are being held, and then
		# take appropriate action
		self.check_keys()
		self.check_off_screen()
		
		self.bullets.update()

		self.meteors.update()

		if(self.animationsLoaded):
			if randint(0,self.delay) == 1:
				self.create_meteor()

		self.ship.update()

		self.check_collisions()

		self.animations.update()

		#Check if animations have already been loaded
		if(not self.animationsLoaded):
			self.check_animations_loaded()

		#Check if the ship is still alive
		if(not self.ship.alive):
			#Check if there ship has  frames left 
			#This gives time for  the explosion of the ship to appear on the screen
			if(self.ship.framesAfterDead == 0):
				self.gameOver()
			else:
				self.ship.framesAfterDead = self.ship.framesAfterDead - 1		

	def check_collisions(self):
		for meteor in self.meteors:
			#Check if a meteor collided with a bullet
			if meteor.collides_with_list(self.bullets):
				meteor.alive = False
				# Instantiate an explosion
				self.create_explosion( meteor.center_x, meteor.center_y)
				arcade.sound.play_sound(self.hit_sound)
				self.score += 10

			#Create a temp list for the ship 
			ship = SpriteList()
			ship.append(self.ship)
			#Check if a meteor collided with the ship
			if meteor.collides_with_list(ship):
				meteor.alive = False
				self.ship.alive = False
				# Instantiate an explosion
				self.create_explosion( meteor.center_x, meteor.center_y)
				arcade.sound.play_sound(self.hit_sound)

			#Check if a meteor crossed the bottom screen
			elif meteor.bottom <= 10:
				self.create_explosion( meteor.center_x, meteor.center_y)
				arcade.sound.play_sound(self.hit_sound)
				self.lives -= 1
				self.lifeList.remove(self.lifeList[-1])
				meteor.alive = False
				if self.lives <= 0:
					self.gameOver()

		#Check if a bullet collided with a meteor
		for bullet in self.bullets:
			if bullet.collides_with_list(self.meteors):
				bullet.alive = False

		#Remove all dead sprites
		self.clean_up_zombies()

	def clean_up_zombies(self):
		for meteor in self.meteors:
			if not meteor.alive:
				self.meteors.remove(meteor)

		for bullet in self.bullets:
			if not bullet.alive:
				self.bullets.remove(bullet)
	
	def check_off_screen(self):
		""" 
		Removes sprites that have gone off screen
		"""
		for bullet in self.bullets:
			if bullet.bottom > SCREEN_HEIGHT + bullet.height:
				self.bullets.remove(bullet)
				
	def check_keys(self):
		"""
		Checks to see if the user is holding down an
		arrow key, and if so, takes appropriate action.
		"""
		if arcade.key.LEFT in self._keys:
			self.ship.move_left()
		elif arcade.key.RIGHT in self._keys:
			self.ship.move_right()

	def on_key_press(self, key, key_modifiers):
		"""
		Called when a key is pressed. Sets the state of
		holding an arrow key.
		:param key: The key that was pressed
		:param key_modifiers: Things like shift, ctrl, etc
		"""
		#Wait for animations to be loaded before accepting user input
		if (self.animationsLoaded):
			if key == arcade.key.LEFT:
				self._keys.add(key)

			if key == arcade.key.RIGHT:
				self._keys.add(key)

			if key == arcade.key.SPACE:
				self.create_bullet()

		
		if key == arcade.key.A or key == arcade.key.S or key == arcade.key.D or key == arcade.key.F:
			
			if self.dashboard.check_answer(key):

				self.reload()
				# !!!!!!!!!!!!!
				# TODO: Add display for right/wrong answer and its consequences
				# !!!!!!!!!!!!!
			else:
				self.lives -= 1
				self.lifeList.remove(self.lifeList[-1])
				if self.lives <= 0:
					self.gameOver()


				
			

		if key == arcade.key.F1:
			# User hits s. Flip between full and not full screen.
			self.window.set_fullscreen(not self.window.fullscreen)
			# Instead of a one-to-one mapping, stretch/squash window to match the
			# constants. This does NOT respect aspect ratio. You'd need to
			# do a bit of math for that.
			self.window.set_viewport(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT)

		if key == arcade.key.ESCAPE:			
			self.gameOver()

	def on_key_release(self, key, key_modifiers):
		"""
		Called when a key is released. Sets the state of
		the arrow key as being not held anymore.
		:param key: The key that was pressed
		:param key_modifiers: Things like shift, ctrl, etc
		"""
		#The game is waiting  for animations to be loaded before accepting user input
		if (self.animationsLoaded) and len(self._keys) > 0:
			if key == arcade.key.LEFT:
				self._keys.remove(key)

			if key == arcade.key.RIGHT:
				self._keys.remove(key)

	def create_bullet(self):
		"""
		Creates an instance of laser and appends it to the bullets sprite list
		"""
		if self.ammo > 0:
			laser = Laser(self.ship.center_x, self.ship.center_y)
			self.bullets.append(laser)
			arcade.sound.play_sound(self.gun_sound)
			self.ammo -=1

	def reload(self):
		self.ammo += 5
		
	def create_meteor(self):
		"""
		Creates an instance of Meteor and appends it to the meteors sprite list
		"""
		self.meteors.append(Meteor())

	def create_explosion(self, x, y):
		"""
		Creates an instance of Explosion and appends it to the animations sprite list
		"""
		new_explosion = Explosion(self.explosion_texture_list, x, y)
		# Call update() because it sets which image we start on
		new_explosion.update()
		self.animations.append(new_explosion)	

	def load_animantion_frames(self):
		"""
		Creates an instance of all possible animations so that they are loaded before the game starts 
		"""
		# Initialize  an explosion outside of the screen to load the explosion animation frames
		self.create_explosion(-50, -50)

	def check_animations_loaded(self):
		"""
		Sets the self.animationsLoaded variable to true if the animations list is empty
		"""
		if(len(self.animations) == 0):
			self.animationsLoaded = True
			
	def gameOver(self):
		"""
		Renders the GemeOverView and sends the score to the server
		"""
		self.window.show_view(GameOverView(self.score))

class GameOverView(arcade.View):
	""" Class that manages the 'game over' view. """
	def __init__(self,score=0):
		super().__init__()
		self.background = arcade.load_texture("images/space2.jpeg")
		self.window.set_mouse_visible(visible=True)
		self.score = score
		self.name = "Player"
		self.gui = Gui(self.window)
		
		#This is necesary to possition the input text box
		self.inputBox = arcade.gui.UIInputBox(SCREEN_WIDTH // 2 ,SCREEN_HEIGHT // 2 - 25,200,30)
		self.gui.add_ui_element(self.inputBox)

	def on_draw(self):
		""" Draw the menu """
		arcade.start_render()

		# Draw the background texture
		width, height = self.window.get_size()

		arcade.draw_lrwh_rectangle_textured(0, 0, width, height, self.background)
		arcade.draw_text(f"--GAME OVER--\n", SCREEN_WIDTH/2, SCREEN_HEIGHT/2+50,
						 arcade.color.ALABAMA_CRIMSON, font_size=60, anchor_x="center")

		arcade.draw_text(f"Player: {self.name}\nScore: {self.score}", SCREEN_WIDTH/2, SCREEN_HEIGHT/2+40,
						 arcade.color.WHITE, font_size=30, anchor_x="center")

		if self.inputBox in self.gui._ui_elements:
			arcade.draw_text(f" \nEnter Name:", SCREEN_WIDTH/2 , SCREEN_HEIGHT//3+85,
							arcade.color.WHITE, font_size=30, anchor_x="center")

			arcade.draw_text(f"Press Enter to submit name.", SCREEN_WIDTH/2, SCREEN_HEIGHT/3,
							arcade.color.WHITE, font_size=26, anchor_x="center")
						
		arcade.draw_text(f"Press Esc to quit, F2 to restart.", SCREEN_WIDTH/2, SCREEN_HEIGHT/4,
						 arcade.color.WHITE, font_size=26, anchor_x="center")           

	def on_key_press(self, key, modifiers):
		# Quit game with ESCAPE
		if key == arcade.key.ESCAPE:
			self.get_name()
			#Send score to server
			self.send_score()
			arcade.close_window()
		
		# Submit Name with ENTER
		if key == arcade.key.ENTER:
			self.name = self.inputBox.text          
			self.gui._ui_elements.remove(self.inputBox)

		# Restart with F2
		if key == arcade.key.F2:
			self.get_name()
			try:
				self.gui._ui_elements.remove(self.inputBox)
			except:
				print("something happened")
			self.window.show_view(GameView())
			self.send_score()
		# Change screen size
		if key == arcade.key.F1:
			# User hits s. Flip between full and not full screen.
			self.window.set_fullscreen(not self.window.fullscreen)
			# Instead of a one-to-one mapping, stretch/squash window to match the
			# constants. This does NOT respect aspect ratio. You'd need to
			# do a bit of math for that.
			self.window.set_viewport(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT)

	def get_name(self):
		if self.inputBox.text != "":
			self.name = self.inputBox.text

	def send_score(self):
		if self.score > 0 and self.name != '' and ':' not in self.name:
			send(f"{self.name}:{self.score}")

def initializeGame():
	window = MainWindow()
	window.show_view(MenuView())


