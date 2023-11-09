from typing import List, Tuple

import numpy as np

from settings.panels import *
from settings.paths import *


def get_fresh_world_data(columns: int,
                         rows: int) -> np.array:
    """
        Gets a Numpy 2d array of size columns * rows
            where each item is -1.

        Args:
            columns (int): Number of columns.
            rows (int): Number of rows.

        Returns:
            np.array: Numpy 2d array where each item is -1.
    """
    return np.full((rows, columns), -1)


def get_sorted_tile_names(preset_name: str) -> List[str]:
    """
        Get a list of tile names sorted by their index.

        Args:
            preset_name (str): Name of the preset
    """
    indexes = get_tile_indexes(preset_name=preset_name)
    full_names = os.listdir(os.path.join(PRESETS_DIR, preset_name))
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
        [int(f.split("_")[0]) for f in os.listdir(os.path.join(PRESETS_DIR, preset_name)) if
         f.endswith(".png")])
