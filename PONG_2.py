"""
File: pong.py
Original Author: Br. Burton
Designed to be completed by others
This program implements a simplistic version of the
classic Pong arcade game.
"""
import arcade
import random

# These are Global constants to use throughout the game
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
BALL_RADIUS = 10

PADDLE_WIDTH = 10
PADDLE_HEIGHT = 50
MOVE_AMOUNT = 5

SCORE_HIT = 1
SCORE_MISS = 0

class Point:
    """
    Point class contains an x and a y coordinate.
    """
    def __init__(self):
        self.x = 0
        self.y = 0
        
class PaddlePoint():
    def __init__(self):
        #super().__init__()
        self.x = 0
        self._y = 0
        
    @property
    def y(self):
        return self._y
    
    @y.setter
    def y(self, y):
        if y + (PADDLE_HEIGHT / 2) > SCREEN_HEIGHT:
            self._y = SCREEN_HEIGHT - (PADDLE_HEIGHT / 2)
        elif y - (PADDLE_HEIGHT / 2) < 0:
            self._y = PADDLE_HEIGHT / 2
        else:
            self._y = y

class Velocity:
    """
    Velocity Class contains a horizontal (dx) and a vertical (dy) velocity.
    """
    def __init__(self):
        self.dx = 0     
        self.dy = 0
        
    
class Ball:
    """
    Ball Class has-a Point object and a Velocity object. It
    has the capacity to bounce vertically and horizontally
    when called.
    """
    def __init__(self):
        self.restart()
    
    # Draw's the ball
    def draw(self):
        arcade.draw_circle_filled(self.center.x,self.center.y,
                           BALL_RADIUS,arcade.color.EGYPTIAN_BLUE)
        arcade.draw_circle_filled(self.center.x,self.center.y,
                           BALL_RADIUS / 2,arcade.color.BRIGHT_GREEN)        
    
    # Move's ball across screen
    def advance(self):
        self.center.x += self.velocity.dx
        self.center.y += self.velocity.dy
        
    
    # Reverses the x (horizontal) direction of the ball
    def bounce_horizontal(self):
        self.velocity.dx *= -1

    # Reverses the y (vertical) direction of the ball
    def bounce_vertical(self):
        self.velocity.dy *= -1
    
    # Places ball in new starting position
    def restart(self):
        self.center = Point()
        self.center.x = SCREEN_WIDTH // 2
        self.center.y = random.randint(0,SCREEN_WIDTH)
        
        self.velocity = Velocity()
        
        
        self.velocity.dx = random.randint(2,4)
        if random.randint(0,1) == 0:
            self.velocity.dx *= -1
        
        self.velocity.dy = random.randint(3,6)
        if random.randint(0,1) == 0:
            self.velocity.dy *= -1        
        

class Paddle:
    """
    Paddle class has-a Point object. Enables paddle to
    move up and down on the screen.
    """
    def __init__(self):
        self.center = PaddlePoint()
        self.center.y = SCREEN_HEIGHT/2
        self.score = 0

    # Draws paddle on screen
    def draw(self):
        arcade.draw_rectangle_filled(self.center.x,self.center.y,
                                     PADDLE_WIDTH,PADDLE_HEIGHT,(100,100,100))
    
    # Moves paddle up the screen without leaving the screen
    def move_up(self):
        self.center.y += MOVE_AMOUNT
        
    # Moves paddle down the screen without leaving the screen
    def move_down(self):
        self.center.y -= MOVE_AMOUNT

