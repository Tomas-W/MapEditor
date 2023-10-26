from typing import List, Self, Union, Dict

import pygame

from settings.buttons import *
from settings.paths import *
from settings.panels import *

from utilities.sprites import get_preset_sprites


class TileButton:
    def __init__(self,
                 x: int,
                 y: int,
                 image: pygame.Surface,
                 scale: int,
                 tile_index: Union[None, int],
                 editor: any) -> Self:
        """
            Initialize a TileButton to be used in the right panel to
                place tiles on the grid.

            Args:
                x (int): The x-coordinate of the button's top-left corner.
                y (int): The y-coordinate of the button's top-left corner.
                image (pygame.Surface): The image to use for the button.
                scale (int): The scaling factor for the image.
                tile_index (int): The index associated with the tile.
                editor (any): Current Editor instance.

        """
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image,
                                            (int(width * scale),
                                             int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.tile_index = tile_index

        self.editor = editor

    def __str__(self) -> str:
        return f"TileButton instance (index: {self.tile_index})"

    def draw(self) -> bool:
        """
            Draws the TileButton on screen.
            Listens for mouse click and returns a bool conveying
                if user clicked (mouse 1) on the Button.

            Returns:
                bool: True if the button was clicked, False otherwise.
        """
        action = False

        if self.rect.collidepoint(self.editor.mouse_pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        self.editor.screen.blit(self.image, (self.rect.x, self.rect.y))

        return action


class UtilityButton:
    def __init__(self,
                 x: int,
                 y: int,
                 image: pygame.Surface,
                 scale: int,
                 name: str,
                 editor: any) -> Self:
        """
            Initialize a Button.

            Args:
                x (int): The x-coordinate of the button's top-left corner.
                y (int): The y-coordinate of the button's top-left corner.
                image (pygame.Surface): Image used for the button.
                scale (int): The scaling factor for the image.
                name str): Name of the utility.
                editor (any): Current Editor instance.

        """
        width = image.get_width()
        height = image.get_height()

        self.image = pygame.transform.scale(image,
                                            (int(width * scale),
                                             int(height * scale)))
        self.image.set_alpha(200)

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

        self.name = name
        self.editor = editor

    def __str__(self) -> str:
        return f"UtilityButton instance (name: {self.name})"

    def draw(self) -> bool:
        """
            Draws the button on screen.
            Listens for mouse click and returns a bool conveying
                if user clicked (mouse 1) on the Button.

            Button's appearance changes when uer hovers over or clicks ont the button.

            Returns:
                bool: True if the button was clicked, False otherwise.
        """
        button_selected = False
        action = False

        if self.rect.collidepoint(self.editor.mouse_pos):
            self.image.set_alpha(255)

            if self.clicked:
                for event in self.editor.events:
                    if event.type == pygame.MOUSEBUTTONUP:
                        action = True

            if pygame.mouse.get_pressed()[0] == 1:
                button_selected = True

                if not self.clicked:
                    self.clicked = True

        else:
            self.image.set_alpha(200)

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        self.editor.screen.blit(self.image, (self.rect.x, self.rect.y))
        if button_selected:
            pygame.draw.rect(
                surface=self.editor.screen,
                color=BUTTON_HIGHLIGHT_COLOR,
                rect=self.rect,
                width=BUTTON_HIGHLIGHT_WIDTH
            )
            self.image.set_alpha(255)

        return action


def get_tile_buttons(preset_name: str,
                     editor: any) -> List[TileButton]:
    """
       Get a list of tile buttons related to the preset.

       Args:
           preset_name (str): Name of the preset.
           editor (any): Current Editor instance.

       Returns:
           List[TileButton]: A list of tile buttons.
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
        tile_button = TileButton(x=SCREEN_WIDTH + (TILE_X_SPACING * button_col + TILE_X),
                                 y=TILE_Y_OFFSET * button_row + TILE_START_Y,
                                 image=tile_list_[i],
                                 scale=1,
                                 tile_index=index_list[i],
                                 editor=editor)
        button_list.append(tile_button)
        button_col += 1
        if button_col == 3:
            button_row += 1
            button_col = 0

    return button_list


def get_utility_button(editor: any,
                       **kwargs) -> UtilityButton:
    """
        Creates a UtilityButton instance based on a dict containing the Button's parameters.

        Args:
             editor (any): Current Editor instance.
             **kwargs (dict): Button parameters (x, y, image, scale, tile_index)

        Returns:
              A UtilityButton with kwargs attributes.
    """
    util_button = UtilityButton(editor=editor,
                                **kwargs)
    return util_button
