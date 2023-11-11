"""
Action functions for the File Menu.
None of the functions return data.
These functions DO interact with the program directly.
"""

import os
import pickle
from typing import Any

from menu_manager.file_menu import utils
from settings.paths import MAPS_DIR
from utilities import helpers


def save_map_details(editor: Any) -> None:
    """
        Serializes map-dependent variables into pickle format and
            saves it under the maps name.

        Args:
            editor (any): Current Editor object.
    """
    save_data = [
        editor.rows,
        editor.columns,
        editor.grid_size_x,
        editor.grid_size_y,
        editor.world_data
    ]

    with open(file=os.path.join(MAPS_DIR, editor.map_name),
              mode="wb") as pickle_out:
        pickle.dump(obj=save_data,
                    file=pickle_out)


def load_new_map(editor: Any,
                 selected_map: str) -> None:
    """
        Gets deserialized map details and updates the Editors attributes to
            load the new map.

        Args:
            editor (Any): Current Editor instance.
            selected_map (str): Map the user selected to load.
    """
    map_attributes = utils.get_deserialized_map_details(editor=editor,
                                                        map_name=selected_map)
    helpers.update_class_dict(cls=editor,
                              attributes=map_attributes)
