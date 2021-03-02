from globals import *

class Meteor(Sprite):
    """
    Enemies
    """
    def __init__(self):
        super().__init__(filename="images/meteor.png")
        self.scale = .1
        self.center_x = randint(0,SCREEN_WIDTH)
        self.center_y = SCREEN_HEIGHT + (self.height // 2) + 1
        self.change_y = randint(-3,-1)
        self.alive = True