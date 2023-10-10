from typing import List, Self, Union

import pygame

from settings.paths import *
from settings.bottom_panel import *
from settings.minimap import *
from settings.right_panel import *

from utilities.sprites import save_button_image, load_button_image, back_button_image, \
    name_button_image, ok_button_image, get_current_tab_sprites, sets_button_image


class Button:
    def __init__(self,
                 x: int,
                 y: int,
                 image: pygame.Surface,
                 scale: int,
                 tile_index: Union[None, int]) -> Self:
        """
            Initialize a Button.

            Args:
                x (int): The x-coordinate of the button's top-left corner.
                y (int): The y-coordinate of the button's top-left corner.
                image (pygame.Surface): The image to use for the button.
                scale (int): The scaling factor for the image.
                tile_index (int): The index associated with the tile.

        """
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.tile_index = tile_index

    def draw(self,
             surface: pygame.Surface) -> bool:
        """
           Draw the button on screen.

           Args:
               surface (pygame.Surface): The surface to draw the button on.

           Returns:
               bool: True if the button was clicked, False otherwise.
        """
        action = False

        # get mouse position
        pos = pygame.mouse.get_pos()

        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # draw button
        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action


def get_tile_buttons(tab_names: List[str],
                     current_tab_name: str) -> List[Button]:
    """
       Get a list of tile buttons.

       Args:
           tab_names (List[str]): List of tab names (preset folders).
           current_tab_name (str): The name of the current tab.

       Returns:
           List[Button]: A list of tile buttons.
       """
    button_list = []
    button_col = 0
    button_row = 0

    # Get tiles corresponding to the current tab
    tile_list_ = get_current_tab_sprites(tab_name=current_tab_name)
    # Get their indexes for tile-map
    index_list = sorted([int(f.split("_")[0]) for f in
                         os.listdir(os.path.join(PRESET_DIR, current_tab_name)) if
                         f.endswith('.png')])

    # Create and append all tile buttons
    for i in range(len(tile_list_)):
        tile_button = Button(x=SCREEN_WIDTH + (85 * button_col + 50),
                             y=80 * button_row + TILE_START_Y,
                             image=tile_list_[i],
                             scale=1,
                             tile_index=index_list[i])
        button_list.append(tile_button)
        button_col += 1
        if button_col == 3:
            button_row += 1
            button_col = 0

    return button_list


def get_sets_button() -> Button:
    """
       Get the sets button.

       Returns:
           Button: The sets button.
       """
    return Button(x=SETS_BUTTON_X,
                  y=SETS_BUTTON_Y,
                  image=sets_button_image,
                  scale=1,
                  tile_index=None)


def get_save_button() -> Button:
    """
       Get the save button.

       Returns:
           Button: The save button.
       """
    return Button(x=SAVE_BUTTON_X_OFFSET,
                  y=SAVE_BUTTON_Y_OFFSET,
                  image=save_button_image,
                  scale=1,
                  tile_index=None)


def get_load_button() -> Button:
    """
       Get the load button.

       Returns:
           Button: The load button.
       """
    return Button(x=LOAD_BUTTON_X_OFFSET,
                  y=LOAD_BUTTON_Y_OFFSET,
                  image=load_button_image,
                  scale=1,
                  tile_index=None)


def get_name_button() -> Button:
    """
       Get the name button.

       Returns:
           Button: The name button.
       """
    return Button(x=NAME_BUTTON_X_OFFSET,
                  y=NAME_BUTTON_Y_OFFSET,
                  image=name_button_image,
                  scale=1,
                  tile_index=None)


def get_back_button() -> Button:
    """
       Get the back button.

       Returns:
           Button: The back button.
       """
    return Button(x=(SCREEN_WIDTH + RIGHT_MARGIN) // 2 - back_button_image.get_width() * 1.5,
                  y=BACK_BUTTON_Y_OFFSET_NAME_SCREEN,
                  image=back_button_image,
                  scale=1,
                  tile_index=None)


def get_ok_button() -> Button:
    """
       Get the ok button.

       Returns:
           Button: The ok button.
       """
    return Button(x=(SCREEN_WIDTH + RIGHT_MARGIN) // 2 + ok_button_image.get_width() // 2,
                  y=BACK_BUTTON_Y_OFFSET_NAME_SCREEN,
                  image=ok_button_image,
                  scale=1,
                  tile_index=None)
