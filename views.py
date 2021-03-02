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
    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ If the user presses the mouse button, re-start the game. """
        """game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)"""
        game_view = GameView()
        self.window.show_view(game_view)
        