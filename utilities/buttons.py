from typing import List, Self, Union, Dict

import pygame

from settings.paths import *
from settings.panels import *

from utilities.sprites import get_preset_sprites


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

    def __str__(self) -> str:
        return f"Button instance (index: {self.tile_index})"

    def draw(self,
             surface: pygame.Surface) -> bool:
        """
            Draws the button on screen.
            Listens for mouse click and returns a bool conveying
                if user clicked (mouse 1) on the Button.

            Args:
                surface (pygame.Surface): The surface to draw the button on.

            Returns:
                bool: True if the button was clicked, False otherwise.
        """
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action


def get_tile_buttons(preset_name: str) -> List[Button]:
    """
       Get a list of tile buttons related to the preset.

       Args:
           preset_name (str): Name of the preset.

       Returns:
           List[Button]: A list of tile buttons.
       """
    button_list = []
    button_col = 0
    button_row = 0

    # Get tiles corresponding to the current tab
    tile_list_ = get_preset_sprites(preset_name=preset_name)
    # Get their indexes for tile-map
    index_list = sorted([int(f.split("_")[0]) for f in
                         os.listdir(os.path.join(PRESET_DIR, preset_name)) if
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


def get_utility_button(btn_dict: Dict[str, Dict[str, Button]],
                       name: str,
                       state: str,
                       **kwargs) -> Button:
    """
        Creates a Button instance based on a dict containing the Button's parameters.
        Adds Button to active Editor instance to allow calculations.

        Args:
             btn_dict (Dict): Editor attribute containing all utility Buttons.
             name (str): Name of the Button used to save as key value in btn_dict.
             state (str): Button type (inactive, selected, active).
             **kwargs (Dict): Button parameters (x, y, image, scale, tile_index)

        Returns:
              A Button with kwargs attributes.
    """
    util_button = Button(**kwargs)
    btn_dict[name] = {state: util_button}
    return util_button
