"""
Action functions for the Edit Menu.
None of the functions return data.
These functions interact with the program directly.
"""
from typing import Any, Tuple

import numpy as np

from menu_manager.edit_menu import utils

from utilities import helpers
from utilities import render_text
from utilities import fonts

from settings.setup import WHITE
from settings.menus import PREFERENCE_MESSAGE_Y


def prepare_preferences_menu(editor: Any,
                             edit_menu_renderer: Any) -> None:
    """
        Prepares preference menu by selecting a default preference so the user can interact.

        Args:
            editor (Any): Current Editor instance.
            edit_menu_renderer (Any): Current EditMenuRenderer instance.
    """
    edit_menu_renderer.preferences_dict = utils.get_preferences_dict(editor=editor)
    editor.selected_preference_value = editor.rows
    editor.selected_preference_value_change = editor.rows


def load_selected_preference(editor: Any,
                             selected_preference: Tuple[str, int]) -> None:
    """
        Loads the user selected preference and its value so the user can interact.

        Args:
            editor (Any): Current Editor instance.
            selected_preference (Tuple[str, int]): The selected preference and its value.
    """
    editor.selected_preference_name = selected_preference[0]
    editor.selected_preference_value = selected_preference[1]
    editor.selected_preference_value_change = editor.selected_preference_value


def apply_preference_change(menu_renderer: Any,
                            pref_name: str,
                            pref_value_change: int) -> None:
    """
        Takes the user selected (and edited) preference and its value and apply it
            to the Editor.

        Args:
            menu_renderer (Any): Current EditMenuRenderer instance.
            pref_name (str): Name of the preference to change.
            pref_value_change (int): New value of the preference.
    """
    menu_renderer.editor.selected_preference_value = pref_value_change

    # Update settings (row, col, grid_size ect)
    attributes_dict = {
        pref_name: int(pref_value_change)
    }

    helpers.update_class_dict(cls=menu_renderer.editor,
                              attributes=attributes_dict)
    # menu_renderer.editor.background = helpers.update_background(editor=menu_renderer.editor)
    menu_renderer.preferences_dict = utils.get_preferences_dict(editor=menu_renderer.editor)


def update_world_data_size(editor: Any,
                           name: str,
                           value: int) -> None:
    """
        Updates either the row or column of world_data.
        Takes the name and the new value and applies the change.

        Args:
            editor (Any): Current Editor instance.
            name (str): Name of the axis ('rows' or 'columns').
            value (int): New value to be set.

    """
    if name == "rows":
        if value > editor.rows:
            # add rows
            rows = np.full((value - editor.rows, editor.world_data.shape[1]), -1)
            editor.world_data = np.vstack((editor.world_data, rows))
        elif value < editor.rows:
            # remove rows
            editor.world_data = editor.world_data[:value, :]

    elif name == "columns":
        if value > editor.columns:
            # add columns
            cols = np.full((editor.world_data.shape[0], value - editor.columns), -1)
            editor.world_data = np.hstack((editor.world_data, cols))
        elif value < editor.columns:
            # remove columns
            editor.world_data = editor.world_data[:, :value - editor.columns]


def manage_preferences_change(menu_renderer: Any) -> None:
    """
        Checks if the user selected preference and its value are allowed.
        If so, world_data will be updated and a message will appear.
        If not, an error message will appear. Usually this means a tile is placed outside of
            world_data.

        Args:
             menu_renderer (Any): Current EditMenuRenderer instance.
    """
    pref_name = menu_renderer.editor.selected_preference_name
    pref_value = int(menu_renderer.editor.selected_preference_value)
    pref_value_change = int(menu_renderer.editor.selected_preference_value_change)

    if utils.is_new_value_allowed(name=pref_name,
                                  value=pref_value_change):

        # check if tiles are outside the new world_data size
        max_rows, max_cols = utils.get_grid_max_row_col(world_data=menu_renderer.editor.world_data)

        if menu_renderer.editor.selected_preference_name == "rows" and pref_value_change < max_rows:
            update = False
        elif menu_renderer.editor.selected_preference_name == "columns" and pref_value_change < max_cols:
            update = False
        else:
            update = True

        if update:
            # new size is accepted
            update_world_data_size(editor=menu_renderer.editor,
                                   name=menu_renderer.editor.selected_preference_name,
                                   value=pref_value_change)

            accepted_text = utils.get_preferences_accepted_text(pref_name=pref_name,
                                                                pref_value=pref_value,
                                                                pref_value_change=pref_value_change)
            # Blit change successful tet
            render_text.centered_x(screen=menu_renderer.editor.screen,
                                   text=accepted_text,
                                   font=fonts.popup_font,
                                   color=WHITE,
                                   y_pos=PREFERENCE_MESSAGE_Y)

            apply_preference_change(menu_renderer=menu_renderer,
                                    pref_name=pref_name,
                                    pref_value_change=pref_value_change)

    else:
        # new size is not accepted
        denied_text = utils.get_preferences_denied_text(
            pref_name=pref_name,
            pref_value=pref_value,
            pref_value_change=pref_value_change)
        # Blit denied text
        render_text.centered_x(screen=menu_renderer.editor.screen,
                               text=denied_text,
                               font=fonts.popup_font,
                               color=WHITE,
                               y_pos=PREFERENCE_MESSAGE_Y)
