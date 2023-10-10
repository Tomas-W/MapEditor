import pickle
from typing import List, Union, Tuple

import pygame

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


def get_world_data(columns: int,
                   rows: int) -> list[list[int]]:
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


def save_map_details(editor: any) -> None:
    """
        Serializes map-dependent variables into pickle format and
            saves it under the maps name.

        Args:
            editor (any): Current Editor object.
    """
    # noinspection PyProtectedMember
    save_data = [
        editor._rows,
        editor._columns,
        editor._grid_size_x,
        editor._grid_size_y,
        editor.world_data
    ]

    with open(file=os.path.join(MAPS_DIR, editor.map_name),
              mode="wb") as pickle_out:
        pickle.dump(obj=save_data,
                    file=pickle_out)


def get_loaded_map_details(editor: any) -> list[int, int, int, int, list[list[int]]]:
    """
        Loads map-dependent variables from a pickle file and deserializes it.

        Args:
            editor (any): Current Editor object.

        Returns:
            list[int, int, int, int, list[list[int]]]: A list containing map-dependent variables.
    """
    pickle_in = open(f"maps/{editor.map_name}",
                     mode="rb")
    load_data = pickle.load(pickle_in)

    return load_data


def load_map_details(editor: any,
                     map_name: str) -> None:
    """
        Deserialize a pickled map and load the settings into the current Editor.

        Args:
            editor (any): Current Editor object.
            map_name (str): Name of the map to deserialize.

        Returns:
             None
    """
    editor.scroll_x = 0
    editor.scroll_y = 0
    editor.world_data = []
    editor.map_name = map_name
    editor.temp_map_name = editor.map_name

    load_data = get_loaded_map_details(editor=editor)

    editor._rows, editor._columns, editor._grid_size_x, editor._grid_size_y, editor.world_data = load_data

    editor.background = pygame.transform.scale(surface=editor.background,
                                               size=(
                                                   editor._columns * editor._grid_size_x,
                                                   editor._rows * editor._grid_size_y
                                               ))

    editor.is_loading_map = False
    editor.is_building = True


def can_edit_tile(world_data: List[List[int]],
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


def may_place_tile(mouse_pos: Tuple[int, int],
                   background: pygame.Surface,
                   world_object: int,
                   current_object: int) -> bool:
    if world_object != current_object:
        return background.get_rect().collidepoint(mouse_pos)


def may_remove_tile(mouse_pos: Tuple[int, int],
                    background: pygame.Surface,
                    world_object: int,
                    current_object: int) -> bool:
    if world_object == current_object:
        return background.get_rect().collidepoint(mouse_pos)


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


def get_enlarged_rect(rect: Union[tuple[int, int, int, int], pygame.Rect],
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


def get_minimap_dimensions(columns: int,
                           rows: int,
                           grid_x: int,
                           grid_y: int) -> tuple[float, float, float]:
    """
       Get a tuple containing the dimensions of the minimap
       It is scaled to fit the minimap section on the Editor.

       Returns:
           tuple[float, float]: minimap size.
    """
    map_width = columns * grid_x
    map_height = rows * grid_y

    scale_width = RIGHT_MARGIN / map_width
    scale_height = BOTTOM_MARGIN / map_height

    if scale_width < scale_height:
        scale_factor = scale_width
    else:
        scale_factor = scale_height

    return scale_factor, map_width * scale_factor, map_height * scale_factor
