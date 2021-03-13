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
        arcade.draw_text(f"Player: {self.name}\nScore: {self.score}", self.window.width/2, self.window.height/2+40,
                         arcade.color.BLACK, font_size=30, anchor_x="center")

        if self.inputBox in self.gui._ui_elements:
            arcade.draw_text(f" \nEnter Name:", self.window.width/2, self.window.height//3+110,
                            arcade.color.GRAY, font_size=30, anchor_x="center")

            arcade.draw_text(f"Press Enter to submit name.", self.window.width/2, self.window.height/3,
                            arcade.color.WHITE, font_size=26, anchor_x="center")
                        
        arcade.draw_text(f"Press Esc to quit, F1 to restart.", self.window.width/2, self.window.height/4,
                         arcade.color.WHITE, font_size=26, anchor_x="center")           

    def on_key_press(self, key, modifiers):
        # Quit game with ESCAPE
        if key == arcade.key.ESCAPE:
            self.get_name()
            #Send score to server
            self.send_score()
            arcade.close_window()
        
        # Submit Name with ENTER
        if key == arcade.key.ENTER:
            self.name = self.inputBox.text          
            self.gui._ui_elements.remove(self.inputBox)

        # Restart with F1
        if key == arcade.key.F1:
            self.get_name()
            try:
                self.gui._ui_elements.remove(self.inputBox)
            except:
                print("something happened")
            
            self.window.show_view(self.GameView())
            self.send_score()
            
    def get_name(self):
        if self.inputBox.text != "":
            self.name = self.inputBox.text

    def send_score(self):
        if self.score > 0:
            send(f"{self.name}:{self.score}")