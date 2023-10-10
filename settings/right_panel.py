from .setup import *


RIGHT_PANEL_COLOR = BROWN

# ######## Sets button ######## #
SETS_BUTTON_X = SCREEN_WIDTH + RIGHT_MARGIN // 2 - BUTTON_WIDTH // 2
SETS_BUTTON_Y = BUTTON_HEIGHT // 2


# ######## Tabs ######## #
TAB_NAME_FONT_HEIGHT = 32  # linked with fonts.py
TAB_NAME_X_OFFSET = SCREEN_WIDTH + 20
TAB_NAME_Y_OFFSET = 75
TAB_NAME_Y_SPACING = TAB_NAME_FONT_HEIGHT * 1.5
TAB_HIGHLIGHT_WIDTH = 3
TAB_HIGHLIGHT_LEFT_OFFSET = -5
TAB_HIGHLIGHT_RIGHT_OFFSET = 10
TAB_HIGHLIGHT_TOP_OFFSET = - TAB_HIGHLIGHT_WIDTH * 2
TAB_HIGHLIGHT_BOTTOM_OFFSET = TAB_HIGHLIGHT_WIDTH * 2

TAB_NAME_COLOR = (255, 255, 255)
TAB_HIGHLIGHT_COLOR = (200, 25, 25)


# ######## Tile Preview ######## #
PREVIEW_X = SCREEN_WIDTH + RIGHT_MARGIN - 64
PREVIEW_Y_OFFSET = 70
PREVIEW_WIDTH = 32
PREVIEW_HEIGHT = 32


# ######## Tiles ######## #
TILE_SIZE_X = 32
TILE_SIZE_Y = 32
TILE_TYPES = 15

TILE_HIGHLIGHT_COLOR = (200, 25, 25)
TILE_LABEL_COLOR = (255, 255, 255)

TILE_START_Y = 100
TILE_BUTTON_Y_OFFSET = 30
TILE_LABEL_Y_OFFSET = 20
TILE_HIGHLIGHT_WIDTH = 3
TILE_HIGHLIGHT_LEFT_OFFSET = -3
TILE_HIGHLIGHT_RIGHT_OFFSET = 6