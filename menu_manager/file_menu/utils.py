import os
import pickle
from typing import Any, Dict, List, Tuple

import pygame

from settings.paths import MAPS_DIR


def get_saved_maps_names() -> List[str]:
    """
        Creates and returns a list with the names of the saved maps in the MAPS_DIR folder.

        Returns:
             List[str]: Names of all saved maps.
    """
    return os.listdir(MAPS_DIR)


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


def deserialize_map_details(editor: Any,
                            map_name: str) -> Dict:
    """
        Deserialize a pickled map and load the attributes into a dict.

        Args:
            editor (any): Current Editor object.
            map_name (str): Name of the map to deserialize.

        Returns:
             Dict: Dictionary containing attributes to update a class instance.
    """
    load_data = get_loaded_map_details(map_name=map_name)

    rows, columns, grid_size_x, grid_size_y, world_data = load_data

    background = pygame.transform.scale(surface=editor.background,
                                        size=(
                                            columns * grid_size_x,
                                            rows * grid_size_y
                                        ))

    dict_updater = {
        "scroll_x": 0,
        "scroll_y": 0,
        "map_name": map_name,
        "temp_map_name": map_name,

        "rows": rows,
        "columns": columns,
        "grid_size_x": grid_size_x,
        "grid_size_y": grid_size_y,

        "world_data": world_data,
        "background": background,

        "is_building": True,
    }

    return dict_updater


def get_loaded_map_details(map_name: str) -> Tuple[int, int, int, int, List[List[int]]]:
    """
        Loads map-dependent variables from a pickle file and deserializes it.

        Args:
            map_name (str): Name of the map to load.

        Returns:
            list[int, int, int, int, list[list[int]]]: A list containing map-dependent variables.
    """
    pickle_in = open(os.path.join(MAPS_DIR, map_name),
                     mode="rb")
    load_data = pickle.load(pickle_in)

    return load_data
