from globals import *

class Laser(Sprite):
    """
    weapon
    """
    def __init__(self, x, y):
        super().__init__(filename=":resources:images/space_shooter/laserBlue01.png")
        self.scale = LASER_SCALE
        self.center_x = x
        self.center_y = y
        self.change_y = LASER_SPEED
        self.angle = 90
        self.alive = True