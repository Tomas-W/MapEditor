from typing import Tuple, Dict, Any

import pygame

from settings.setup import *


def update_background(editor: Any) -> pygame.Surface:
    return pygame.transform.scale(surface=editor.background_backup,
                                  size=(
                                      (editor.columns * editor.grid_size_x) * editor.scale,
                                      (editor.rows * editor.grid_size_y) * editor.scale
                                  ))


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
        test = editor.world_data[grid_y, grid_x]
    except IndexError:
        return False

    if test == editor.current_object:
        return False

    # Check top and left boundaries
    if grid_x < 0 or grid_y < 0:
        return False

    # Check bottom and right boundaries
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
        if editor.world_data[grid_y, grid_x] == -1:
            return False
    except IndexError:
        return False

    if 0 <= grid_y < editor.world_data.shape[0] and 0 <= grid_x < editor.world_data.shape[1]:
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


def get_enlarged_rect(rect: Tuple[int, int, int, int] | pygame.Rect,
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
