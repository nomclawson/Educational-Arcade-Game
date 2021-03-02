from globals import *
from client import *




class GameOverView(arcade.View):
    """ Class that manages the 'menu' view. """
    def __init__(self, score):
        super().__init__()
        self.score = score
        self.name = "Player"
        self.gui = arcade.gui.UIManager(WINDOW)
        self.inputBox = arcade.gui.UIInputBox(SCREEN_WIDTH//4,30,SCREEN_WIDTH//2,60)
        self.gui.add_ui_element(self.inputBox)
        self.inputBox.render()

    def on_show(self):
        """ Called when switching to this view"""
        arcade.set_background_color(arcade.color.NEON_CARROT)
        

    def on_draw(self):
        """ Draw the menu """
        arcade.start_render()
        arcade.draw_text(f"--GAME OVER--\nScore: {self.score}\nPress Esc to quit.", SCREEN_WIDTH/2, SCREEN_HEIGHT/2,
                         arcade.color.WHITE, font_size=30, anchor_x="center")
        arcade.draw_text(f"Player: {self.name}\nScore: {self.score}", 100, SCREEN_HEIGHT/4,
                         arcade.color.WHITE, font_size=24, anchor_x="center")           

    def on_key_press(self, key, modifiers):
        
        if key == arcade.key.ESCAPE:
            #Send score to server
            send(f"{self.score}")
            arcade.close_window()
            
        if key == arcade.key.ENTER:
            self.name = self.inputBox.text
           