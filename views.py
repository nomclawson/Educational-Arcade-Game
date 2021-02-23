from globals import *





class GameOverView(arcade.View):
    """ Class that manages the 'menu' view. """
    def __init__(self, score):
        super().__init__()
        self.score = score

    def on_show(self):
        """ Called when switching to this view"""
        arcade.set_background_color(arcade.color.NEON_CARROT)

    def on_draw(self):
        """ Draw the menu """
        arcade.start_render()
        arcade.draw_text(f"--GAME OVER--\nScore: {self.score}", SCREEN_WIDTH/2, SCREEN_HEIGHT/2,
                         arcade.color.WHITE, font_size=30, anchor_x="center")
        