import arcade


GRAVITY = -.45 # Pixels per frame squared
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
BALL_RADIUS = 15


class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        
class Velocity:
    def __init__(self, dx=0, dy=0):
        self.dx = dx
        self.dy = dy
        
class Acceleration:
    def __init__(self, ddx=0, ddy=0):
        self.ddy = GRAVITY + ddy
        self.ddx = ddx


class Ball:
    """
    BALL:
    
    """
    def __init__(self,x=0,y=0):
        self.vel = Velocity(dx=1.5)
        self.cen = Point(x,y)
        self.radius = BALL_RADIUS
        self.a = Acceleration()
        
    def draw(self):
        arcade.draw_circle_filled(self.cen.x,self.cen.y,self.radius,arcade.color.RED)
    
    def advance(self):
        self.accelerate()
        self.cen.x += self.vel.dx
        self.cen.y += self.vel.dy
        
    def accelerate(self):
        self.vel.dy += self.a.ddy
        self.vel.dx += self.a.ddx
        
    def bot(self):
        return self.cen.y - self.radius
    
    def top(self):
        return self.cen.y + self.radius
    
    def left(self):
        return self.cen.x - self.radius
    
    def right(self):
        return self.cen.x + self.radius
        
    def bounce_vert(self):
        #self.vel.dy *= -1
        if self.vel.dy >= .9 or self.vel.dy <= -.9:
            self.vel.dy *= -.93
        else:
            self.vel.dy = 0
            self.a.ddy = 0
            
    def bounce_horz(self):
        self.vel.dx *= -1
        
        
        

class Curve:
    def __init__(self):
        self.function = self.func
        self.m = 1
        
    def func(self,x):
        # y = 0
        y = -x*self.m + SCREEN_HEIGHT - 30
        return y
    
    def func_x(self,y):
        x = (-y + SCREEN_HEIGHT - 30) / self.m
        return x
    
    def is_below(self, x, y):
        return y <= self.func(x)
        
    def draw(self):
        arcade.draw_triangle_filled(0,self.func(SCREEN_WIDTH), self.func_x(SCREEN_HEIGHT-30),SCREEN_HEIGHT-30, \
                                    SCREEN_WIDTH,self.func(SCREEN_WIDTH), \
                                    arcade.color.BLUE_SAPPHIRE)
        

    

class Game(arcade.Window):


    def __init__(self, width, height):
        super().__init__(width, height)
        self.restart()
        self.ground = 20
        
        
    def restart(self):    
        arcade.set_background_color(arcade.color.SMOKY_BLACK)

        self.held_keys = set()
        self.surface = Curve()
        self.ball = Ball(10, SCREEN_HEIGHT)
        


    def on_draw(self):
        """
        Called automatically by the arcade framework.
        Handles the responsibility of drawing all elements.
        """

        # clear the screen to begin drawing
        arcade.start_render()
        
        self.surface.draw()
        self.ball.draw()
            
          
    def update(self, delta_time):
        """
        Update each object in the game.
        :param delta_time: tells us how much time has actually elapsed
        """
        self.check_keys()
        self.check_bounce()
        
        self.ball.advance()
        
    
    def check_bounce(self):
        #print(self.ball.vel.dy)
        if self.surface.is_below(self.ball.cen.x, self.ball.bot()) and self.ball.vel.dy <= 0:
            self.ball.bounce_vert()
            
            


    def check_keys(self):
        """
        This function checks for keys that are being held down.
        You will need to put your own method calls in here.
        """
       
              
        if arcade.key.LEFT in self.held_keys:
            self.ship1.turn_left()

        if arcade.key.RIGHT in self.held_keys:
            self.ship1.turn_right()

        if arcade.key.UP in self.held_keys:
            self.ship1.thrust_forward()

        if arcade.key.DOWN in self.held_keys:
            self.ship1.thrust_backward()
                
        

        # Machine gun mode...
        # if arcade.key.SPACE in self.held_keys:
        #    pass


    def on_key_press(self, key: int, modifiers: int):
        """
        Puts the current key in the set of keys that are being held.
        You will need to add things here to handle firing the bullet.
        """
        """
        if self.ship1.alive:
            self.held_keys.add(key)
            if not self.ship1.shield.active:
                if key == arcade.key.SPACE:
                    self.lasers1.append(self.ship1.fire_laser())
                    """
        self.held_keys.add(key)
        
        if arcade.key.R in self.held_keys:
            self.restart()
        
            

    def on_key_release(self, key: int, modifiers: int):
        """
        Removes the current key from the set of held keys.
        """
        if key in self.held_keys:
            self.held_keys.remove(key)
            
    
# Creates the game and starts it going
window = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
arcade.run() 