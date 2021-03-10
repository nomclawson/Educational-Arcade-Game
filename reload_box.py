from globals import *

class ReloadBox():
    def __init__(self):
        self.color = arcade.color.DARK_GRAY
        self.left = 0
        self.right = SCREEN_WIDTH//4
        self.top = SCREEN_HEIGHT
        self.bottom = 0
    
    def draw(self):
        arcade.draw_lrtb_rectangle_filled(self.left, self.right, self.top, self.bottom, self.color)