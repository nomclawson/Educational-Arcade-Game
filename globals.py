import arcade
from arcade import Sprite, SpriteList, gui
import math
from random import randint
from views import *


VIEWS = {
    "window" : WINDOW,
    "gameOver" : GameOverView
}


SCREEN_WIDTH = WINDOW.width
SCREEN_HEIGHT = WINDOW.height





SHIP_SPEED = 10

PLAYER_LIVES = 3

