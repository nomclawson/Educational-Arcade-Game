from globals import *

class Ship(Sprite):
    """
    Ship class
    """
    def __init__(self):
        super().__init__(filename="images/star-shooter.png")
        self.center_x = SCREEN_WIDTH // 2
        self.center_y = SCREEN_HEIGHT // 7
        self.scale = .25

    def move_left(self):
        self.change_x = -SHIP_SPEED

    def move_right(self):
        self.change_x = SHIP_SPEED
        