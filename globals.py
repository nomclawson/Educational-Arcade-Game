import arcade
from arcade import Sprite, SpriteList, gui
import math
from random import randint, choice



SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 576
DASHBOARD_WIDTH = SCREEN_WIDTH // 4
SHIP_SPEED = 10
START_DELAY = 120 # 1 in 120 chance per frame * 60 frames per second =~ 1 asteroid per 2 second, I think

PLAYER_LIVES = 3
SCREEN_TITLE = 'Math game'
SHIP_SCALE= .1
LASER_SCALE = .5
LASER_SPEED = 30
METEOR_SCALE = .1
SHOTING_AREA_PADDING_SIDE = 40
SHOTING_AREA_PADDING_BOTTOM = 60


