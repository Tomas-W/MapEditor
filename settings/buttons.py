from utilities.sprites import *


BUTTON_HIGHLIGHT_COLOR = RED
BUTTON_HIGHLIGHT_WIDTH = 4
BUTTON_MARGIN_X = 16
BUTTON_MARGIN_Y = 16

# Presets Buttons
SETS_BUTTON_X = SCREEN_WIDTH + RIGHT_MARGIN // 2 - BUTTON_WIDTH // 2
SETS_BUTTON_Y = BUTTON_HEIGHT // 2

# Menu Buttons
FILE_BUTTON_X = BUTTON_MARGIN_X
FILE_BUTTON_Y = SCREEN_HEIGHT + BUTTON_MARGIN_Y

EDIT_BUTTON_X = FILE_BUTTON_X
EDIT_BUTTON_Y = FILE_BUTTON_Y + BUTTON_HEIGHT + BUTTON_MARGIN_Y

TEST_BUTTON_Y = EDIT_BUTTON_Y + BUTTON_HEIGHT + BUTTON_MARGIN_Y

# File Menu Buttons
SAVE_BUTTON_X = FILE_BUTTON_X + BUTTON_WIDTH + BUTTON_MARGIN_X * 2
SAVE_BUTTON_Y = FILE_BUTTON_Y

LOAD_BUTTON_X = SAVE_BUTTON_X + BUTTON_WIDTH + BUTTON_MARGIN_X
LOAD_BUTTON_Y = SAVE_BUTTON_Y

NAME_BUTTON_X = SAVE_BUTTON_X
NAME_BUTTON_Y = SAVE_BUTTON_Y + BUTTON_HEIGHT + BUTTON_MARGIN_Y

NEW_BUTTON_X = LOAD_BUTTON_X
NEW_BUTTON_Y = NAME_BUTTON_Y

# Edit Menu Buttons
PREF_BUTTON_X = EDIT_BUTTON_X + BUTTON_WIDTH + BUTTON_MARGIN_X * 2
PREF_BUTTON_Y = FILE_BUTTON_Y

CROP_BUTTON_X = PREF_BUTTON_X + BUTTON_WIDTH + BUTTON_MARGIN_X
CROP_BUTTON_Y = PREF_BUTTON_Y

WIPE_BUTTON_X = PREF_BUTTON_X
WIPE_BUTTON_Y = EDIT_BUTTON_Y

# General Menu
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
GRID_BUTTON_Y = LOAD_BUTTON_Y + BUTTON_HEIGHT + BUTTON_MARGIN_Y

MAP_BUTTON_X = REDO_BUTTON_X
MAP_BUTTON_Y = GRID_BUTTON_Y

ZOOM_IN_BUTTON_X = UNDO_BUTTON_X
ZOOM_IN_BUTTON_Y = TEST_BUTTON_Y

ZOOM_OUT_BUTTON_X = REDO_BUTTON_X
ZOOM_OUT_BUTTON_Y = TEST_BUTTON_Y

# Presets Buttons
SETS_BTN = {
    "x": SETS_BUTTON_X,
    "y": SETS_BUTTON_Y,
    "image": sets_button_image,
    "scale": 1,
    "name": "sets_btn",
}

# Menu Buttons
FILE_BTN = {
    "x": FILE_BUTTON_X,
    "y": FILE_BUTTON_Y,
    "image": file_button_image,
    "scale": 1,
    "name": "file_btn",
}

EDIT_BTN = {
    "x": EDIT_BUTTON_X,
    "y": EDIT_BUTTON_Y,
    "image": edit_button_image,
    "scale": 1,
    "name": "edit_btn",
}

# File Menu Buttons
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

# Edit Menu Buttons
PREF_BTN = {
    "x": PREF_BUTTON_X,
    "y": PREF_BUTTON_Y,
    "image": pref_button_image,
    "scale": 1,
    "name": "pref_btn",
}

CROP_BTN = {
    "x": CROP_BUTTON_X,
    "y": CROP_BUTTON_Y,
    "image": crop_button_image,
    "scale": 1,
    "name": "crop_btn",
}

WIPE_BTN = {
    "x": WIPE_BUTTON_X,
    "y": WIPE_BUTTON_Y,
    "image": wipe_button_image,
    "scale": 1,
    "name": "wipe_btn",
}

# General Menu
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

ZOOM_IN_BTN = {
    "x": ZOOM_IN_BUTTON_X,
    "y": ZOOM_IN_BUTTON_Y,
    "image": zoom_in_button_image,
    "scale": 1,
    "name": "zoom_in_btn",
}
ZOOM_OUT_BTN = {
    "x": ZOOM_OUT_BUTTON_X,
    "y": ZOOM_OUT_BUTTON_Y,
    "image": zoom_out_button_image,
    "scale": 1,
    "name": "zoom_out_btn",
}



