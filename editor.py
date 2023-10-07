import time
from typing import Union

from settings import *
import pygame

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH + RIGHT_MARGIN,
                                  SCREEN_HEIGHT + BOTTOM_MARGIN))

import pickle

import utilities.buttons as buttons
import utilities.sprites as sprites
import utilities.fonts as fonts
import utilities.helpers as helpers


class Editor:
    def __init__(self):
        # Setup
        self.map_name: str = "New map"
        self.temp_map_name: str = self.map_name
        self.sky = sprites.sky_img
        self.background = sprites.background_img
        self.world_data: list[list[int]] = [[-1] * COLUMNS for _ in range(ROWS)]

        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.screen: pygame.display = screen
        self.events: pygame.event = None

        self.label_font: pygame.font = fonts.label_font
        self.tab_font: pygame.font = fonts.tab_font
        self.change_name_font: pygame.font = fonts.change_name_font
        self.map_names_font: pygame.font = fonts.map_names_font

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

        # Tabs
        self.tile_start_y: int = 0
        self.tab_names: list[str] = helpers.get_preset_dir_names()
        self.current_tab: str = self.tab_names[0]

        # Tiles
        self.level_objects: list[pygame.Surface] = sprites.get_all_level_objects(
            folder_path=PRESET_DIR)
        self.tile_list: list[pygame.Surface] = sprites.get_current_tab_sprites(
            tab_name=self.current_tab)
        self.tile_names: list[str] = helpers.get_tile_names(current_tab=self.current_tab)
        self.tile_indexes: list[int] = helpers.get_tile_indexes(current_tab=self.current_tab)
        self.tile_buttons: list[buttons.Button] = buttons.get_tile_buttons(
            len(self.tab_names) * TAB_NAME_FONT_HEIGHT + TILE_BUTTON_Y_OFFSET, self.current_tab)
        self.current_tile: int = 0
        self.current_object: int = self.tile_indexes[0]

        # Utility buttons
        self.save_button = buttons.get_save_button()
        self.load_button = buttons.get_load_button()
        self.name_button = buttons.get_name_button()
        self.back_button = buttons.get_back_button()
        self.ok_button = buttons.get_ok_button()

        # States
        self.is_running = True
        self.is_building = True
        self.is_changing_name = False
        self.is_loading_map = False

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
        for event in self.events:
            # Activate scrolling
            if event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_a:
                        self.scroll_left = True
                    case pygame.K_a:
                        self.scroll_left = True
                    case pygame.K_d:
                        self.scroll_right = True
                    case pygame.K_w:
                        self.scroll_up = True
                    case pygame.K_s:
                        self.scroll_down = True

                    case pygame.K_LSHIFT:
                        self.scroll_speed = self.max_scroll_speed

            # De-activate scrolling
            if event.type == pygame.KEYUP:
                match event.key:
                    case pygame.K_a:
                        self.scroll_left = False
                    case pygame.K_a:
                        self.scroll_left = False
                    case pygame.K_d:
                        self.scroll_right = False
                    case pygame.K_w:
                        self.scroll_up = False
                    case pygame.K_s:
                        self.scroll_down = False

                    case pygame.K_LSHIFT:
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

    def draw_text(self,
                  text: str,
                  font: pygame.font,
                  color: tuple[int, int, int],
                  x_pos: int,
                  y_pos: int,
                  get_rect: bool = False):
        """
           Generic function to draw text on screen.

           Args:
               text (str): Text to blit to screen.
               font (pygame.font.Font): pygame.font object.
               color (tuple[int, int, int]): Text color in RGB format.
               x_pos (int): Text x-position.
               y_pos (int): Text y-position.
               get_rect (bool, optional): Flag to indicate if position information is needed.
                   Default is False.

           Returns:
               None or Tuple[int, int, int, int]: If get_pos is True, returns a tuple containing
                   (x-position, y-position, width, height) of the rendered text.
                   Otherwise, returns None.
        """
        image = font.render(text, True, color)
        self.screen.blit(image,
                         (x_pos, y_pos))

        if get_rect:
            rect = image.get_rect()
            return rect

    def draw_text_centered_x(self,
                             text: str,
                             font: pygame.font,
                             color: tuple[int, int, int],
                             y_pos: int,
                             get_rect: bool = False):
        """
           Generic function to draw text on center of x-axis of screen.

           Args:
               text (str): Text to blit to screen.
               font (pygame.font.Font): pygame.font object.
               color (tuple[int, int, int]): Text color in RGB format.
               y_pos (int): Text y-position.
               get_rect (bool, optional): Flag to indicate if position information is needed.
                   Default is False.

           Returns:
               None or Tuple[int, int, int, int]: If get_pos is True, returns a tuple containing
                   (x-position, y-position, width, height) of the rendered text.
                   Otherwise, returns None.
        """
        image = font.render(text, True, color)
        rect = image.get_rect()
        self.screen.blit(image, ((SCREEN_WIDTH + RIGHT_MARGIN) // 2 - rect.width // 2, y_pos))

        if get_rect:
            centered_rect = image.get_rect()
            return centered_rect

    def draw_background(self) -> None:
        """
            Blits self.background to self.screen.
        """
        self.screen.blit(self.background,
                         (self.scroll_x, self.scroll_y))

    def draw_grid(self) -> None:
        """
            Draws horizontal and vertical lines on screen according to
                grid size settings.
        """
        # Horizontal lines
        for x in range(ROWS + 1):
            pygame.draw.line(self.screen,
                             GRID_LINE_COLOR,
                             (0, x * GRID_SIZE_Y + self.scroll_y),
                             (SCREEN_WIDTH, x * GRID_SIZE_Y + self.scroll_y))

        # Vertical lines
        for y in range(COLUMNS + 1):
            pygame.draw.line(self.screen,
                             GRID_LINE_COLOR,
                             (y * GRID_SIZE_X + self.scroll_x, 0),
                             (y * GRID_SIZE_X + self.scroll_x, SCREEN_HEIGHT))

    def draw_world(self) -> None:
        """
            Loops over self.world_data and draws all objects.
        """
        for x, row in enumerate(self.world_data):
            for y, tile in enumerate(row):
                if tile > -1:
                    self.screen.blit(self.level_objects[tile],
                                     (y * GRID_SIZE_X + self.scroll_x,
                                      x * GRID_SIZE_Y + self.scroll_y))

    def draw_right_panel(self) -> None:
        """
            Blits right panel to the screen according to
                panel settings.
        """
        pygame.draw.rect(self.screen,
                         RIGHT_PANEL_COLOR,
                         (SCREEN_WIDTH,
                          0,
                          RIGHT_MARGIN,
                          SCREEN_HEIGHT + BOTTOM_MARGIN))

    def draw_tab_names(self) -> None:
        """
            Draws names of sub-folders in 'presets' folder on the side panel and
                allows switching between different tiles contained in the selected folder.
        """
        tabs = 1
        # Draw the clickable folder names
        for i, name in enumerate(self.tab_names):
            text_pos = self.draw_text(text=name,
                                      font=self.tab_font,
                                      color=TAB_NAME_COLOR,
                                      x_pos=TAB_NAME_X_OFFSET,
                                      y_pos=TAB_NAME_Y_OFFSET + i * TAB_NAME_Y_SPACING,
                                      get_rect=True)

            text_rect = pygame.rect.Rect(text_pos)
            # Check for collision between mouse and tab
            if text_rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(
                    surface=screen,
                    color=TAB_HIGHLIGHT_COLOR,
                    rect=(text_pos[0] + TAB_HIGHLIGHT_LEFT_OFFSET,
                          text_pos[1] + TAB_HIGHLIGHT_LEFT_OFFSET,
                          text_pos[2] + TAB_HIGHLIGHT_RIGHT_OFFSET,
                          text_pos[3] + TAB_HIGHLIGHT_RIGHT_OFFSET),
                    width=TAB_HIGHLIGHT_WIDTH
                )
                for event in self.events:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        # Check if user presses the mouse button
                        if event.button == 1:
                            # Load settings
                            self.current_tab = name
                            self.current_tile = 0
                            self.current_object = \
                                helpers.get_tile_indexes(current_tab=self.current_tab)[0]
                            self.tile_list = sprites.get_current_tab_sprites(
                                tab_name=self.current_tab)
                            self.tile_names = helpers.get_tile_names(current_tab=self.current_tab)
                            self.tile_buttons = buttons.get_tile_buttons(
                                tile_start_y=len(
                                    self.tab_names) * TAB_NAME_FONT_HEIGHT + TILE_BUTTON_Y_OFFSET,
                                tab_name=self.current_tab)

            tabs += 1

        # Draw seperator between tabs and tiles
        pygame.draw.line(surface=self.screen,
                         color=WHITE,
                         start_pos=(SCREEN_WIDTH, TAB_NAME_FONT_HEIGHT * tabs),
                         end_pos=(SCREEN_WIDTH + RIGHT_MARGIN, TAB_NAME_FONT_HEIGHT * tabs))

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
        for tile, text in zip(self.tile_buttons, self.tile_names):
            self.draw_text(text=text,
                           font=self.label_font,
                           color=TILE_LABEL_COLOR,
                           x_pos=tile.rect.topleft[0],
                           y_pos=tile.rect.topleft[1] - TILE_LABEL_Y_OFFSET)

    def highlight_selected_tile(self) -> None:
        """
            Draws a red square around the selected tile.
        """
        pygame.draw.rect(surface=self.screen,
                         color=TILE_HIGHLIGHT_COLOR,
                         rect=(self.tile_buttons[self.current_tile].rect.topleft[
                                   0] + TILE_HIGHLIGHT_LEFT_OFFSET,
                               self.tile_buttons[self.current_tile].rect.topleft[
                                   1] + TILE_HIGHLIGHT_LEFT_OFFSET,
                               TILE_SIZE_X + TILE_HIGHLIGHT_RIGHT_OFFSET,
                               TILE_SIZE_Y + TILE_HIGHLIGHT_RIGHT_OFFSET),
                         width=TILE_HIGHLIGHT_WIDTH)

    def draw_bottom_panel(self) -> None:
        """
            Blits bottom panel to the screen according to
                panel settings.
        """
        pygame.draw.rect(self.screen,
                         BOTTOM_PANEL_COLOR,
                         (0,
                          SCREEN_HEIGHT,
                          SCREEN_WIDTH + BOTTOM_MARGIN,
                          SCREEN_HEIGHT + BOTTOM_MARGIN))

    def draw_utility_buttons(self) -> None:
        """
            Blits utility buttons to the screen.
                Save
                Load
                Name
        """
        if self.save_button.draw(surface=self.screen):
            pickle_out = open(file=os.path.join(MAPS_DIR, self.map_name),
                              mode="wb")
            pickle.dump(obj=self.world_data,
                        file=pickle_out)
            pickle_out.close()

        if self.load_button.draw(self.screen):
            self.is_loading_map = True
            self.is_building = False

        if self.name_button.draw(self.screen):
            self.is_changing_name = True
            self.is_building = False

    def add_and_remove_tiles(self) -> None:
        """
            Places self.current_tile on the grid at current mouse position or
                removes tile in current grid location.
        """
        mouse_pos = pygame.mouse.get_pos()
        x = (mouse_pos[0] - self.scroll_x) // GRID_SIZE_X
        y = (mouse_pos[1] - self.scroll_y) // GRID_SIZE_Y

        # Limit mouse coordinates
        if mouse_pos[0] < SCREEN_WIDTH and mouse_pos[1] < SCREEN_HEIGHT:
            if pygame.mouse.get_pressed()[0] == 1:
                # Add new tile
                if self.world_data[y][x] != self.current_object:
                    self.world_data[y][x] = self.current_object

            if pygame.mouse.get_pressed()[2] == 1:
                # Remove tile
                self.world_data[y][x] = -1

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

    def draw_change_name_text(self) -> None:
        """
            Blits title and name of the map to the screen.
        """
        # Title
        self.draw_text_centered_x(text=CHANGE_NAME_TEXT,
                                  font=self.change_name_font,
                                  y_pos=CHANGE_NAME_TITLE_Y_OFFSET,
                                  color=CHANGE_NAME_TITLE_COLOR)

        # Name
        self.draw_text_centered_x(text=self.temp_map_name,
                                  font=self.change_name_font,
                                  y_pos=CHANGE_NAME_Y_OFFSET,
                                  color=CHANGE_NAME_COLOR)

    def draw_saved_maps_text(self) -> None:
        """
            Checks maps folder to create and display a list of saved maps.
            Highlights name when collision with mouse.
            Loads selected map on click.
        """
        saved_items = os.listdir(MAPS_DIR)

        # Draw map names
        for i, name in enumerate(saved_items):
            saved_map_pos = self.draw_text(text=name,
                                           font=self.map_names_font,
                                           color=WHITE,
                                           x_pos=(SCREEN_WIDTH + RIGHT_MARGIN) // 3,
                                           y_pos=i * 75 + 100,
                                           get_rect=True)

            text_rect = pygame.rect.Rect(saved_map_pos)

            # Check collision
            if text_rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(
                    surface=screen,
                    color=RED,
                    rect=(saved_map_pos[0] - 10,
                          saved_map_pos[1] - 10,
                          saved_map_pos[2] + 20,
                          saved_map_pos[3] + 20),
                    width=5
                )
                if pygame.mouse.get_pressed()[0] == 1:
                    # User selects a map
                    self.scroll_x = 0
                    self.scroll_y = 0
                    self.world_data = []
                    pickle_in = open(f"maps/{saved_items[i]}",
                                     mode="rb")
                    self.world_data = pickle.load(pickle_in)
                    self.is_loading_map = False
                    self.is_building = True
                    time.sleep(0.1)

        if self.back_button.draw(self.screen):
            self.is_loading_map = False
            self.is_building = True

    def run(self):
        while self.is_running:
            # General
            # pygame.event.pump()
            self.events = pygame.event.get()
            self.manage_quitting()

            pygame.display.set_caption(f"Editing: {self.map_name}")

            # Layout
            self.screen.fill((89, 160, 205))
            self.draw_background()
            self.draw_grid()
            self.draw_world()

            self.draw_bottom_panel()
            self.draw_right_panel()

            self.draw_tab_names()
            self.draw_utility_buttons()

            # Tile selection
            self.draw_and_select_tile()
            self.draw_tile_labels()
            self.highlight_selected_tile()

            if self.is_changing_name:
                self.screen.fill(DARK_ORANGE)
                self.draw_change_name_text()
                self.get_map_name_input()

            elif self.is_loading_map:
                self.screen.fill(DARK_ORANGE)
                self.draw_saved_maps_text()

            elif self.is_building:
                self.manage_scrolling()
                self.scroll_map()
                self.add_and_remove_tiles()

            pygame.display.update()
            self.clock.tick(FPS)

        pygame.quit()
