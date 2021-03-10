import arcade
from arcade import gui
from client import *

WINDOW = arcade.Window(fullscreen=True,resizable=True)


class GameOverView(arcade.View):
    """ Class that manages the 'menu' view. """
    def __init__(self,GameView,score=0):
        super().__init__()
        self.window.set_mouse_visible(visible=True)
        self.GameView = GameView
        self.score = score
        self.name = "Player"
        self.gui = arcade.gui.UIManager()
        self.inputBox = arcade.gui.UIInputBox(self.window.width//2,self.window.height//3+90,200,30)
        self.gui.add_ui_element(self.inputBox)
        self.inputBox.render()

    def on_show(self):
        """ Called when switching to this view"""
        arcade.set_background_color(arcade.color.NEON_CARROT)
        

    def on_draw(self):
        """ Draw the menu """
        arcade.start_render()
        
        arcade.draw_text(f"--GAME OVER--\n", self.window.width/2, self.window.height/2+50,
                         arcade.color.GRAY, font_size=60, anchor_x="center")
        arcade.draw_text(f"Player: {self.name}\nScore: {self.score}", self.window.width/2, self.window.height/2+50,
                         arcade.color.WHITE, font_size=30, anchor_x="center")
        arcade.draw_text(f" \nEnter Name:", self.window.width/2, self.window.height//3+110,
                         arcade.color.GRAY, font_size=30, anchor_x="center")
                        
        arcade.draw_text(f"Press Esc to quit, R to restart.", self.window.width/2, self.window.height/3,
                         arcade.color.WHITE, font_size=26, anchor_x="center")           

    def on_key_press(self, key, modifiers):
        
        if key == arcade.key.ESCAPE:
            #Send score to server
            send(f"{self.score}")
            arcade.close_window()
            
        if key == arcade.key.ENTER:
            self.name = self.inputBox.text

        if key == arcade.key.R:
            self.window.show_view(self.GameView())
            self.gui._ui_elements.remove(self.inputBox)
            send(f"{self.score}")



