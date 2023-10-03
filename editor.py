import time

from settings import *
import pygame
import pickle

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH + RIGHT_MARGIN,
                                  SCREEN_HEIGHT + BOTTOM_MARGIN))

import utilities.buttons as buttons
import utilities.sprites as sprites
import utilities.fonts as fonts


class Editor:
    def __init__(self):
        self.scroll_left = False
        self.scroll_right = False
        self.scroll_up = False
        self.scroll_down = False
        self.scroll_x = 0
        self.scroll_y = 0
        self.scroll_speed = 5
        self.base_scroll_speed = 5
        self.max_scroll_speed = 15

        # General
        self.events = None
        self.map_name = "New map"
        self.sky = sprites.sky_img
        self.background = sprites.background_img
        self.world_data = [[-1] * COLUMNS for _ in range(ROWS)]
        self.small_font = fonts.small_font
        self.medium_font = fonts.medium_font
        self.clock = pygame.time.Clock()
        self.screen = screen

        # Tiles
        # self.tile_list = utilities.tile_list

        self.tile_list = sprites.get_sprites(location="images/hedge_sprites.png",
                                             number_sprites=15,
                                             width=32,
                                             height=32,
                                             scale=1)
        self.tile_names = TILE_NAMES
        self.current_tile = 0
        self.tile_buttons = buttons.get_tile_buttons()

        # Utility
        self.save_button = buttons.get_save_button()
        self.load_button = buttons.get_load_button()
        self.name_button = buttons.get_name_button()
        self.back_button = buttons.get_back_button()

        # Handlers
        self.is_running = True
        self.is_building = True
        self.is_changing_name = False
        self.is_loading_map = False

        self.test = False

    def manage_quitting(self):
        """
        Listens for quit event.
        """
        for event in self.events:
            if event.type == pygame.QUIT:
                self.is_running = False

    def manage_scrolling(self):
        """
        Gets user inputs and changes scroll values.
        """
        for event in self.events:
            # Activate scrolling
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.scroll_left = True
                    print("go left")
                if event.key == pygame.K_d:
                    self.scroll_right = True
                if event.key == pygame.K_w:
                    self.scroll_up = True
                if event.key == pygame.K_s:
                    self.scroll_down = True

                if event.key == pygame.K_LSHIFT:
                    self.scroll_speed = self.max_scroll_speed

            # De-activate scrolling
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.scroll_left = False
                    print("stop left")
                if event.key == pygame.K_d:
                    self.scroll_right = False

                if event.key == pygame.K_w:
                    self.scroll_up = False
                if event.key == pygame.K_s:
                    self.scroll_down = False

                if event.key == pygame.K_LSHIFT:
                    self.scroll_speed = self.base_scroll_speed

    def scroll_map(self):
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

    def draw_text(self, text, font, color, x_pos, y_pos, get_pos=False):
        """
        Generic function to draw text on screen.
        """
        image = font.render(text, True, color)
        self.screen.blit(image, (x_pos, y_pos))

        if get_pos:
            rect = image.get_rect()
            return x_pos, y_pos, rect[2], rect[3]

    def draw_center_text(self, text, font, color, x_pos, y_pos, get_pos=False):
        """
        Generic function to draw text on screen.
        """
        image = font.render(text, True, color)
        self.screen.blit(image, (x_pos, y_pos))

        if get_pos:
            rect = image.get_rect()
            return x_pos - 10, y_pos - 10, rect[2] + 20, rect[3] + 20

    def draw_tile_labels(self):
        """
        Draws label above the tile on the side menu.
        """
        for tile, text in zip(self.tile_buttons, self.tile_names):
            self.draw_text(text=text,
                           font=self.small_font,
                           color=WHITE,
                           x_pos=tile.rect.topleft[0],
                           y_pos=tile.rect.topleft[1] - 20)

    def draw_background(self):
        self.screen.blit(self.background, (self.scroll_x, self.scroll_y))

    def draw_grid(self):
        # Horizontal lines
        for x in range(ROWS + 1):
            pygame.draw.line(self.screen,
                             WHITE,
                             (0, x * GRID_SIZE_Y + self.scroll_y),
                             (SCREEN_WIDTH, x * GRID_SIZE_Y + self.scroll_y))

        # Vertical lines
        for y in range(COLUMNS + 1):
            pygame.draw.line(self.screen,
                             WHITE,
                             (y * GRID_SIZE_X + self.scroll_x, 0),
                             (y * GRID_SIZE_X + self.scroll_x, SCREEN_HEIGHT))

    def draw_world(self):
        """
        Loops over world csv and draws all items.
        """
        for x, row in enumerate(self.world_data):
            for y, tile in enumerate(row):
                if tile > -1:
                    self.screen.blit(self.tile_list[tile],
                                     (y * GRID_SIZE_X + self.scroll_x,
                                      x * GRID_SIZE_Y + self.scroll_y))

    def draw_right_panel(self):
        pygame.draw.rect(self.screen,
                         BROWN,
                         (SCREEN_WIDTH,
                          0,
                          RIGHT_MARGIN,
                          SCREEN_HEIGHT + BOTTOM_MARGIN))

    def draw_and_select_tile(self):
        """
        Draws all tiles on side menu and stores currently selected tile.
        """
        for button_count, button in enumerate(self.tile_buttons):
            if button.draw(self.screen):
                self.current_tile = button_count

    def highlight_selected_tile(self):
        """
        Draws a red square around the selected tile.
        """
        pygame.draw.rect(surface=self.screen,
                         color=RED,
                         rect=(self.tile_buttons[self.current_tile].rect.topleft[0] - 3,
                               self.tile_buttons[self.current_tile].rect.topleft[1] - 3,
                               TILE_SIZE_X + 6,
                               TILE_SIZE_Y + 6),
                         width=3)

    def draw_bottom_panel(self):
        pygame.draw.rect(self.screen,
                         BROWN,
                         (0,
                          SCREEN_HEIGHT,
                          SCREEN_WIDTH + BOTTOM_MARGIN,
                          SCREEN_HEIGHT + BOTTOM_MARGIN))

    def draw_utility_buttons(self):
        if self.save_button.draw(surface=self.screen):
            pickle_out = open(file=f"maps/{self.map_name}",
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

    def add_new_tiles(self):
        """
        Places a tile on the grid at current mouse position.
        """
        mouse_pos = pygame.mouse.get_pos()
        x = (mouse_pos[0] - self.scroll_x) // GRID_SIZE_X
        y = (mouse_pos[1] - self.scroll_y) // GRID_SIZE_Y

        # Limit mouse coordinates
        if mouse_pos[0] < SCREEN_WIDTH and mouse_pos[1] < SCREEN_HEIGHT:
            if pygame.mouse.get_pressed()[0] == 1:
                if self.world_data[y][x] != self.current_tile:
                    self.world_data[y][x] = self.current_tile
            if pygame.mouse.get_pressed()[2] == 1:
                self.world_data[y][x] = -1

    def get_map_name_input(self):
        for events in self.events:
            if events.type == pygame.KEYDOWN:

                if events.key == pygame.K_BACKSPACE:
                    self.map_name = self.map_name[:-1]

                elif events.key == pygame.K_RETURN:
                    self.is_changing_name = False
                    self.is_building = True

                else:
                    self.map_name += events.unicode

        if self.back_button.draw(self.screen):
            self.is_changing_name = False
            self.is_building = True

    def draw_change_name_text(self):
        self.draw_text(text="Provide a name:",
                       font=self.medium_font,
                       color=WHITE,
                       x_pos=550,
                       y_pos=400)

        self.draw_text(text=self.map_name,
                       font=self.medium_font,
                       color=WHITE,
                       x_pos=(SCREEN_WIDTH + RIGHT_MARGIN) // 2 - 8 * len(self.map_name),
                       y_pos=700)

    def draw_saved_maps_text(self):
        saved_items = os.listdir(MAPS_DIR)

        for i, name in enumerate(saved_items):
            saved_map_pos = self.draw_text(text=name,
                                           font=self.medium_font,
                                           color=WHITE,
                                           x_pos=(SCREEN_WIDTH + RIGHT_MARGIN) // 3,
                                           y_pos=i * 75 + 100,
                                           get_pos=True)

            text_rect = pygame.rect.Rect(saved_map_pos)

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

            self.draw_tile_labels()
            self.draw_utility_buttons()

            # Tile selection
            self.draw_and_select_tile()
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
                self.add_new_tiles()

            pygame.display.update()
            self.clock.tick(FPS)

        pygame.quit()
