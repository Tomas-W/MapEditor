from collections import OrderedDict
from typing import List, Any

from settings.panels import *
from settings.paths import *


def get_preferences_dict(editor: Any) -> OrderedDict[str, int]:
    """
        Creates and returns an OrderedDict containing the following Editor attributes and values:
            rows
            columns
            grid_size_x
            grid_size_y

        Args:
            editor (Any): Current Editor instance.

        Returns:
            OrderedDict[str, int]: An OrderedDict containing Editor preferences attributes.

    """
    preferences_dict: OrderedDict[str, int] = OrderedDict([
        ("rows", editor.rows),
        ("columns", editor.columns),
        ("grid_size_x", editor.grid_size_x),
        ("grid_size_y", editor.grid_size_y)])
    return preferences_dict


def get_saved_maps_names() -> List[str]:
    """
        Creates and returns a list with the names of the saved maps in the MAPS_DIR folder.

        Returns:
             List[str]: Names of all saved maps.
    """
    return os.listdir(MAPS_DIR)


def get_presets_dir_names() -> List[str]:
    """
       Creates and returns a list of folders in the PRESETS_DIR folder.

       Returns:
           List[str]: List of names of folders in the PRESETS_DIR folder.
       """
    return sorted([f.name for f in os.scandir(PRESETS_DIR) if f.is_dir()])


def get_shortened_presets_dir_names(names: List[str]) -> List[str]:
    """
        Gets a list with names of presets and returns a new list that
            caps each names length to PRESETS_MAX_NAME_LENGTH and
            returns a list of folders in the PRESETS_DIR folder and returns a list where
        the names have been capped to 15 characters and have a trailing '..'

       Returns:
           List[str]: List of shortened names of folders in the PRESETS_DIR folder.
       """
    for i, name in enumerate(names):
        if len(name) > PRESETS_MAX_NAME_LENGTH:
            names[i] = name[:PRESETS_MAX_NAME_LENGTH - 1] + ".."

    return names
