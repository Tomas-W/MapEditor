import pickle
from collections import OrderedDict
from typing import List, Union, Tuple, Dict, Any

import pygame

from settings.paths import *
from settings.setup import *


def save_map_details(editor: any) -> None:
    """
        Serializes map-dependent variables into pickle format and
            saves it under the maps name.

        Args:
            editor (any): Current Editor object.
    """
    # noinspection PyProtectedMember
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


def update_class_dict(cls: any,
                      attributes: dict):
    """
        Gets a dict containing instance attributes and
            checks if exist within the class.
        If all attributes exit, update __dict__,
            else raise a KeyError.

        Args:
            cls (any): A Class to update its attributes.
            attributes (Dict): A dict containing attributes to update.
    """
    cls_dict = cls.__dict__
    approved_dict = {}
    for key, val in attributes.items():
        if key in cls_dict:
            approved_dict[key] = val
        else:
            raise KeyError(f"'{str(cls)}' accepts no keyword '{key}'.")

    cls.__dict__.update(approved_dict)


def deserialize_map_details(editor: any,
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


def can_place_tile(editor: any,
                   grid_x: int,
                   grid_y: int) -> bool:
    """
        Checks if the current mouse position is within the maps boundaries.
        Mouse position is expressed in grid units, not actual coordinates.
        Returns True if it is, else False.
        No tiles can be placed outside of grid, only removed.

        Args:
            editor (any): Current Editor instance.
            grid_x (int): Current mouse x position expressed in grid units.
            grid_y (int): Current mouse y position expressed in grid units.

        Returns:
            True if x and y are in world data, else False.
    """
    # Check if object is new or already placed
    try:
        test = editor.world_data[grid_y][grid_x]
    except IndexError:
        return False

    if test == editor.current_object:
        return False
    # Check top and left boundaries
    if grid_x < 0 or grid_y < 0:
        return False

    # Check bottom and right boundaries
    # noinspection PyProtectedMember
    if grid_x >= editor.columns or grid_y >= editor.rows:
        return False

    return True


def can_remove_tile(editor: any,
                    grid_x: int,
                    grid_y: int) -> bool:
    """
        Checks if the current mouse position is within the maps boundaries.
        Mouse position is expressed in grid units, not actual coordinates.
        Returns True if it is, else False.
        No tiles can be placed outside of grid, only removed.

        Args:
            editor (any): Current Editor instance.
            grid_x (int): Current mouse x position expressed in grid units.
            grid_y (int): Current mouse y position expressed in grid units.

        Returns:
            True if x and y are in world data, else False.
    """
    # Check if object is new or already placed
    try:
        if editor.world_data[grid_y][grid_x] == -1:
            return False
    except IndexError:
        return False

    if 0 <= grid_y < len(editor.world_data) and 0 <= grid_x < len(
            editor.world_data[grid_y]):
        return True

    return False


def get_minimap_dimensions(editor: any) -> Tuple[float, float, float]:
    """
       Get a tuple containing the dimensions of the minimap
       It is scaled to fit the minimap section on the Editor.

       Returns:
           tuple[float, float]: minimap size.
    """
    # noinspection PyProtectedMember
    map_width = editor.columns * editor.grid_size_x
    # noinspection PyProtectedMember
    map_height = editor.rows * editor.grid_size_y

    scale_width = RIGHT_MARGIN / map_width
    scale_height = BOTTOM_MARGIN / map_height

    if scale_width < scale_height:
        scale_factor = scale_width
    else:
        scale_factor = scale_height

    return scale_factor, map_width * scale_factor, map_height * scale_factor


def get_enlarged_rect(rect: Union[Tuple[int, int, int, int], pygame.Rect],
                      pixels: int) -> pygame.Rect:
    """
       Get a pygame.Rect object enlarged by x pixels on each side.

       Args:
           rect (Union[tuple[int, int, int, int], pygame.Rect): A pygame.Rect object or a tuple.
           pixels (int): With in pixels to add to all four sides of the Rect.

       Returns:
           pygame.Rect: pygame.Rect object.
    """
    larger_rect = pygame.Rect(
        rect[0] - pixels,
        rect[1] - pixels,
        rect[2] + 2 * pixels,
        rect[3] + 2 * pixels
    )

    return larger_rect


def update_background(editor: any) -> pygame.Surface:
    return pygame.transform.scale(surface=editor.background,
                                  size=(
                                      editor.columns * editor.grid_size_x,
                                      editor.rows * editor.grid_size_y
                                  ))


def update_world_data_size(editor: any) -> None:
    rows_to_add = editor.rows - len(editor.world_data)
    cols_to_add = editor.columns - len(editor.world_data[0])

    for row in editor.world_data:
        for x in range(cols_to_add):
            row.append(-1)

    for x in range(rows_to_add):
        editor.world_data.append([-1 for y in range(editor.columns)])

