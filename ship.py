from globals import *

class Ship(Sprite):
    """
    Ship class
    """
    def __init__(self ):
        super().__init__(filename="images/ship2.png")
        self.center_x = (SCREEN_WIDTH - DASHBOARD_WIDTH) // 2 + DASHBOARD_WIDTH
        self.center_y = SHOTING_AREA_PADDING_BOTTOM
        self.scale = SHIP_SCALE
        self.alive = True
        self.framesAfterDead = 20

    def move_left(self):
        #Check if the ship can move left
        if (self.center_x > DASHBOARD_WIDTH + SHOTING_AREA_PADDING_SIDE):
            self.center_x = self.center_x - SHIP_SPEED

    def move_right(self):
        #Check if the ship can move right
        if (self.center_x < SCREEN_WIDTH - SHOTING_AREA_PADDING_SIDE):
            self.center_x = self.center_x + SHIP_SPEED
        