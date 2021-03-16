from globals import *

class Ship(Sprite):
    """
    Ship class
    """
    def __init__(self ):
        super().__init__(filename="images/star-shooter.png")
        self.center_x = (SCREEN_WIDTH - RELOAD_BOX_WIDTH) // 2 + RELOAD_BOX_WIDTH
        self.center_y = SHOTING_AREA_PADDING_BOTTOM
        self.scale = SHIP_SCALE
        self.alive = True
        self.framesAfterDead = 20

    def move_left(self):
        #Check if the ship can move left
        if (self.center_x > RELOAD_BOX_WIDTH + SHOTING_AREA_PADDING_SIDE):
            self.center_x = self.center_x - SHIP_SPEED

    def move_right(self):
        #Check if the ship can move right
        if (self.center_x < SCREEN_WIDTH - SHOTING_AREA_PADDING_SIDE):
            self.center_x = self.center_x + SHIP_SPEED
        