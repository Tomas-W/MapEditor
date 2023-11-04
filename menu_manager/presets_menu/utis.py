import os
from typing import List

from settings.panels import PRESETS_MAX_NAME_LENGTH
from settings.paths import PRESETS_DIR


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
