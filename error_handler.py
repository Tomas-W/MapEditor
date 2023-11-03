from dataclasses import dataclass, field
from typing import List, Union, Dict, OrderedDict, Tuple, Self

import pygame

import utilities.drawing as text

from settings.setup import *
from settings.paths import *

from settings.canvas import *
from settings.errors import *
from settings.panels import *
from settings.menus import *
from settings.minimap import *

import utilities.drawing as drawing
import utilities.fonts as fonts
import utilities.general as general
import utilities.sprites as sprites
import utilities.helpers as helpers


class ErrorHandler:

    def __init__(self,
                 editor: any) -> Self:
        self.editor = editor

        self.error_messages: Dict[str, str] = {}

        self.row_errors = None
        self.col_errors = None

        self.set_preset_error()
        self.set_tile_error()

    def reset_errors(self) -> None:
        """
            Resets all error messages to None.

            Returns:
                None.
        """
        self.error_messages: List[str] = []

        self.row_errors = None
        self.col_errors = None

        self.set_preset_error()
        self.set_tile_error()

    def set_preset_error(self) -> None:
        """
            Sets preset error message if more presets are loaded than can be drawn.
            If no error, message is set to None.

            Returns:
            None.
        """
        if len(self.editor.preset_names) > MAX_NR_PRESETS:
            self.error_messages["preset"] = MAX_PRESETS_ERROR

        else:
            self.error_messages["preset"] = None

    def set_tile_error(self) -> None:
        """
            Sets tile error message if more tiles are loaded than can be drawn.
            If no error, message is set to None.

            Returns:
            None.
        """
        if len(self.editor.tile_names) > MAX_NR_TILES:
            self.error_messages["tile"] = f"{MAX_TILES_ERROR} {len(self.editor.tile_names)} in a preset folder."

        else:
            self.error_messages["tile"] = None

    def set_out_of_bounds_error(self):
        """
            Sets out_of_bounds error message if tiles are places outside the current grid.
            If no error, message is set to None.

            Returns:
            None.
        """
        row_errors = 0
        col_errors = 0
        world_data: List[List[int]] = self.editor.world_data
        # check rows
        if len(world_data) > self.editor.rows:
            # more world data rows than grid rows
            for row in world_data[self.editor.rows:]:
                for tile in row:
                    if tile != -1:
                        row_errors += 1
        if len(world_data[0]) > self.editor.columns:
            col_iterator = range(self.editor.columns, len(world_data[0]))
            for row in world_data:
                for i in col_iterator:
                    if row[i] != -1:
                        col_errors += 1

        self.row_errors = row_errors
        self.col_errors = col_errors
        if row_errors > 0 or col_errors > 0:
            self.error_messages["grid"] = OUT_OF_BOUNDS_ERROR

        else:
            self.error_messages["grid"] = None

    def display_error_messages(self) -> None:
        """
            Loops over self.error_messages and displays them in order on the screen
                if message is not None.

            Returns:
                 None.
        """
        error_messages = [val for (key, val) in self.error_messages.items() if val is not None]

        for i, error in enumerate(error_messages):
            text.draw(
                screen=self.editor.screen,
                text=error,
                font=fonts.error_font,
                color=ERROR_COLOR,
                x_pos=ERROR_X,
                y_pos=ERROR_Y + i * ERROR_Y_SPACING
            )
