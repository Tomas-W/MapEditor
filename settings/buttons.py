from utilities.sprites import *


BUTTON_HIGHLIGHT_COLOR = RED
BUTTON_HIGHLIGHT_WIDTH = 4
BUTTON_MARGIN_X = 16
BUTTON_MARGIN_Y = 16

# Presets
SETS_BUTTON_X = SCREEN_WIDTH + RIGHT_MARGIN // 2 - BUTTON_WIDTH // 2
SETS_BUTTON_Y = BUTTON_HEIGHT // 2

# Menu
SAVE_BUTTON_X = BUTTON_MARGIN_X
SAVE_BUTTON_Y = SCREEN_HEIGHT + BUTTON_MARGIN_Y

LOAD_BUTTON_X = SAVE_BUTTON_X
LOAD_BUTTON_Y = SAVE_BUTTON_Y + BUTTON_HEIGHT + BUTTON_MARGIN_Y

NEW_BUTTON_X = SAVE_BUTTON_X
NEW_BUTTON_Y = LOAD_BUTTON_Y + BUTTON_HEIGHT + BUTTON_MARGIN_Y

NAME_BUTTON_X = SAVE_BUTTON_X + BUTTON_WIDTH + BUTTON_MARGIN_X
NAME_BUTTON_Y = SAVE_BUTTON_Y

PREF_BUTTON_X = NAME_BUTTON_X
PREF_BUTTON_Y = LOAD_BUTTON_Y

# Extra Menu
BACK_BUTTON_X = (SCREEN_WIDTH + RIGHT_MARGIN) // 2 - BUTTON_WIDTH * 1.25
BACK_BUTTON_Y = SCREEN_HEIGHT + BOTTOM_MARGIN - 50

OK_BUTTON_X = (SCREEN_WIDTH + RIGHT_MARGIN) // 2 + BUTTON_WIDTH * 0.25
OK_BUTTON_Y = SCREEN_HEIGHT + BOTTOM_MARGIN - 50

# Quick Menu
UNDO_BUTTON_X = SCREEN_WIDTH - (BUTTON_WIDTH + BUTTON_MARGIN_X) * 2
UNDO_BUTTON_Y = SAVE_BUTTON_Y

REDO_BUTTON_X = SCREEN_WIDTH - BUTTON_WIDTH - BUTTON_MARGIN_X
REDO_BUTTON_Y = SAVE_BUTTON_Y

GRID_BUTTON_X = UNDO_BUTTON_X
GRID_BUTTON_Y = LOAD_BUTTON_Y

MAP_BUTTON_X = REDO_BUTTON_X
MAP_BUTTON_Y = LOAD_BUTTON_Y

# Presets
SETS_BTN = {
    "x": SETS_BUTTON_X,
    "y": SETS_BUTTON_Y,
    "image": sets_button_image,
    "scale": 1,
    "name": "sets_btn",
}

# Meun
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

NEW_BTN = {
    "x": NEW_BUTTON_X,
    "y": NEW_BUTTON_Y,
    "image": new_button_image,
    "scale": 1,
    "name": "new_btn",
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

#  Extra Menu
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

# Quick Menu
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

UNDO_BTN = {
    "x": UNDO_BUTTON_X,
    "y": UNDO_BUTTON_Y,
    "image": undo_button_image,
    "scale": 1,
    "name": "undo_btn",
}

REDO_BTN = {
    "x": REDO_BUTTON_X,
    "y": REDO_BUTTON_Y,
    "image": redo_button_image,
    "scale": 1,
    "name": "redo_btn",
}
