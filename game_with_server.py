from globals import *
from meteors import Meteor
from ship import Ship
from laser import Laser
from explosion import Explosion
from reload_box import ReloadBox
from explosion import createExplosionTextureList



class MenuView(arcade.View):
	""" Class that manages the 'menu' view. """

	def on_show(self):
		""" Called when switching to this view"""
		#self.background = arcade.load_texture("images/starnight.jpeg")
		arcade.set_background_color(arcade.color.BLACK)

	def on_draw(self):
		""" Draw the menu """
		arcade.start_render()
		arcade.draw_text("3", SCREEN_WIDTH/2, SCREEN_HEIGHT/2-100,
						 arcade.color.DARK_RED, font_size=200, anchor_x="center")
		arcade.draw_text("Math   Blaster", SCREEN_WIDTH/2+15, SCREEN_HEIGHT/2,
						 arcade.color.WHITE, font_size=60, anchor_x="center")
		arcade.draw_text("Click or Press any key to advance", SCREEN_WIDTH/2, SCREEN_HEIGHT/2-120,
                         arcade.color.WHITE, font_size=20, anchor_x="center")

	def on_mouse_press(self, _x, _y, _button, _modifiers):
		""" Use a mouse press to advance to the 'game' view. """
		game_view = GameView() 
		self.window.show_view(game_view)

	def on_key_press(self, symbol, modifiers):
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

		self._keys = set()

		self.score = 0

		self.reload_box = ReloadBox()

		#Objects
		self.ship = Ship()

		self.window.set_mouse_visible(False)

		self.bullets = SpriteList()

		self.meteors = SpriteList()	

		self.animations = SpriteList()

		#Explosion Frames
		self.explosion_texture_list =  createExplosionTextureList()
		self.animationsLoaded = False
		self.load_animantion_frames()
		

		# Load sounds. Sounds from kenney.nl
		self.gun_sound = arcade.sound.load_sound(":resources:sounds/laser2.wav")
		self.hit_sound = arcade.sound.load_sound(":resources:sounds/explosion2.wav")

		arcade.set_background_color(arcade.color.ARSENIC)

	def on_draw(self):
		"""
		Called automatically by the arcade framework.
		Handles the responsiblity of drawing all elements.
		"""

		# clear the screen to begin drawing
		arcade.start_render()
		self.reload_box.draw()
		self.draw_score()
		
		for bullet in self.bullets:
			bullet.draw()

		for meteor in self.meteors:
			meteor.draw()

		if(self.ship.alive):
			self.ship.draw()
		
		self.animations.draw()

		

		#Verify if animations have been loaded
		if(not self.animationsLoaded):
			self.draw_get_ready()

	def draw_score(self):
		"""
		Puts the current score on the screen
		"""
		
		score_text = "Score: {}".format(self.score)
		start_x = 10
		start_y = SCREEN_HEIGHT - 20
		
		arcade.draw_rectangle_filled(50, start_y + 5,90,20,(0,0,0,150))
		arcade.draw_text(score_text, start_x=start_x, start_y=start_y,
						 font_size=12, color=arcade.color.WHITE)
			
	def draw_get_ready(self):
		"""
		Writes a get ready message on the screen 
		"""
		arcade.draw_text("Get ready", SCREEN_WIDTH/2, SCREEN_HEIGHT/2,
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
		
		for bullet in self.bullets:
			bullet.update()

		for meteor in self.meteors:
			meteor.update()

		if(self.animationsLoaded):
			if randint(0,50) == 1:
				self.create_meteor()

		if ((self.ship.center_x > SCREEN_WIDTH and self.ship.change_x > 0) or \
			(self.ship.center_x < 0 and self.ship.change_x < 0)):
			self.ship.change_x = 0

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
			elif meteor.bottom <= 0:
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
		if arcade.key.LEFT in self._keys or arcade.key.RIGHT in self._keys:
			self.ship.update()

	def on_key_press(self, key, key_modifiers):
		"""
		Called when a key is pressed. Sets the state of
		holding an arrow key.
		:param key: The key that was pressed
		:param key_modifiers: Things like shift, ctrl, etc
		"""
		#Wait for animations to be loaded before accepting user input
		if (self.animationsLoaded):
			if key == arcade.key.LEFT or key == arcade.key.DOWN:
				self.ship.move_left()
				self._keys.add(key)

			if key == arcade.key.RIGHT or key == arcade.key.UP:
				self.ship.move_right()
				self._keys.add(key)
				
			if key == arcade.key.B:
				print(self.bullets)
				
			if key == arcade.key.S or key == arcade.key.A:
				pass

			if key == arcade.key.SPACE:
				# bullet = self.create_bullet()
				# self.bullets.append(bullet)
				self.create_bullet()
				# Gunshot sound
				arcade.sound.play_sound(self.gun_sound)

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
			if key == arcade.key.LEFT or key == arcade.key.DOWN:
				self._keys.remove(key)

			if key == arcade.key.RIGHT or key == arcade.key.UP:
				self._keys.remove(key)
				
			if key == arcade.key.W or key == arcade.key.D:
				pass
				
			if key == arcade.key.S or key == arcade.key.A:
				pass

	def create_bullet(self):
		"""
		Creates an instance of laser and appends it to the bullets sprite list
		"""
		laser = Laser(self.ship.center_x, self.ship.center_y)
		self.bullets.append(laser)

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
		self.window.show_view(VIEWS["gameOver"](GameView,self.score))
		#Send score to server
		#send(f"{self.score}")



def main():
	""" Main method """

	window = WINDOW
	menu_view = MenuView()
	window.show_view(menu_view)
	arcade.run()

if __name__ == "__main__":
	main()
