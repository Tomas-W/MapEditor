"""
Action functions for the Preset Menu.
None of the functions return data.
These functions DO interact with the program directly.
"""

from typing import Any

from utilities import sprites, general, buttons


def load_new_preset(editor: Any,
                    menu_controller: Any,
                    selected_preset: str) -> None:
    """
        Updates the Editor so the new preset is loaded.
        Sets current_object,
            tile_list,
            tile_names,
            tile_buttons and
            sets the correct Menu Controller state.

        Args:
            editor (Any): Current Editor instance.
            menu_controller (Any): Current MenuController instance.
            selected_preset (str): Name of the preset to load.
    """
    editor.current_preset = selected_preset
    editor.current_tile = 0

    editor.current_object = general.get_tile_indexes(
        preset_name=editor.current_preset)[0]
    editor.tile_list = sprites.get_preset_sprites(
        preset_name=editor.current_preset
    )
    editor.tile_names = general.get_tile_names(
        preset_name=editor.current_preset
    )
    editor.tile_buttons = buttons.get_tile_buttons(
        preset_name=editor.current_preset,
        editor=editor
    )
    menu_controller.set_state("preset_menu")