class Pong(arcade.Window):
    """
    This class handles all the game callbacks and interaction
    It assumes the following classes exist:
        Point
        Velocity
        Ball
        Paddle
    This class will then call the appropriate functions of
    each of the above classes.
    You are welcome to modify anything in this class,
    but should not have to if you don't want to.
    """

    def __init__(self, width, height):
        """
        Sets up the initial conditions of the game
        :param width: Screen width
        :param height: Screen height
        """
        super().__init__(width, height)

        self.ball = Ball()
        self.paddle1 = Paddle()
        self.paddle2 = Paddle()
        self.init_paddle()
        self.score = 0

        # These are used to see if the user is
        # holding down the arrow keys
        self.holding_left = False
        self.holding_right = False
        
        self.holding_w = False
        self.holding_s = False

        arcade.set_background_color(arcade.color.CORNFLOWER_BLUE)
        
    def init_paddle(self):
        self.paddle2.center.x = (PADDLE_WIDTH / 2)
        self.paddle2.center.y = SCREEN_HEIGHT / 2
        
        self.paddle1.center.x = SCREEN_WIDTH - (PADDLE_WIDTH / 2)
        self.paddle1.center.y = SCREEN_HEIGHT / 2

    def on_draw(self):
        """
        Called automatically by the arcade framework.
        Handles the responsiblity of drawing all elements.
        """

        # clear the screen to begin drawing
        arcade.start_render()

        # draw each object
        self.ball.draw()
        self.paddle1.draw()
        self.paddle2.draw()

        self.draw_score()

    def draw_score(self):
        """
        Puts the current score on the screen
        """
        
        score_text = "Score: {}".format(self.paddle1.score)
        start_x = 10
        start_y = SCREEN_HEIGHT - 20
        
        arcade.draw_rectangle_filled(50, start_y + 5,90,20,(0,0,0,150))
        arcade.draw_text(score_text, start_x=start_x, start_y=start_y,
                         font_size=12, color=arcade.color.WHITE)
        
        score_text = "Score: {}".format(self.paddle2.score)
        start_x = SCREEN_WIDTH - 80
        arcade.draw_rectangle_filled(SCREEN_WIDTH - 40, start_y + 5,90,20,(0,0,0,150))
        arcade.draw_text(score_text, start_x=start_x, start_y=start_y,
                         font_size=12, color=arcade.color.WHITE)

    def update(self, delta_time):
        """
        Update each object in the game.
        :param delta_time: tells us how much time has actually elapsed
        """

        # Move the ball forward one element in time
        self.ball.advance()

        # Check to see if keys are being held, and then
        # take appropriate action
        self.check_keys()

        # check for ball at important places
        self.check_miss()
        self.check_hit(self.paddle1)
        self.check_hit(self.paddle2)
        self.check_bounce()

    def check_hit(self,paddle):
        """
        Checks to see if the ball has hit the paddle
        and if so, calls its bounce method.
        :return:
        """
        too_close_x = (PADDLE_WIDTH / 2) + BALL_RADIUS
        too_close_y = (PADDLE_HEIGHT / 2) + BALL_RADIUS

        if (abs(self.ball.center.x - paddle.center.x) < too_close_x and
                    abs(self.ball.center.y - paddle.center.y) < too_close_y):
            # we are too close and moving right, this is a hit!
            self.ball.bounce_horizontal()
            paddle.score += SCORE_MISS

    def check_miss(self):
        """
        Checks to see if the ball went past the paddle
        and if so, restarts it.
        """
        if self.ball.center.x > SCREEN_WIDTH:
            # We missed!
            self.paddle1.score += SCORE_HIT
            self.ball.restart()
            
        if self.ball.center.x < 0:
            self.paddle2.score += SCORE_HIT
            self.ball.restart()

    def check_bounce(self):
        """
        Checks to see if the ball has hit the borders
        of the screen and if so, calls its bounce methods.
        """

        if self.ball.center.y - BALL_RADIUS < 0 and self.ball.velocity.dy < 0:
            self.ball.bounce_vertical()

        if self.ball.center.y + BALL_RADIUS > SCREEN_HEIGHT and self.ball.velocity.dy > 0:
            self.ball.bounce_vertical()

    def check_keys(self):
        """
        Checks to see if the user is holding down an
        arrow key, and if so, takes appropriate action.
        """
        if self.holding_left:
            self.paddle1.move_down()

        if self.holding_right:
            self.paddle1.move_up()
            
        if self.holding_w:
            self.paddle2.move_up()
            
        if self.holding_s:
            self.paddle2.move_down()

    def on_key_press(self, key, key_modifiers):
        """
        Called when a key is pressed. Sets the state of
        holding an arrow key.
        :param key: The key that was pressed
        :param key_modifiers: Things like shift, ctrl, etc
        """
        
        if key == arcade.key.LEFT or key == arcade.key.DOWN:
            self.holding_left = True

        if key == arcade.key.RIGHT or key == arcade.key.UP:
            self.holding_right = True
            
        if key == arcade.key.W or key == arcade.key.D:
            self.holding_w = True
            
        if key == arcade.key.S or key == arcade.key.A:
            self.holding_s = True
            

    def on_key_release(self, key, key_modifiers):
        """
        Called when a key is released. Sets the state of
        the arrow key as being not held anymore.
        :param key: The key that was pressed
        :param key_modifiers: Things like shift, ctrl, etc
        """
        if key == arcade.key.LEFT or key == arcade.key.DOWN:
            self.holding_left = False

        if key == arcade.key.RIGHT or key == arcade.key.UP:
            self.holding_right = False
            
        if key == arcade.key.W or key == arcade.key.D:
            self.holding_w = False
            
        if key == arcade.key.S or key == arcade.key.A:
            self.holding_s = False
            
        

# Creates the game and starts it going
window = Pong(SCREEN_WIDTH, SCREEN_HEIGHT)
arcade.run()