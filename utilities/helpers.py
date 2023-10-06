import os
from typing import List

from settings import PRESET_DIR


def get_preset_dir_names() -> List[str]:
    """
       Get a list of folders in the 'presets' folder.

       Returns:
           List[str]: List of names of folders in 'presets' folder.
       """
    return sorted([f.name for f in os.scandir(PRESET_DIR) if f.is_dir()])


def get_tile_names(current_tab: str) -> List[str]:
    """
       Get a list of tile names for the current tab by
        checking the file name.

       Args:
           current_tab (str): The name of the current tabs tiles.

       Returns:
           List[str]: List of tile names.
       """
    return [f.split(".")[0].split("_")[-1] for f in
            os.listdir(os.path.join(PRESET_DIR, current_tab))
            if f.endswith(".png")]


def get_tile_indexes(current_tab: str) -> List[int]:
    """
       Get a sorted list of tile indexes for the current tabs tiles.

       Args:
           current_tab (str): The name of the current tab.

       Returns:
           List[int]: Sorted list of tile indexes.
       """
    return sorted(
        [int(f.split("_")[0]) for f in os.listdir(os.path.join(PRESET_DIR, current_tab)) if
         f.endswith(".png")])
