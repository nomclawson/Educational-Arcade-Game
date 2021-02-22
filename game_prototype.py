from globals import *
from meteors import Meteor



PLAYER_SPEED = 5

class MenuView(arcade.View):
    """ Class that manages the 'menu' view. """

    def on_show(self):
        """ Called when switching to this view"""
        arcade.set_background_color(arcade.color.BLACK_LEATHER_JACKET)

    def on_draw(self):
        """ Draw the menu """
        arcade.start_render()
        arcade.draw_text("Math Game?", SCREEN_WIDTH/2, SCREEN_HEIGHT/2,
                         arcade.color.WHITE, font_size=30, anchor_x="center")
        #arcade.draw_text("Click if you want!", SCREEN_WIDTH/2, SCREEN_HEIGHT/2,
        #                 arcade.color.BLACK, font_size=30, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ Use a mouse press to advance to the 'game' view. """
        game_view = GameView()
        self.window.show_view(game_view)


class GameView(arcade.View):
    """
    
    """

    def __init__(self):
        """
        Sets up the initial conditions of the game
        :param width: Screen width
        :param height: Screen height
        """
        super().__init__()

        self._keys = set()

        self.score = 0

        self.init_player()

        self.window.set_mouse_visible(False)

        self.bullets = []

        self.meteors = []

        
        arcade.set_background_color(arcade.color.BLACK_LEATHER_JACKET)

    def init_player(self):
        self.player = Sprite(filename="star-shooter.png")
        self.player.center_x = SCREEN_WIDTH // 2
        self.player.center_y = SCREEN_HEIGHT // 7
        self.player.scale = .25
        

    def on_draw(self):
        """
        Called automatically by the arcade framework.
        Handles the responsiblity of drawing all elements.
        """

        # clear the screen to begin drawing
        arcade.start_render()
        self.draw_score()
        
        for bullet in self.bullets:
            bullet.draw()

        for meteor in self.meteors:
            meteor.draw()

        self.player.draw()
        


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
        self.check_off_screen()
        
        for bullet in self.bullets:
            bullet.update()

        for meteor in self.meteors:
            meteor.update()

        if randint(0,50) == 1:
            self.create_meteor()


        if ((self.player.center_x > SCREEN_WIDTH and self.player.change_x > 0) or \
            (self.player.center_x < 0 and self.player.change_x < 0)):
            self.player.change_x = 0

    def create_meteor(self):
        self.meteors.append(Meteor())

        
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
            self.player.update()

    def on_key_press(self, key, key_modifiers):
        """
        Called when a key is pressed. Sets the state of
        holding an arrow key.
        :param key: The key that was pressed
        :param key_modifiers: Things like shift, ctrl, etc
        """
        
        if key == arcade.key.LEFT or key == arcade.key.DOWN:
            self.player.change_x = -PLAYER_SPEED
            self._keys.add(key)

        if key == arcade.key.RIGHT or key == arcade.key.UP:
            self.player.change_x = PLAYER_SPEED
            self._keys.add(key)
            
        if key == arcade.key.B:
            print(self.bullets)
            
        if key == arcade.key.S or key == arcade.key.A:
            pass

        if key == arcade.key.SPACE:
            bullet = Sprite(filename="bullet.png", \
                center_x=self.player.center_x, center_y=self.player.center_y)
            bullet.change_y = 30
            bullet.scale = .20
            self.bullets.append(bullet)

            

    def on_key_release(self, key, key_modifiers):
        """
        Called when a key is released. Sets the state of
        the arrow key as being not held anymore.
        :param key: The key that was pressed
        :param key_modifiers: Things like shift, ctrl, etc
        """
        if key == arcade.key.LEFT or key == arcade.key.DOWN:
            self._keys.remove(key)

        if key == arcade.key.RIGHT or key == arcade.key.UP:
            self._keys.remove(key)
            
        if key == arcade.key.W or key == arcade.key.D:
            pass
            
        if key == arcade.key.S or key == arcade.key.A:
            pass
            
        

def main():
    """ Main method """

    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT)
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()

if __name__ == "__main__":
    main()