import pickle
from collections import OrderedDict
from typing import List, Union, Tuple, Dict, Any
from typing import OrderedDict as OrderedDictType

from settings.paths import *
from settings.minimap import *


def is_pickled(file_path: str) -> bool:
    """
        Check if a file is pickled.

        Args:
            file_path (str): Path to the file.

        Returns:
            bool: True if the file is pickled, False otherwise.
        """
    try:
        with open(file_path, "rb") as file:
            pickle.load(file)
        return True

    except (pickle.UnpicklingError, EOFError, FileNotFoundError):
        return False


def get_fresh_world_data(columns: int,
                         rows: int) -> List[List[int]]:
    """
        Gets a nested list containing object indexes or -1.
        Size depends on chosen number of columns and rows.

        Args:
            columns (int): Number of columns.
            rows (int): Number of rows.

        Returns:
            List[List[int]]: Nested list containing object indexes.
    """
    return [[-1] * columns for _ in range(rows)]


def can_place_tile(world_data: List[List[int]],
                   current_index: int,
                   grid_x: int,
                   grid_y: int) -> bool:
    """
        Checks if the current mouse position is within the maps boundaries.
        Mouse position is expressed in grid units, not actual coordinates.
        Returns True if it is, else False.

        Args:
            current_index (int): Index of the selected tile.
            world_data (List[List[int]]: Nested list containing all map objects.
            grid_x (int): Current mouse x position expressed in grid units.
            grid_y (int): Current mouse y position expressed in grid units.

        Returns:
            True if x and y are in world data, else False.
    """
    if 0 <= grid_y < len(world_data) and 0 <= grid_x < len(world_data[grid_y]):
        if world_data[grid_y][grid_x] != current_index:
            return True
    else:
        return False


def can_remove_tile(world_data: List[List[int]],
                    current_index: int,
                    grid_x: int,
                    grid_y: int) -> bool:
    """
        Checks if the current mouse position is within the maps boundaries.
        Mouse position is expressed in grid units, not actual coordinates.
        Returns True if it is, else False.

        Args:
            current_index (int): Index of the selected tile.
            world_data (List[List[int]]: Nested list containing all map objects.
            grid_x (int): Current mouse x position expressed in grid units.
            grid_y (int): Current mouse y position expressed in grid units.

        Returns:
            True if x and y are in world data, else False.
    """
    if 0 <= grid_y < len(world_data) and 0 <= grid_x < len(world_data[grid_y]):
        if world_data[grid_y][grid_x] != -1:
            return True
    else:
        return False


def get_preset_dir_names() -> List[str]:
    """
       Get a list of folders in the 'presets' folder.

       Returns:
           List[str]: List of names of folders in 'presets' folder.
       """
    return sorted([f.name for f in os.scandir(PRESET_DIR) if f.is_dir()])


def get_shortened_dir_names() -> List[str]:
    """
       Get a list of folders in the 'presets' folder and returns a list where
        the names have been capped to 15 and have trailing '..'

       Returns:
           List[str]: List of names of shortened folders in 'presets' folder.
       """
    names = get_preset_dir_names()

    for i, name in enumerate(names):
        if len(name) > 15:
            names[i] = name[:14] + ".."

    return names


def get_sorted_tile_names(preset_name: str) -> List[str]:
    indexes = get_tile_indexes(preset_name=preset_name)
    full_names = os.listdir(os.path.join(PRESET_DIR, preset_name))
    tile_names = []

    for i in range(indexes[0], indexes[-1] + 1):
        for name in full_names:
            if int(name.split("_")[0]) == i:
                tile_names.append(name)

    return tile_names


def get_tile_names(preset_name: str) -> List[str]:
    """
       Get a list of tile names for the current preset by
        checking the file name.

       Args:
           preset_name (str): Name of the current preset.

       Returns:
           List[str]: List of tile names.
       """
    tile_names = get_sorted_tile_names(preset_name=preset_name)

    return [f.split(".")[0].split("_")[-1] for f in
            tile_names
            if f.endswith(".png")]


def get_tile_indexes(preset_name: str) -> List[int]:
    """
       Get a sorted list of tile indexes for the current preset.

       Args:
           preset_name (str): Name of the preset.

       Returns:
           List[int]: Sorted list of tile indexes.
       """
    return sorted(
        [int(f.split("_")[0]) for f in os.listdir(os.path.join(PRESET_DIR, preset_name)) if
         f.endswith(".png")])


def get_saved_map_names() -> List[str]:
    return os.listdir(MAPS_DIR)


def get_empty_list() -> List:
    return []


def get_empty_ordered_dict() -> OrderedDictType[str, int]:
    return OrderedDict()


def is_new_value_allowed(name: str,
                         value: int) -> bool:
    dict_ = GRID_PREFERENCES_DICT
    return dict_[name]["min"] <= value <= dict_[name]["max"]
