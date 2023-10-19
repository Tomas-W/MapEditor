import time
from typing import List, Self

import pygame

pygame.init()

from settings.setup import *
from settings.paths import *

from settings.canvas import *
from settings.minimap import *
from settings.panels import *

screen = pygame.display.set_mode((SCREEN_WIDTH + RIGHT_MARGIN,
                                  SCREEN_HEIGHT + BOTTOM_MARGIN))

from menus import Menu
from error_handler import ErrorHandler

from settings.buttons import *

import utilities.buttons as buttons
import utilities.fonts as fonts
import utilities.general as general
import utilities.helpers as helpers
import utilities.sprites as sprites
import utilities.text as text


class Editor:
    def __init__(self) -> Self:
        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.screen: pygame.display = screen
        self.events: pygame.event = None
        self.keys: pygame.key = None
        self.mouse_pos = pygame.mouse.get_pos()

        self.map_name: str = "New map"
        self.temp_map_name: str = self.map_name
        self.sky = sprites.sky_img
        self.background = sprites.background_img

        self._rows = ROWS
        self._columns = COLUMNS
        self._grid_size_x = GRID_SIZE_X
        self._grid_size_y = GRID_SIZE_Y
        # self.preferences_dict: Dict[str, int] = helpers.get_preferences_dict(editor=self)
        self.world_data: List[List[int]] = general.get_fresh_world_data(
            columns=self._columns,
            rows=self._rows
        )

        # Scrolling
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
        self.menus = Menu(editor=self)
        self.menus.preferences_dict = helpers.get_preferences_dict(editor=self)

        # Preferences
        self.selected_preference_name = "_rows"
        self.selected_preference_value = ROWS
        self.selected_preference_value_change = ROWS

        # Presets
        self.preset_names: List[str] = general.get_preset_dir_names()
        self.shortened_preset_names: List[str] = general.get_shortened_dir_names()
        self.current_preset: str = self.preset_names[0]
        self.displaying_presets = False

        # Tiles
        self.level_objects: List[pygame.Surface] = sprites.get_all_level_objects()
        self.tile_list: List[pygame.Surface] = sprites.get_preset_sprites(
            preset_name=self.current_preset
        )
        self.tile_names: List[str] = general.get_tile_names(
            preset_name=self.current_preset
        )
        self.tile_indexes: List[int] = general.get_tile_indexes(
            preset_name=self.current_preset
        )
        self.tile_buttons: List[buttons.Button] = buttons.get_tile_buttons(
            preset_name=self.current_preset
        )
        self.current_tile: int = 0
        self.current_object: int = self.tile_indexes[0]

        # Utility buttons
        self.utility_buttons = {}
        self.sets_button = buttons.get_utility_button(btn_dict=self.utility_buttons,
                                                      name="sets",
                                                      state="inactive",
                                                      **SETS_BTN_INACTIVE)
        self.save_button = buttons.get_utility_button(btn_dict=self.utility_buttons,
                                                      name="save",
                                                      state="inactive",
                                                      **SAVE_BTN_INACTIVE)
        self.load_button = buttons.get_utility_button(btn_dict=self.utility_buttons,
                                                      name="load",
                                                      state="inactive",
                                                      **LOAD_BTN_INACTIVE)
        self.name_button = buttons.get_utility_button(btn_dict=self.utility_buttons,
                                                      name="name",
                                                      state="inactive",
                                                      **NAME_BTN_INACTIVE)
        self.pref_button = buttons.get_utility_button(btn_dict=self.utility_buttons,
                                                      name="pref",
                                                      state="inactive",
                                                      **PREF_BTN_INACTIVE)

        self.back_button = buttons.get_utility_button(btn_dict=self.utility_buttons,
                                                      name="back",
                                                      state="inactive",
                                                      **BACK_BTN_INACTIVE)
        self.ok_button = buttons.get_utility_button(btn_dict=self.utility_buttons,
                                                    name="ok",
                                                    state="inactive",
                                                    **OK_BTN_INACTIVE)

        # States
        self.is_running = True
        self.is_building = True
        self.is_changing_name = False
        self.is_loading_map = False
        self.is_changing_preferences = False

        # Display
        self.show_grid = True

        # Prevent accidental clicks after switches
        self.click_time = 0

        # Errors
        self.error_handler = ErrorHandler(editor=self)

        self.test = 100

    def __str__(self) -> str:
        return "Editor instance"

    def manage_quitting(self) -> None:
        """
            Listens for quit event.
        """
        for event in self.events:
            if event.type == pygame.QUIT:
                self.is_running = False

    def manage_scrolling(self) -> None:
        """
            Gets user inputs and changes scroll values.
        """
        keys = self.keys

        # Activate scrolling
        if keys[pygame.K_a]:
            self.scroll_left = True
        if keys[pygame.K_d]:
            self.scroll_right = True
        if keys[pygame.K_w]:
            self.scroll_up = True
        if keys[pygame.K_s]:
            self.scroll_down = True
        if keys[pygame.K_LSHIFT]:
            self.scroll_speed = self.max_scroll_speed

        # De-activate scrolling
        if not keys[pygame.K_a]:
            self.scroll_left = False
        if not keys[pygame.K_d]:
            self.scroll_right = False
        if not keys[pygame.K_w]:
            self.scroll_up = False
        if not keys[pygame.K_s]:
            self.scroll_down = False
        if not keys[pygame.K_LSHIFT]:
            self.scroll_speed = self.base_scroll_speed

    def scroll_map(self) -> None:
        """
            Scrolls the map based on scroll values.
        """
        if self.scroll_left:
            self.scroll_x += self.scroll_speed
        if self.scroll_right:
            self.scroll_x -= self.scroll_speed
        if self.scroll_up:
            self.scroll_y += self.scroll_speed
        if self.scroll_down:
            self.scroll_y -= self.scroll_speed

    def draw_background(self,
                        background: pygame.Surface,
                        scroll_x: int,
                        scroll_y: int) -> None:
        """
            Blits the background image to the screen.

            Args:
                background (pygame.Surface): Background image of the map.
                scroll_x (int): X coordinate of background.topleft.
                scroll_y (int): Y coordinate of background.topleft.
        """
        self.screen.blit(background,
                         (scroll_x, scroll_y))

    def draw_grid(self) -> None:
        """
            Draws horizontal and vertical lines on screen according to
                grid size settings.
        """
        # Horizontal lines
        for x in range(self._rows + 1):
            pygame.draw.line(surface=self.screen,
                             color=GRID_LINE_COLOR,
                             start_pos=(0, x * self._grid_size_y + self.scroll_y),
                             end_pos=(SCREEN_WIDTH, x * self._grid_size_y + self.scroll_y))

        # Vertical lines
        for y in range(self._columns + 1):
            pygame.draw.line(surface=self.screen,
                             color=GRID_LINE_COLOR,
                             start_pos=(y * self._grid_size_x + self.scroll_x, 0),
                             end_pos=(y * self._grid_size_x + self.scroll_x, SCREEN_HEIGHT))

    def draw_world(self) -> None:
        """
            Loops over self.world_data and draws all objects.
        """
        for x, row in enumerate(self.world_data):
            for y, tile in enumerate(row):
                if tile > -1:
                    self.screen.blit(source=self.level_objects[tile],
                                     dest=(y * self._grid_size_x + self.scroll_x,
                                           x * self._grid_size_x + self.scroll_y))

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

    def load_new_preset(self, selected_preset: str) -> None:
        """
            Loads all settings for the selected preset.

            Args:
                 selected_preset (str): Name of the preset to load.
        """
        self.current_preset = selected_preset
        self.current_tile = 0

        self.current_object = general.get_tile_indexes(
            preset_name=self.current_preset)[0]
        self.tile_list = sprites.get_preset_sprites(
            preset_name=self.current_preset
        )
        self.tile_names = general.get_tile_names(
            preset_name=self.current_preset
        )
        print(self.tile_names)
        self.tile_buttons = buttons.get_tile_buttons(
            preset_name=self.current_preset
        )
        self.displaying_presets = False

    def draw_and_select_tile(self) -> None:
        """
            Draws all tiles on side panel and stores currently selected tile.
        """
        for button_count, button in enumerate(self.tile_buttons):
            if button.draw(self.screen):
                self.current_tile = button_count
                self.current_object = button.tile_index

    def draw_tile_labels(self) -> None:
        """
            Draws label above the tile on the side panel.
        """
        for tile, text_ in zip(self.tile_buttons, self.tile_names):
            text.draw(screen=self.screen,
                      text=str(text_),
                      font=fonts.label_font,
                      color=TILE_LABEL_COLOR,
                      x_pos=tile.rect.topleft[0],
                      y_pos=tile.rect.topleft[1] - TILE_LABEL_Y_OFFSET)

    def highlight_selected_tile(self) -> None:
        """
            Draws a red square around the selected tile.
        """
        pygame.draw.rect(
            surface=self.screen,
            color=TILE_HIGHLIGHT_COLOR,
            rect=(self.tile_buttons[self.current_tile].rect.topleft[0] + TILE_HIGHLIGHT_LEFT_OFFSET,
                  self.tile_buttons[self.current_tile].rect.topleft[1] + TILE_HIGHLIGHT_LEFT_OFFSET,
                  TILE_SIZE_X + TILE_HIGHLIGHT_RIGHT_OFFSET,
                  TILE_SIZE_Y + TILE_HIGHLIGHT_RIGHT_OFFSET),
            width=TILE_HIGHLIGHT_WIDTH)

    def place_and_remove_tiles(self) -> None:
        """
            Places self.current_tile on the grid at current mouse position or
                removes tile in current grid location.
        """
        mouse_pos = self.mouse_pos
        x = (mouse_pos[0] - self.scroll_x) // self._grid_size_x
        y = (mouse_pos[1] - self.scroll_y) // self._grid_size_y

        # Check if within map canvas
        if mouse_pos[0] < SCREEN_WIDTH and mouse_pos[1] < SCREEN_HEIGHT:
            if pygame.mouse.get_pressed()[0] == 1:
                # Add new tile if within map bounds
                if helpers.can_place_tile(editor=self,
                                          grid_x=x,
                                          grid_y=y):
                    self.world_data[y][x] = self.current_object

            if pygame.mouse.get_pressed()[2] == 1:
                # Remove tile if within bounds
                if helpers.can_remove_tile(editor=self,
                                           grid_x=x,
                                           grid_y=y):
                    self.world_data[y][x] = -1

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

    def draw_utility_buttons(self) -> None:
        """
            Blits utility buttons to the screen.
                Sets (Presets of images)
                Save (Save current map)
                Load (Load saved map)
                Name (Rename current map)
        """
        if self.sets_button.draw(self.screen):
            self.displaying_presets = not self.displaying_presets

        if self.save_button.draw(self.screen):
            helpers.save_map_details(editor=self)

        if self.load_button.draw(self.screen):
            self.is_loading_map = True
            self.is_building = False

        if self.name_button.draw(self.screen):
            self.is_changing_name = True
            self.is_building = False

        if self.pref_button.draw(self.screen):
            self.is_building = False
            self.is_changing_preferences = True

    def highlight_utility_buttons(self) -> None:
        pass

    def get_preference_input(self) -> None:
        """
            Listens for keydown events to change the value of a preference.
        """
        for events in self.events:
            if events.type == pygame.KEYDOWN:
                if events.key == pygame.K_BACKSPACE:
                    # Delete last character
                    self.selected_preference_value_change = str(
                        self.selected_preference_value_change)[:-1]

                elif events.key in range(pygame.K_0, pygame.K_9 + 1):
                    self.selected_preference_value_change = str(
                        self.selected_preference_value_change) + events.unicode

    def draw_preference_buttons(self) -> None:
        # Do not save value and go back
        if self.back_button.draw(self.screen):
            self.is_changing_preferences = False
            self.is_building = True

        # Save new value
        if self.ok_button.draw(self.screen):
            if general.is_new_value_allowed(name=self.selected_preference_name,
                                            value=int(self.selected_preference_value_change)):
                print(
                    f"{self.selected_preference_name} changed from {self.selected_preference_value} to {self.selected_preference_value_change}")
                self.selected_preference_value = self.selected_preference_value_change

                attributes_dict = {
                    self.selected_preference_name: int(self.selected_preference_value)
                }
                helpers.update_class_dict(cls=self,
                                          attributes=attributes_dict)
                self.background = helpers.update_background(editor=self)
                self.menus.preferences_dict = helpers.get_preferences_dict(editor=self)

            else:
                print(
                    f"name: '{self.selected_preference_name}' cannot be value: '{self.selected_preference_value_change}"'')

    def get_map_name_input(self) -> None:
        """
            Listens for keydown events to change the name of the map.
        """
        for events in self.events:
            if events.type == pygame.KEYDOWN:

                if events.key == pygame.K_BACKSPACE:
                    # Delete last character
                    self.temp_map_name = self.temp_map_name[:-1]

                elif events.key == pygame.K_RETURN:
                    # Exit out
                    self.is_changing_name = False
                    self.is_building = True
                    self.map_name = self.temp_map_name

                else:
                    # Add new character to end
                    self.temp_map_name += events.unicode

        # Do not save new map name
        if self.back_button.draw(self.screen):
            self.temp_map_name = self.map_name
            self.is_changing_name = False
            self.is_building = True

        # Save new map name
        if self.ok_button.draw(self.screen):
            self.map_name = self.temp_map_name
            self.is_changing_name = False
            self.is_building = True

    def draw_minimap(self) -> None:
        """
            Blits minimap section and view to the screen.
        """
        minimap_background = pygame.draw.rect(surface=self.screen,
                                              color=MINIMAP_PANEL_COLOR,
                                              rect=(
                                                  SCREEN_WIDTH,
                                                  SCREEN_HEIGHT,
                                                  RIGHT_MARGIN,
                                                  BOTTOM_MARGIN
                                              ),
                                              width=0)

        minimap_outline = pygame.draw.rect(surface=self.screen,
                                           color=MINIMAP_OUTLINE_COLOR,
                                           rect=(
                                               SCREEN_WIDTH + MINIMAP_OUTLINE_WIDTH // 2,
                                               SCREEN_HEIGHT + MINIMAP_OUTLINE_WIDTH // 2,
                                               RIGHT_MARGIN - MINIMAP_OUTLINE_WIDTH // 2,
                                               BOTTOM_MARGIN - MINIMAP_OUTLINE_WIDTH // 2
                                           ),
                                           width=MINIMAP_OUTLINE_WIDTH)

        scale_factor, minimap_view_width, minimap_view_height = helpers.get_minimap_dimensions(
            editor=self
        )

        map_outline = pygame.draw.rect(surface=self.screen,
                                       color=MAP_OUTLINE_COLOR,
                                       rect=(
                                           SCREEN_WIDTH + MAP_OUTLINE_WIDTH + (
                                                   RIGHT_MARGIN - minimap_view_width) // 2,
                                           SCREEN_HEIGHT + MAP_OUTLINE_WIDTH + (
                                                   BOTTOM_MARGIN - minimap_view_height) // 2,
                                           minimap_view_width - MAP_OUTLINE_WIDTH,
                                           minimap_view_height - MAP_OUTLINE_WIDTH
                                       ),
                                       width=MAP_OUTLINE_WIDTH)

        view_area = pygame.draw.rect(surface=self.screen,
                                     color=MAP_VIEW_OUTLINE_COLOR,
                                     rect=(
                                         map_outline.topleft[0] - self.scroll_x * scale_factor,
                                         map_outline.topleft[1] - self.scroll_y * scale_factor,
                                         SCREEN_WIDTH * scale_factor,
                                         SCREEN_HEIGHT * scale_factor
                                     ),
                                     width=MAP_VIEW_OUTLINE_WIDTH)

    def run(self):
        while self.is_running:
            # General
            # pygame.event.pump()
            self.events = pygame.event.get()
            self.keys = pygame.key.get_pressed()
            self.mouse_pos = pygame.mouse.get_pos()
            self.manage_quitting()

            pygame.display.set_caption(
                f"Editing: {self.map_name} @ {int(self.clock.get_fps())} fps")

            # Layout
            self.screen.fill((89, 160, 205))
            self.draw_background(background=self.background,
                                 scroll_x=self.scroll_x,
                                 scroll_y=self.scroll_y)

            # Canvas
            if self.show_grid:
                self.draw_grid()
            self.draw_world()

            # Errors
            self.error_handler.set_out_of_bounds_error()
            self.error_handler.display_error_messages()

            # Panels
            self.draw_minimap()
            self.draw_bottom_panel()
            self.draw_right_panel()

            if self.displaying_presets:
                self.menus.draw_presets_menu()
                self.menus.display_presets_previews()
                selected_preset = self.menus.highlight_selected_preset()
                if selected_preset is not None:
                    self.load_new_preset(selected_preset=selected_preset)
                    time.sleep(0.1)  # to prevent placing tile

            self.draw_utility_buttons()

            if self.is_changing_name:
                self.screen.fill(DARK_ORANGE)
                self.menus.draw_rename_menu()
                self.get_map_name_input()

            elif self.is_loading_map:
                self.screen.fill(DARK_ORANGE)
                self.menus.draw_load_map_menu()
                selected_map = self.menus.highlight_selected_map()
                if selected_map is not None:
                    map_attributes = helpers.deserialize_map_details(editor=self,
                                                                     map_name=selected_map)
                    helpers.update_class_dict(cls=self,
                                              attributes=map_attributes)

                    time.sleep(0.1)  # to prevent placing tile

            elif self.is_changing_preferences:
                self.screen.fill(DARK_ORANGE)
                self.menus.draw_preferences_menu()
                self.get_preference_input()
                self.draw_preference_buttons()
                selected_preference = self.menus.highlight_selected_preference()
                if selected_preference is not None:
                    self.selected_preference_name = selected_preference[0]
                    self.selected_preference_value = selected_preference[1]
                    self.selected_preference_value_change = self.selected_preference_value

            elif self.is_building:
                self.manage_scrolling()
                self.scroll_map()
                if not self.displaying_presets:
                    # Tile selection
                    self.draw_and_select_tile()
                    self.draw_tile_labels()
                    self.highlight_selected_tile()
                    self.place_and_remove_tiles()

            pygame.display.update()
            self.clock.tick(FPS)

        pygame.quit()
