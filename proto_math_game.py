import arcade
from arcade import Sprite
import math

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600



class Game(arcade.Window):
    """
    
    """

    def __init__(self, width, height):
        """
        Sets up the initial conditions of the game
        :param width: Screen width
        :param height: Screen height
        """
        super().__init__(width, height)

        self.score = 0

        self.player = Sprite(filename="demo_player.jpeg")
        self.player.center_x = SCREEN_WIDTH // 2
        self.player.center_y = SCREEN_HEIGHT // 3
        self.player.change_x = 3

        self.bullets = []
        

        
        arcade.set_background_color(arcade.color.CORNFLOWER_BLUE)
        

    def on_draw(self):
        """
        Called automatically by the arcade framework.
        Handles the responsiblity of drawing all elements.
        """

        # clear the screen to begin drawing
        arcade.start_render()
        self.draw_score()
        self.player.draw()
        for bullet in self.bullets:
            bullet.draw()
        


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
        
    

    def update(self, delta_time):
        """
        Update each object in the game.
        :param delta_time: tells us how much time has actually elapsed
        """

        # Check to see if keys are being held, and then
        # take appropriate action
        self.check_keys()
        self.player.update()
        for bullet in self.bullets:
            bullet.update()


        
        if ((self.player.center_x > SCREEN_WIDTH and self.player.change_x > 0) or \
            (self.player.center_x < 0 and self.player.change_x < 0)):
            self.player.change_x *= -1
            
        

    def check_keys(self):
        """
        Checks to see if the user is holding down an
        arrow key, and if so, takes appropriate action.
        """
        pass

    def on_key_press(self, key, key_modifiers):
        """
        Called when a key is pressed. Sets the state of
        holding an arrow key.
        :param key: The key that was pressed
        :param key_modifiers: Things like shift, ctrl, etc
        """
        
        if key == arcade.key.LEFT or key == arcade.key.DOWN:
            self.player.change_x = -3

        if key == arcade.key.RIGHT or key == arcade.key.UP:
            self.player.change_x = 3
            
        if key == arcade.key.W or key == arcade.key.D:
            pass
            
        if key == arcade.key.S or key == arcade.key.A:
            pass

        if key == arcade.key.SPACE:
            bullet = Sprite(filename="game_piece_red.png", center_x=self.player.center_x, center_y=self.player.center_y)
            bullet.change_y = 30
            self.bullets.append(bullet)

            

    def on_key_release(self, key, key_modifiers):
        """
        Called when a key is released. Sets the state of
        the arrow key as being not held anymore.
        :param key: The key that was pressed
        :param key_modifiers: Things like shift, ctrl, etc
        """
        if key == arcade.key.LEFT or key == arcade.key.DOWN:
            pass

        if key == arcade.key.RIGHT or key == arcade.key.UP:
            pass
            
        if key == arcade.key.W or key == arcade.key.D:
            pass
            
        if key == arcade.key.S or key == arcade.key.A:
            pass
            
        

# Creates the game and starts it going
window = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
arcade.run()