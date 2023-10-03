import os
import sys


EDITOR_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))
IMAGES_DIR = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "images/")
MAPS_DIR = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "maps/")

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
BOTTOM_MARGIN = 150
RIGHT_MARGIN = 300

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 300

FPS = 60

ROWS = 80
COLUMNS = 80
GRID_SIZE_X = 32
GRID_SIZE_Y = 32

TILE_SIZE_X = 32
TILE_SIZE_Y = 32
TILE_TYPES = 15
TILE_NAMES = ["TopL", "TopR", "BotR", "BotL", "EndL", "EndR", "EndB", "EndT", "Horiz", "Vertic", "SplitL", "SplitR",   "SplitB", "SplitT", "Cross"]
# TILE_NAMES = ["┌", "┐", "└", "┘", "─", "│", "←", "→", "↑", "↓", "┬", "┴", "├", "┤", "+"]

BROWN = (105, 70, 35)
DARK_BROWN = (95, 78, 57)
ORANGE = (166, 101, 68)
DARK_ORANGE = (130, 98, 83)
WHITE = (255, 255, 255)
RED = (200, 25, 25)
