from collections import OrderedDict
from typing import Any, List, Tuple

import numpy as np

from settings.setup import GRID_PREFERENCES_DICT


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


def crop_world_data(world_data: np.ndarray) -> np.ndarray:
    """
        Removes all rows and columns, descending, that contain only -1 values.

        Args:
            world_data (np.ndarray): Nested list containing tile indexes of the map.

        Returns:
            np.ndarray: Cropped version of world_data
    """
    old_rows, old_cols = world_data.shape
    new_rows, new_cols = get_grid_max_row_col(world_data=world_data)

    min_rows = GRID_PREFERENCES_DICT["rows"]["min"]
    min_cols = GRID_PREFERENCES_DICT["columns"]["min"]
    # User tries to crop map smaller than min map size
    if new_rows < min_rows:
        new_rows = min_rows

    if new_cols < min_cols:
        new_cols = min_cols

    world_data = world_data[:new_rows, :]

    new_world_data = world_data[:, :new_cols]

    return new_world_data


def get_grid_max_row_col(world_data: np.ndarray) -> Tuple[int, int]:
    """
        Get the number of rows and columns that can be removed from the end of world_data.
        First value is the number of rows, descending, that contain no -1.
        Second value is the number of columns, descending, that contain no -1

        Args:
            world_data (List[List[int]]: Nested list containing tile indexes of the map.

        Returns:
            Tuple[int, int]: Number of rows and columns that can be safely removed.
    """
    rows_to_keep = world_data.shape[0]
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


def update_world_data_size(editor: Any,
                           name: str,
                           value: int) -> None:
    if name == "rows":
        if value > editor.rows:
            rows = np.full((value - editor.rows, editor.world_data.shape[1]), -1)
            editor.world_data = np.vstack((editor.world_data, rows))
        elif value < editor.rows:
            editor.world_data = editor.world_data[:value, :]

    elif name == "columns":
        if value > editor.columns:
            cols = np.full((editor.world_data.shape[0], value - editor.columns), -1)
            editor.world_data = np.hstack((editor.world_data, cols))
        elif value < editor.columns:
            editor.world_data = editor.world_data[:, :value - editor.columns]