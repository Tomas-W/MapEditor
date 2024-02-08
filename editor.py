from typing import Self, Tuple

import numpy as np
import pygame

pygame.init()

from settings.minimap import *
from settings.presets import *
from settings.errors import *

screen = pygame.display.set_mode((SCREEN_WIDTH + RIGHT_MARGIN,
                                  SCREEN_HEIGHT + BOTTOM_MARGIN))
pygame.display.message_box()

from menu_manager.menu_controller import MenuController
from event_handler import EventHandler
from error_handler import ErrorHandler

from settings.buttons import *

import utilities.buttons as buttons
import utilities.fonts as fonts
import utilities.general as general
import utilities.helpers as helpers
import utilities.sprites as sprites
import utilities.render_text as render_text


class Editor:
    def __init__(self) -> Self:
        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.screen: pygame.display = screen
        self.events: pygame.event = pygame.event.get()
        self.keys: pygame.key = pygame.key.get_pressed()
        self.mouse_pos = pygame.mouse.get_pos()

        self.map_name: str = "New map"
        self.temp_map_name: str = self.map_name
        # self.sky = sprites.sky_img
        self.backgrounds = helpers.get_scaled_backgrounds(background=sprites.background_img)

        self.columns = 500
        self.max_visible_cols = np.ceil(SCREEN_WIDTH / GRID_SIZE_X)
        self.start_col = 0
        self.stop_col = self.columns
        self.rows = 500
        self.max_visible_rows = np.ceil(SCREEN_HEIGHT / GRID_SIZE_Y)
        self.start_row = 0
        self.stop_row = self.rows

        self.grid_size_x = GRID_SIZE_X
        self.grid_size_y = GRID_SIZE_Y
        self.world_data: np.ndarray = general.get_fresh_world_data(
            columns=self.columns,
            rows=self.rows
        )

        # Scrolling
        self.may_scroll_to: dict[str, bool] = {
            "left": True,
            "right": True,
            "up": True,
            "down": True
        }
        self.scroll_left = False
        self.scroll_right = False
        self.scroll_up = False
        self.scroll_down = False
        self.scroll_x = 0
        self.scroll_y = 0
        self.scroll_speed = BASE_SCROLL_SPEED
        self.base_scroll_speed = BASE_SCROLL_SPEED
        self.max_scroll_speed = MAX_SCROLL_SPEED

        # Events
        self.event_handler = EventHandler(editor=self)

        # Menus
        self.menu_controller = MenuController(editor=self)

        # Quick Menu buttons
        self.undo_button = buttons.get_utility_button(editor=self,
                                                      **UNDO_BTN)
        self.redo_button = buttons.get_utility_button(editor=self,
                                                      **REDO_BTN)
        self.grid_button = buttons.get_utility_button(editor=self,
                                                      **GRID_BTN)
        self.zoom_in_button = buttons.get_utility_button(editor=self,
                                                         **ZOOM_IN_BTN)
        self.zoom_out_button = buttons.get_utility_button(editor=self,
                                                          **ZOOM_OUT_BTN)

        # Preferences
        self.selected_preference_name = "rows"
        self.selected_preference_value = self.rows
        self.selected_preference_value_change = self.rows

        # Presets
        self.preset_names: list[str] = self.menu_controller.presets_renderer.preset_names
        self.shortened_preset_names: list[
            str] = self.menu_controller.presets_renderer.shortened_preset_names
        self.current_preset: str = self.preset_names[0]

        # Tiles
        self.level_objects: dict[int, pygame.Surface] = sprites.get_all_level_objects()
        self.level_objects_backup: dict[int, pygame.Surface] = sprites.get_all_level_objects()
        self.tile_list: list[pygame.Surface] = sprites.get_preset_sprites(
            preset_name=self.current_preset
        )
        self.tile_names: list[str] = general.get_tile_names(
            preset_name=self.current_preset
        )
        self.tile_indexes: list[int] = general.get_tile_indexes(
            preset_name=self.current_preset
        )
        self.tile_buttons: list[buttons.TileButton] = buttons.get_tile_buttons(
            preset_name=self.current_preset,
            editor=self
        )
        self.current_tile: int = 0
        self.current_object: int = self.tile_indexes[0]
        self.tile_undo_tracker: list[Tuple[tuple, int]] = []
        self.tile_redo_tracker: list[Tuple[tuple, int]] = []

        # States
        self.is_running = True
        self.is_building = True

        self.is_displaying_presets = False

        # Quick menu
        self.show_grid = True
        self.scale = 1.0
        self.center_col = self.columns // 2
        self.center_row = self.rows // 2

        # Errors
        self.error_handler = ErrorHandler(editor=self)

        self.test = 100

    def __str__(self) -> str:
        return f"Editing: {self.map_name}"

    def set_scroll_restrictions(self) -> None:
        """
            Stops user from scrolling off the grid completely by disallowing to scroll
                when MIN_VISIBLE_ROWS/COLS is reached.
        """
        # Out of bounds upwards after zooming
        if self.stop_row < MIN_VISIBLE_COLS:
            self.scroll_y -= (abs(self.stop_row) + 3) * self.grid_size_y

        # Out of bounds downwards after zooming
        elif self.start_row > self.rows - MIN_VISIBLE_ROWS:
            self.scroll_y += (self.start_row - self.rows + 3) * self.grid_size_x

        # Out of bounds left after zooming
        if self.stop_col < MIN_VISIBLE_COLS:
            self.scroll_x -= (abs(self.stop_col) + 3) * self.grid_size_x

        # Out of bounds right after zooming
        elif self.start_col > self.columns - MIN_VISIBLE_ROWS:
            self.scroll_x += (self.start_col - self.rows + 3) * self.grid_size_x

        # Check if grid still in bounds
        if self.start_col >= self.columns - MIN_VISIBLE_COLS:
            self.may_scroll_to["right"] = False
        else:
            self.may_scroll_to["right"] = True

        if self.stop_col <= MIN_VISIBLE_COLS:
            self.may_scroll_to["left"] = False
        else:
            self.may_scroll_to["left"] = True

        if self.start_row >= self.rows - MIN_VISIBLE_ROWS:
            self.may_scroll_to["down"] = False
        else:
            self.may_scroll_to["down"] = True

        if self.stop_row <= MIN_VISIBLE_ROWS:
            self.may_scroll_to["up"] = False
        else:
            self.may_scroll_to["up"] = True

    def scroll_map(self) -> None:
        """
            Scrolls the map based on scroll speed and restrictions.
        """

        if self.scroll_left and self.may_scroll_to["left"]:
            self.scroll_x += self.scroll_speed

        if self.scroll_right and self.may_scroll_to["right"]:
            self.scroll_x -= self.scroll_speed

        if self.scroll_up and self.may_scroll_to["up"]:
            self.scroll_y += self.scroll_speed

        if self.scroll_down and self.may_scroll_to["down"]:
            self.scroll_y -= self.scroll_speed

    def set_visible_cols_rows(self) -> None:
        """
            Sets the number of columns and rows that can be seen by the user by
                checking the screen size, grid size and scale.
            Is called by zoom in- and out functions.
        """
        self.max_visible_cols = int(np.ceil(SCREEN_WIDTH / (self.grid_size_x * self.scale)))
        self.max_visible_rows = int(np.ceil(SCREEN_HEIGHT / (self.grid_size_y * self.scale)))

    def set_col_start_stop(self) -> None:
        """
            Sets first and last column checking scroll_x, grid_size_x,
                max_visible_cols and scale.
            Is called by zoom in- and out functions.
        """
        self.start_col = int(-self.scroll_x / self.grid_size_x) if self.scroll_x < 0 else 0
        self.stop_col = min(int(np.ceil(
            self.max_visible_cols - (self.scroll_x * self.scale) / (
                        self.grid_size_x * self.scale))), self.columns)

    def set_row_start_stop(self) -> None:
        """
            Sets first and last row by checking scroll_y, grid_size_y,
                max_visible_rows and scale.
            Is called by run and zoom in- and out functions.
        """
        self.start_row = int(-self.scroll_y / self.grid_size_y) if self.scroll_y < 0 else 0
        self.stop_row = min(int(np.ceil(
            self.max_visible_rows - (self.scroll_y * self.scale) / (
                        self.grid_size_y * self.scale))), self.rows)

    def set_center_col_row(self) -> None:
        """
            Sets center column and row in the current users view by checking
                start and stop column and row.
            Is called by zoom in- and out functions.
        """
        self.center_col = (self.start_col + self.stop_col) // 2
        self.center_row = (self.start_row + self.stop_row) // 2

    def set_new_scroll_values(self,
                              old_mid_col: int,
                              old_mid_row: int) -> None:
        """
            Sets new scroll_x and scroll_y values after user uses zoom function to
                keep the same tile in the center of the screen.
            Is called by zoom in- and out functions.
        """
        new_mid_col = (self.stop_col - self.start_col) / 2
        new_mid_row = (self.stop_row - self.start_row) / 2

        self.scroll_x += (new_mid_col - old_mid_col) * (self.grid_size_x * self.scale)
        self.scroll_y += (new_mid_row - old_mid_row) * (self.grid_size_y * self.scale)

    def scale_level_objects(self) -> None:
        """
            Scales all level objects by the Editor's scale.
            Is called by zoom in- and out functions.
        """
        for (index, tile) in self.level_objects.items():
            self.level_objects[index] = pygame.transform.scale(self.level_objects_backup[index],
                                                               (int(self.scale *
                                                                    self.level_objects_backup[
                                                                        index].get_width()),
                                                                int(self.scale *
                                                                    self.level_objects_backup[
                                                                        index].get_height())
                                                                ))

    def zoom_in(self) -> None:
        """
            Scales up all map features by increasing the scale by 0.2 up to
                a set maximum.
        """

        if self.scale < 1.6:
            old_mid_col = (self.stop_col - self.start_col) / 2
            old_mid_row = (self.stop_row - self.start_row) / 2

            self.scale = round(self.scale + 0.2, 1)

            self.set_visible_cols_rows()
            self.set_col_start_stop()
            self.set_row_start_stop()

            self.set_new_scroll_values(old_mid_col=old_mid_col,
                                       old_mid_row=old_mid_row)

            self.scale_level_objects()

    def zoom_out(self) -> None:
        """
            Scales down all map features by decreasing the scale by 0.2 down to
                a set minimum.
        """
        if self.scale > 0.4:
            old_mid_col = (self.stop_col - self.start_col) / 2
            old_mid_row = (self.stop_row - self.start_row) / 2

            self.scale = round(self.scale - 0.2, 1)

            self.set_visible_cols_rows()
            self.set_col_start_stop()
            self.set_row_start_stop()

            self.set_new_scroll_values(old_mid_col=old_mid_col,
                                       old_mid_row=old_mid_row)

            self.scale_level_objects()

    def wipe_map(self):
        """
            Sets all world_data array items to -1.
        """
        self.world_data: np.ndarray = general.get_fresh_world_data(
            columns=self.columns,
            rows=self.rows
        )

    def reload_editor(self) -> None:
        """
            Sets all Editor attributes to their default state to mimic a restart.
        """
        self.map_name: str = "New map"
        self.temp_map_name: str = self.map_name

        self.columns = COLUMNS
        self.max_visible_cols = np.ceil(SCREEN_WIDTH / GRID_SIZE_X)
        self.start_col = 0
        self.stop_col = self.columns
        self.rows = ROWS
        self.max_visible_rows = np.ceil(SCREEN_HEIGHT / GRID_SIZE_Y)
        self.start_row = 0
        self.stop_row = self.rows

        self.grid_size_x = GRID_SIZE_X
        self.grid_size_y = GRID_SIZE_Y
        self.world_data: np.ndarray = general.get_fresh_world_data(
            columns=self.columns,
            rows=self.rows
        )

        # Scrolling
        self.may_scroll_to: dict[str, bool] = {
            "left": True,
            "right": True,
            "up": True,
            "down": True
        }
        self.scroll_left = False
        self.scroll_right = False
        self.scroll_up = False
        self.scroll_down = False
        self.scroll_x = 0
        self.scroll_y = 0
        self.scroll_speed = BASE_SCROLL_SPEED
        self.base_scroll_speed = BASE_SCROLL_SPEED
        self.max_scroll_speed = MAX_SCROLL_SPEED

        # Menus
        self.menu_controller = MenuController(editor=self)  # to allow adding new presets

        # Preferences
        self.selected_preference_name = "rows"
        self.selected_preference_value = self.rows
        self.selected_preference_value_change = self.rows

        # Presets
        self.preset_names: list[str] = self.menu_controller.presets_renderer.preset_names
        self.shortened_preset_names: list[
            str] = self.menu_controller.presets_renderer.shortened_preset_names
        self.current_preset: str = self.preset_names[0]

        # Tiles
        self.level_objects: dict[int, pygame.Surface] = sprites.get_all_level_objects()
        self.tile_list: list[pygame.Surface] = sprites.get_preset_sprites(
            preset_name=self.current_preset
        )
        self.tile_names: list[str] = general.get_tile_names(
            preset_name=self.current_preset
        )
        self.tile_indexes: list[int] = general.get_tile_indexes(
            preset_name=self.current_preset
        )
        self.tile_buttons: list[buttons.TileButton] = buttons.get_tile_buttons(
            preset_name=self.current_preset,
            editor=self
        )
        self.current_tile: int = 0
        self.current_object: int = self.tile_indexes[0]
        self.tile_undo_tracker: list[Tuple[tuple, int]] = []
        self.tile_redo_tracker: list[Tuple[tuple, int]] = []

        # States
        self.is_running = True
        self.is_building = True

        self.is_displaying_presets = False

        # Quick menu
        self.show_grid = True
        self.scale = 1
        self.center_col = self.columns // 2
        self.center_row = self.rows // 2

    def draw_background(self,
                        scroll_x: int,
                        scroll_y: int) -> None:
        """
            Blits the background image to the screen.

            Args:
                scroll_x (int): X coordinate of background.topleft.
                scroll_y (int): Y coordinate of background.topleft.
        """
        self.screen.blit(self.backgrounds[str(self.scale)],
                         (scroll_x * self.scale, scroll_y * self.scale))

    def draw_grid(self) -> None:
        """
            Draws horizontal and vertical lines on screen according to
                grid size settings.
        """
        # Horizontal lines
        for x in range(self.rows + 1):
            pygame.draw.line(surface=self.screen,
                             color=GRID_LINE_COLOR,
                             start_pos=(
                                 0,
                                 int((x * self.grid_size_y + self.scroll_y) * self.scale)),
                             end_pos=(
                                 SCREEN_WIDTH,
                                 int((x * self.grid_size_y + self.scroll_y) * self.scale)))

        # Vertical lines
        for y in range(self.columns + 1):
            pygame.draw.line(surface=self.screen,
                             color=GRID_LINE_COLOR,
                             start_pos=(
                                 int((y * self.grid_size_x + self.scroll_x) * self.scale), 0),
                             end_pos=(int((y * self.grid_size_x + self.scroll_x) * self.scale),
                                      SCREEN_HEIGHT))

    def draw_map(self) -> None:
        """
            Draws all level objects to the screen.
            Checks current viewport and only blits objects that are contained within.
        """
        # Get cols and rows in view
        subset = self.world_data[self.start_row:self.stop_row + 1, self.start_col:self.stop_col + 1]

        blit_list = []
        for (y, x), tile in np.ndenumerate(subset):
            if tile > -1:
                x_pos = ((x + self.start_col) * self.grid_size_x + self.scroll_x) * self.scale
                y_pos = ((y + self.start_row) * self.grid_size_y + self.scroll_y) * self.scale

                blit_list.append((self.level_objects[tile], (x_pos, y_pos)))

        self.screen.blits(blit_list)

    def draw_right_panel(self) -> None:
        """
            Blits right panel to the screen according to
                panel settings.
        """
        pygame.draw.rect(surface=self.screen,
                         color=RIGHT_PANEL_COLOR,
                         rect=(SCREEN_WIDTH,
                               0,
                               RIGHT_MARGIN,
                               SCREEN_HEIGHT),
                         width=0)

    def draw_and_select_tile(self) -> None:
        """
            Draws all tiles on side panel and stores currently selected tile.
            Limits the number of tiles to MAX_NR_TILES.
            ErrorHandler will display a message if not all tiles can be shown.
        """
        for button_count, button in enumerate(self.tile_buttons[:MAX_NR_TILES]):
            if button.draw():
                self.current_tile = button_count
                self.current_object = button.tile_index

    def draw_tile_labels(self) -> None:
        """
            Draws label above the tile on the side panel.
        """
        for tile, label in zip(self.tile_buttons[:MAX_NR_TILES], self.tile_names[:MAX_NR_TILES]):
            render_text.position(screen=self.screen,
                                 text=str(label),
                                 font=fonts.label_font,
                                 color=TILE_LABEL_COLOR,
                                 x_pos=tile.rect.topleft[0],
                                 y_pos=tile.rect.topleft[1] - TILE_LABEL_Y_OFFSET)

    def highlight_selected_tile(self) -> None:
        """
            Draws highlight effect on the selected tile.
        """
        pygame.draw.rect(
            surface=self.screen,
            color=TILE_HIGHLIGHT_COLOR,
            rect=(self.tile_buttons[self.current_tile].rect.topleft[0] + TILE_HIGHLIGHT_LEFT_OFFSET,
                  self.tile_buttons[self.current_tile].rect.topleft[1] + TILE_HIGHLIGHT_LEFT_OFFSET,
                  TILE_SIZE_X + TILE_HIGHLIGHT_RIGHT_OFFSET,
                  TILE_SIZE_Y + TILE_HIGHLIGHT_RIGHT_OFFSET),
            width=TILE_HIGHLIGHT_WIDTH)

    def update_undo_tracker(self,
                            coords: Tuple[int, int],
                            tile_index: int) -> None:
        """
            Appends the tile index of the previously placed tile to the undo tracker.
            If number of stored tiles exceeds MAX_TILE_TRACKING,
                the first item in the array is removed.

            Args:
                coords (Tuple[int, int]: Grid coordinates of the tile.
                tile_index (int): The tile index of the 'old' tile.

            Returns:
                None
        """
        if len(self.tile_undo_tracker) > MAX_TILE_TRACKING:
            self.tile_undo_tracker.pop(0)

        self.tile_undo_tracker.append((coords, tile_index))

    def update_redo_tracker(self,
                            coords: int,
                            tile_index: int) -> None:
        """
            Appends the tile index of the previously 'un-done' tile to the redo tracker.
            If number of stored tiles exceeds MAX_TILE_TRACKING,
                the first item in the array is removed.

            Args:
                coords (Tuple[int, int]: Grid coordinates of tile.
                tile_index (int): The tile index of the 'un-done' tile.

            Returns:
                None
        """
        if len(self.tile_redo_tracker) > MAX_TILE_TRACKING:
            self.tile_redo_tracker.pop(0)

        self.tile_redo_tracker.append((coords, tile_index))

    def undo_tile_placement(self) -> None:
        """
            Undo the last tile adding or removal.
            Takes the currently last placed tile's grid location and tile index and
                saves it in the redo_tracker.
            Then takes the last item in the undo_tracker and adds the tile index to the corresponding
                grid location.

            Returns:
                None
        """
        try:
            last_action = self.tile_undo_tracker.pop()
            (x, y), index = last_action
            self.update_redo_tracker(coords=(x, y),
                                     tile_index=self.world_data[y, x])
            self.world_data[y, x] = index
        except IndexError:
            return

    def redo_tile_placement(self) -> None:
        """
            Redo the last undo_tile_placement.
            Takes the currently last 'un-done' tile's grid location and tile index and
                saves it in the undo_tracker.
            Then takes the last item in the redo_tracker and adds the tile index to the corresponding
                grid location.

            Returns:
                None
        """
        try:
            last_action = self.tile_redo_tracker.pop()
            (x, y), index = last_action
            self.update_undo_tracker(
                coords=(x, y),
                tile_index=self.world_data[y, x]
            )
            self.world_data[y, x] = index

        except IndexError:
            return

    def place_and_remove_tiles(self) -> None:
        """
            Places self.current_tile on the grid at current mouse position or
                removes tile in current grid location.
        """
        mouse_pos = self.mouse_pos
        x = int((mouse_pos[0] - (self.scroll_x * self.scale)) / (self.grid_size_x * self.scale))
        y = int((mouse_pos[1] - (self.scroll_y * self.scale)) / (self.grid_size_y * self.scale))
        # Check if within map canvas
        if mouse_pos[0] < SCREEN_WIDTH and mouse_pos[1] < SCREEN_HEIGHT:
            if pygame.mouse.get_pressed()[0] == 1:

                # Add new tile if within map bounds
                if helpers.can_place_tile(editor=self,
                                          grid_x=x,
                                          grid_y=y):
                    old_tile_index = self.world_data[y, x]
                    self.update_undo_tracker(coords=(x, y),
                                             tile_index=old_tile_index)
                    self.world_data[y, x] = self.current_object
                    self.tile_redo_tracker = []
                    print(f"x={x}  y={y}")
                    print(self.scroll_x)

            elif pygame.mouse.get_pressed()[2] == 1:
                # Remove tile if within bounds
                if helpers.can_remove_tile(editor=self,
                                           grid_x=x,
                                           grid_y=y):
                    old_tile_index = self.world_data[y, x]
                    self.world_data[y, x] = -1
                    self.update_undo_tracker(coords=(x, y),
                                             tile_index=old_tile_index)
                    self.tile_redo_tracker = []

    def draw_bottom_panel(self) -> None:
        """
            Blits bottom panel to the screen according to
                panel settings.
        """
        pygame.draw.rect(surface=self.screen,
                         color=BOTTOM_PANEL_COLOR,
                         rect=(0,
                               SCREEN_HEIGHT,
                               SCREEN_WIDTH,
                               BOTTOM_MARGIN),
                         width=0)

    def draw_minimap(self) -> None:
        """
            Blits minimap section and view to the screen.
        """
        minimap_surface: pygame.Surface = pygame.Surface((
            RIGHT_MARGIN,
            BOTTOM_MARGIN
        ))

        minimap_background = pygame.draw.rect(surface=minimap_surface,
                                              color=MINIMAP_PANEL_COLOR,
                                              rect=(
                                                  0,
                                                  0,
                                                  RIGHT_MARGIN,
                                                  BOTTOM_MARGIN
                                              ),
                                              width=0)

        scale_factor, minimap_view_width, minimap_view_height = helpers.get_minimap_dimensions(
            editor=self
        )

        map_outline = pygame.draw.rect(surface=minimap_surface,
                                       color=MAP_OUTLINE_COLOR,
                                       rect=(
                                           MAP_OUTLINE_WIDTH + (
                                                   RIGHT_MARGIN - minimap_view_width) // 2,
                                           MAP_OUTLINE_WIDTH + (
                                                   BOTTOM_MARGIN - minimap_view_height) // 2,
                                           minimap_view_width - MAP_OUTLINE_WIDTH,
                                           minimap_view_height - MAP_OUTLINE_WIDTH
                                       ),
                                       width=MAP_OUTLINE_WIDTH)

        view_area = pygame.draw.rect(surface=minimap_surface,
                                     color=MAP_VIEW_OUTLINE_COLOR,
                                     rect=(
                                         map_outline.topleft[0] - self.scroll_x * scale_factor,
                                         map_outline.topleft[1] - self.scroll_y * scale_factor,
                                         (SCREEN_WIDTH * scale_factor) / self.scale,
                                         (SCREEN_HEIGHT * scale_factor) / self.scale
                                     ),
                                     width=MAP_VIEW_OUTLINE_WIDTH)

        minimap_outline = pygame.draw.rect(surface=minimap_surface,
                                           color=MINIMAP_OUTLINE_COLOR,
                                           rect=(
                                               0,
                                               0,
                                               RIGHT_MARGIN,
                                               BOTTOM_MARGIN
                                           ),
                                           width=MINIMAP_OUTLINE_WIDTH)

        self.screen.blit(minimap_surface, (
            SCREEN_WIDTH,
            SCREEN_HEIGHT
        ))

    def run(self):
        while self.is_running:
            # General
            self.events = pygame.event.get()
            self.keys = pygame.key.get_pressed()
            self.mouse_pos = pygame.mouse.get_pos()
            pygame.display.set_caption(
                f"Editing: {self.map_name} ({self.columns}x{self.rows}) @ {int(self.clock.get_fps())} fps")

            # Background
            self.screen.fill((89, 160, 205))
            self.draw_background(scroll_x=self.scroll_x,
                                 scroll_y=self.scroll_y)

            # Grid
            if self.show_grid:
                self.draw_grid()

            # World
            self.set_col_start_stop()
            self.set_row_start_stop()
            self.draw_map()

            # Panels
            self.draw_minimap()
            self.draw_right_panel()
            self.draw_bottom_panel()

            # Quitting
            self.event_handler.quitting_events()

            # Scrolling
            self.event_handler.scrolling_events()

            # # Errors
            # self.error_handler.set_out_of_bounds_error()
            # self.error_handler.set_preset_error()
            # self.error_handler.set_tile_error()
            # self.error_handler.display_error_messages()

            # Menus
            self.menu_controller.run()

            # Quick menu events
            self.event_handler.undo_redo_events()

            if self.is_building:
                # Quick Menu
                if self.undo_button.draw():
                    self.undo_tile_placement()
                if self.redo_button.draw():
                    self.redo_tile_placement()
                if self.grid_button.draw():
                    self.show_grid = not self.show_grid

                if self.zoom_in_button.draw():
                    self.zoom_in()
                if self.zoom_out_button.draw():
                    self.zoom_out()

                # Actual building
                self.set_scroll_restrictions()
                self.scroll_map()
                self.is_displaying_presets = self.menu_controller.is_displaying_presets
                if not self.is_displaying_presets:
                    # Tile selection
                    self.draw_and_select_tile()
                    self.draw_tile_labels()
                    self.highlight_selected_tile()
                    self.place_and_remove_tiles()

            # Errors
            self.error_handler.set_out_of_bounds_error()
            self.error_handler.set_preset_error()
            self.error_handler.set_tile_error()
            self.error_handler.display_error_messages()

            pygame.display.update()
            self.clock.tick(180)

        pygame.quit()
