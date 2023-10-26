from utilities.sprites import *


BUTTON_HIGHLIGHT_COLOR = RED
BUTTON_HIGHLIGHT_WIDTH = 4
BUTTON_X_MARGIN = 35
BUTTON_Y_MARGIN = None

SETS_BUTTON_X = SCREEN_WIDTH + RIGHT_MARGIN // 2 - BUTTON_WIDTH // 2
SETS_BUTTON_Y = BUTTON_HEIGHT // 2

SAVE_BUTTON_X = BUTTON_X_MARGIN
SAVE_BUTTON_Y = SCREEN_HEIGHT + BOTTOM_MARGIN // 2 - BUTTON_HEIGHT * 1.25

LOAD_BUTTON_X = SAVE_BUTTON_X + BUTTON_WIDTH * 1.25
LOAD_BUTTON_Y = SCREEN_HEIGHT + BOTTOM_MARGIN // 2 - BUTTON_HEIGHT * 1.25

NAME_BUTTON_X = BUTTON_X_MARGIN
NAME_BUTTON_Y = SCREEN_HEIGHT + BOTTOM_MARGIN // 2 + BUTTON_HEIGHT * 0.25

PREF_BUTTON_X = NAME_BUTTON_X + BUTTON_WIDTH * 1.25
PREF_BUTTON_Y = SCREEN_HEIGHT + BOTTOM_MARGIN // 2 + BUTTON_HEIGHT * 0.25

BACK_BUTTON_X = (SCREEN_WIDTH + RIGHT_MARGIN) // 2 - BUTTON_WIDTH * 1.25
BACK_BUTTON_Y = SCREEN_HEIGHT + BOTTOM_MARGIN - 50

OK_BUTTON_X = (SCREEN_WIDTH + RIGHT_MARGIN) // 2 + BUTTON_WIDTH * 0.25
OK_BUTTON_Y = SCREEN_HEIGHT + BOTTOM_MARGIN - 50

GRID_BUTTON_X = SCREEN_WIDTH - BUTTON_WIDTH - BUTTON_X_MARGIN
GRID_BUTTON_Y = SCREEN_HEIGHT + BUTTON_HEIGHT * 0.5

MAP_BUTTON_X = GRID_BUTTON_X
MAP_BUTTON_Y = GRID_BUTTON_Y + BUTTON_HEIGHT * 1.25

SETS_BTN = {
    "x": SETS_BUTTON_X,
    "y": SETS_BUTTON_Y,
    "image": sets_button_image,
    "scale": 1,
    "name": "sets_btn",
}

SAVE_BTN = {
    "x": SAVE_BUTTON_X,
    "y": SAVE_BUTTON_Y,
    "image": save_button_image,
    "scale": 1,
    "name": "save_btn",
}

LOAD_BTN = {
    "x": LOAD_BUTTON_X,
    "y": LOAD_BUTTON_Y,
    "image": load_button_image,
    "scale": 1,
    "name": "load_btn",
}

NAME_BTN = {
    "x": NAME_BUTTON_X,
    "y": NAME_BUTTON_Y,
    "image": name_button_image,
    "scale": 1,
    "name": "name_btn",
}

PREF_BTN = {
    "x": PREF_BUTTON_X,
    "y": PREF_BUTTON_Y,
    "image": pref_button_image,
    "scale": 1,
    "name": "pref_btn",
}

BACK_BTN = {
    "x": BACK_BUTTON_X,
    "y": BACK_BUTTON_Y,
    "image": back_button_image,
    "scale": 1,
    "name": "back_btn",
}

OK_BTN = {
    "x": OK_BUTTON_X,
    "y": OK_BUTTON_Y,
    "image": ok_button_image,
    "scale": 1,
    "name": "ok_btn",
}

GRID_BTN = {
    "x": GRID_BUTTON_X,
    "y": GRID_BUTTON_Y,
    "image": grid_button_image,
    "scale": 1,
    "name": "grid_btn",
}

MAP_BTN = {
    "x": MAP_BUTTON_X,
    "y": MAP_BUTTON_Y,
    "image": map_button_image,
    "scale": 1,
    "name": "map_btn",
}
