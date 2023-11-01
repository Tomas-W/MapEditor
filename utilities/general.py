import pickle
from collections import OrderedDict
from typing import List, Union, Tuple, Dict, Any
from typing import OrderedDict as OrderedDictType

from settings.panels import *
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


def get_grid_max_row_col(world_data: List[List[int]]) -> Tuple[int, int]:
    """
        Get the number of rows and columns that can be removed from the end of world_data.
        First value is the number of rows, descending, that contain no -1.
        Second value is the number of columns, descending, that contain no -1

        Args:
            world_data (List[List[int]]: Nested list containing tile indexes of the map.

        Returns:
            Tuple[int, int]: Number of rows and columns that can be safely removed.
    """
    rows_to_keep = len(world_data)
    for row in world_data[::-1]:
        if all(index == -1 for index in row):
            rows_to_keep -= 1
        else:
            break

    cols_to_keep = 0
    for row in world_data:
        for i, col in enumerate(row):
            if col != -1:
                cols_to_keep = max(cols_to_keep, i + 1)

    return rows_to_keep, cols_to_keep


def crop_world_data(world_data: List[List[int]]) -> List[List[int]]:
    """
        Removes all rows and columns, descending, that contain only -1 values.

        Args:
            world_data (List[List[int]]): Nested list containing tile indexes of the map.

        Returns:
            List[List[int]]: Cropped version of world_data
    """
    old_rows, old_cols = len(world_data), len(world_data[0])
    new_rows, new_cols = get_grid_max_row_col(world_data=world_data)

    min_rows = GRID_PREFERENCES_DICT["_rows"]["min"]
    min_cols = GRID_PREFERENCES_DICT["_columns"]["min"]
    # User tries to crop map smaller than min map size
    if new_rows < min_rows:
        new_rows = min_rows

    if new_cols < min_cols:
        new_cols = min_cols

    world_data = world_data[:new_rows]

    new_world_data = []
    for row in world_data:
        new_world_data.append(row[:new_cols])

    return new_world_data


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
    """
        Get a list of tile names sorted by their index.

        Args:
            preset_name (str): Name of the preset
    """
    indexes = get_tile_indexes(preset_name=preset_name)
    full_names = os.listdir(os.path.join(PRESET_DIR, preset_name))
    tile_names = []

    for i in range(indexes[0], indexes[-1] + 1):
        for name in full_names:
            if int(name.split("_")[0]) == i:
                tile_names.append(name)

    return tile_names


def limit_string_length(string_list: List[str],
                        max_length: int) -> List[str]:
    """
        Gets a list of strings and limit the length to the given maximum.
        If length is longer, name wil be cut and .. will be appended.

        Args:
            string_list (list[str]): List of strings to check.
            max_length (int): Maximum length allowed for the strings.

        Returns:
            list[str]: List of strings that ar cut off at max_length and have
                .. appended.
    """
    for i, name in enumerate(string_list):
        if len(name) > max_length:
            string_list[i] = name[:max_length + 1] + ".."

    return string_list


def get_tile_names(preset_name: str) -> List[str]:
    """
       Get a list of tile names for the current preset by
        checking the file name.

       Args:
           preset_name (str): Name of the preset.

       Returns:
           List[str]: List of tile names.
       """
    sorted_tile_file_names = get_sorted_tile_names(preset_name=preset_name)

    tile_names = [f.split(".")[0].split("_")[-1] for f in
                  sorted_tile_file_names
                  if f.endswith(".png")]

    return limit_string_length(string_list=tile_names,
                               max_length=MAX_TILE_NAME_LENGTH)


def get_tile_indexes(preset_name: str) -> List[int]:
    """
       Get a sorted list of tile indexes for the preset.

       Args:
           preset_name (str): Name of the preset.

       Returns:
           List[int]: Sorted list of tile indexes.
       """
    return sorted(
        [int(f.split("_")[0]) for f in os.listdir(os.path.join(PRESET_DIR, preset_name)) if
         f.endswith(".png")])


def get_saved_map_names() -> List[str]:
    """
        Get a list with the name of the saved maps in the maps folder.

        Returns:
             List[str]: Names of al saved maps.
    """
    return os.listdir(MAPS_DIR)


def get_empty_list() -> List:
    """
        Get an empty list.

        Returns:
            List: An empty list.
    """
    return []


def get_empty_ordered_dict() -> OrderedDictType[str, int]:
    """
        Get an empty OrderedDict.

        Returns:
            OrderedDict: An empty OrderedDict.
    """
    return OrderedDict()


def is_new_value_allowed(name: str,
                         value: int) -> bool:
    """
        Checks whether a preference value falls within a bound set in
            grid_preference_dict and returns True if so, else False.

        Args:
            name (str): Name of a preference.
            value (int): Value to check.

        Returns:
            bool: True if value is within bounds, else False.
    """
    dict_ = GRID_PREFERENCES_DICT
    return dict_[name]["min"] <= value <= dict_[name]["max"]
