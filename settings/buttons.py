from utilities.sprites import *


SETS_BUTTON_X = SCREEN_WIDTH + RIGHT_MARGIN // 2 - BUTTON_WIDTH // 2
SETS_BUTTON_Y = BUTTON_HEIGHT // 2

SAVE_BUTTON_X = 35
SAVE_BUTTON_Y = SCREEN_HEIGHT + BOTTOM_MARGIN // 2 - BUTTON_HEIGHT * 1.25

LOAD_BUTTON_X = SAVE_BUTTON_X + BUTTON_WIDTH * 1.25
LOAD_BUTTON_Y = SCREEN_HEIGHT + BOTTOM_MARGIN // 2 - BUTTON_HEIGHT * 1.25

NAME_BUTTON_X = 35
NAME_BUTTON_Y = SCREEN_HEIGHT + BOTTOM_MARGIN // 2 + BUTTON_HEIGHT * 0.25

PREF_BUTTON_X = NAME_BUTTON_X + BUTTON_WIDTH * 1.25
PREF_BUTTON_Y = SCREEN_HEIGHT + BOTTOM_MARGIN // 2 + BUTTON_HEIGHT * 0.25

BACK_BUTTON_X = (SCREEN_WIDTH + RIGHT_MARGIN) // 2 - BUTTON_WIDTH * 1.25
BACK_BUTTON_Y = SCREEN_HEIGHT + BOTTOM_MARGIN - 50

OK_BUTTON_X = (SCREEN_WIDTH + RIGHT_MARGIN) // 2 + BUTTON_WIDTH * 0.25
OK_BUTTON_Y = SCREEN_HEIGHT + BOTTOM_MARGIN - 50


SETS_BTN_INACTIVE = {
    "x": SETS_BUTTON_X,
    "y": SETS_BUTTON_Y,
    "image": sets_button_image,
    "scale": 1,
    "tile_index": None,
}

SETS_BTN_SELECTED = {
    "x": SETS_BUTTON_X,
    "y": SETS_BUTTON_Y,
    "image": sets_button_image,
    "scale": 1,
    "tile_index": None,
}

SETS_BTN_ACTIVE = {
    "x": SETS_BUTTON_X,
    "y": SETS_BUTTON_Y,
    "image": sets_button_image,
    "scale": 1,
    "tile_index": None,
}

SAVE_BTN_INACTIVE = {
    "x": SAVE_BUTTON_X,
    "y": SAVE_BUTTON_Y,
    "image": save_button_image,
    "scale": 1,
    "tile_index": None,
}

LOAD_BTN_INACTIVE = {
    "x": LOAD_BUTTON_X,
    "y": LOAD_BUTTON_Y,
    "image": load_button_image,
    "scale": 1,
    "tile_index": None,
}

NAME_BTN_INACTIVE = {
    "x": NAME_BUTTON_X,
    "y": NAME_BUTTON_Y,
    "image": name_button_image,
    "scale": 1,
    "tile_index": None,
}

PREF_BTN_INACTIVE = {
    "x": PREF_BUTTON_X,
    "y": PREF_BUTTON_Y,
    "image": pref_button_image,
    "scale": 1,
    "tile_index": None,
}

BACK_BTN_INACTIVE = {
    "x": BACK_BUTTON_X,
    "y": BACK_BUTTON_Y,
    "image": back_button_image,
    "scale": 1,
    "tile_index": None,
}

OK_BTN_INACTIVE = {
    "x": OK_BUTTON_X,
    "y": OK_BUTTON_Y,
    "image": ok_button_image,
    "scale": 1,
    "tile_index": None,
}