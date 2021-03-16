from globals import *

class Meteor(Sprite):
    """
    Enemies
    """
    def __init__(self):
        super().__init__(filename="images/meteor.png")
        self.scale = METEOR_SCALE
        self.center_x = randint(RELOAD_BOX_WIDTH + SHOTING_AREA_PADDING_SIDE, SCREEN_WIDTH - SHOTING_AREA_PADDING_SIDE)
        self.center_y = SCREEN_HEIGHT + (self.height // 2) + 1
        self.change_y = randint(-2,-1)
        self.alive = True