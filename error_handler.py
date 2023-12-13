from typing import Dict, Self

import numpy as np

import utilities.render_text as text
import utilities.fonts as fonts
from settings.errors import *

from settings.panels import *


class ErrorHandler:

    def __init__(self,
                 editor: any) -> Self:
        self.editor = editor

        self.ERROR_COLOR = ERROR_COLOR
        self.ERROR_X = ERROR_X
        self.ERROR_Y = ERROR_Y
        self.ERROR_Y_SPACING = ERROR_Y_SPACING

        self.error_messages: Dict[str, str] = {}

        self.OUT_OF_BOUNDS_ERROR = f"Map cannot be saved." \
                                   f" Tiles found outside of grid." \
                                   f" Change map size or remove tiles."

        self.MAX_NR_PRESETS = MAX_NR_PRESETS
        self.MAX_PRESETS_ERROR = f"Not all presets loaded." \
                                 f" Editor can only hold {MAX_NR_PRESETS} presets."

        self.MAX_NR_TILES = MAX_NR_TILES
        self.MAX_TILES_ERROR = f"Not all tiles are loaded." \
                               f" Editor can only hold {MAX_NR_TILES} tiles but found "

    def set_preset_error(self) -> None:
        """
            Sets preset error message if more presets are loaded than can be drawn.
            If no error, message is set to None.

            Returns:
            None.
        """
        if len(self.editor.preset_names) > self.MAX_NR_PRESETS:
            self.error_messages["preset"] = self.MAX_PRESETS_ERROR

        else:
            self.error_messages["preset"] = None

    def set_tile_error(self) -> None:
        """
            Sets tile error message if more tiles are loaded than can be drawn.
            If no error, message is set to None.

            Returns:
            None.
        """
        if len(self.editor.tile_names) > self.MAX_NR_TILES:
            self.error_messages["tile"] = f"{self.MAX_TILES_ERROR} {len(self.editor.tile_names)} in current preset folder."

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
        world_data: np.ndarray = self.editor.world_data
        # check rows
        if world_data.shape[0] > self.editor.rows:
            # more world data rows than grid rows
            for row in world_data[self.editor.rows:]:
                for tile in row:
                    if tile != -1:
                        row_errors += 1
        if world_data.shape[1] > self.editor.columns:
            col_iterator = range(self.editor.columns, world_data.shape[0])
            for row in world_data:
                for i in col_iterator:
                    if row[i] != -1:
                        col_errors += 1

        if row_errors > 0 or col_errors > 0:
            self.error_messages["grid"] = self.OUT_OF_BOUNDS_ERROR

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
            text.position(
                screen=self.editor.screen,
                text=error,
                font=fonts.error_font,
                color=self.ERROR_COLOR,
                x_pos=self.ERROR_X,
                y_pos=self.ERROR_Y + i * self.ERROR_Y_SPACING
            )
