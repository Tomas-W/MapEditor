import time
from typing import Union

import pygame

from settings.canvas import *
from settings.paths import *
from settings.setup import *
from utilities import helpers


def draw_background(screen: pygame.Surface,
                    background: pygame.Surface,
                    scroll_x: int,
                    scroll_y: int) -> None:
    """
        Blits the background image to the screen.

        Args:
            screen (pygame.Surface): Editor window.
            background (pygame.Surface): Background image of the map.
            scroll_x (int): X coordinate of background.topleft.
            scroll_y (int): Y coordinate of background.topleft.
    """
    screen.blit(background,
                (scroll_x, scroll_y))


def draw_text(screen: pygame.Surface,
              text: str,
              font: pygame.font.Font,
              color: tuple[int, int, int],
              x_pos: int,
              y_pos: int,
              get_rect: bool = False) -> Union[None, pygame.Rect]:
    """
       Generic function to draw text on screen.

       Args:
           screen (pygame.Surface): Editor window.
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
    screen.blit(image,
                (x_pos, y_pos))
    if get_rect:
        rect = image.get_rect()
        return x_pos, y_pos, rect[2], rect[3]


def draw_text_centered_x(screen: pygame.Surface,
                         text: str,
                         font: pygame.font.Font,
                         color: tuple[int, int, int],
                         y_pos: int,
                         get_rect: bool = False):
    """
       Generic function to draw text on center of x-axis of screen.

       Args:
           screen (pygame.display): Editor window.
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
    screen.blit(image, ((SCREEN_WIDTH + RIGHT_MARGIN) // 2 - rect.width // 2, y_pos))

    if get_rect:
        centered_rect = image.get_rect()
        return centered_rect[0], y_pos, centered_rect[2], centered_rect[3]


def draw_change_name_text(screen: pygame.Surface,
                          map_name: str,
                          font: pygame.font.Font) -> None:
    """
        Blits change name text and name of the map to the screen.

        Args:
           screen (pygame.display): Editor window.
           map_name (str): Map name to blit to screen.
           font (pygame.font.Font): pygame.font object.

       Returns:
           None.
    """
    # Title
    draw_text_centered_x(screen=screen,
                         text=CHANGE_NAME_TEXT,
                         font=font,
                         y_pos=CHANGE_NAME_TITLE_Y_OFFSET,
                         color=CHANGE_NAME_TITLE_COLOR)

    # Name
    draw_text_centered_x(screen=screen,
                         text=map_name,
                         font=font,
                         y_pos=CHANGE_NAME_Y_OFFSET,
                         color=CHANGE_NAME_COLOR)


def draw_and_load_saved_maps_text(editor: any) -> None:
    """
        Checks maps folder to create and display a list of saved maps.
        Highlights name when collision with mouse.
        Loads selected map on click.

        Args:
            editor (any): Current Editor object.

        Returns:
            None.
    """
    saved_items = os.listdir(MAPS_DIR)

    # Draw map names
    for i, name in enumerate(saved_items):
        saved_map_text = draw_text(screen=editor.screen,
                                   text=name,
                                   font=editor.map_names_font,
                                   color=SAVED_MAPS_COLOR,
                                   x_pos=SAVED_MAPS_X_OFFSET,
                                   y_pos=i * SAVED_MAPS_Y_SPACING + SAVED_MAPS_Y_OFFSET,
                                   get_rect=True)

        saved_map_rect = pygame.Rect(saved_map_text)
        selection_map_rect = helpers.get_enlarged_rect(rect=saved_map_rect,
                                                       pixels=SAVED_MAPS_HIGHLIGHT_WIDTH)

        if selection_map_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(
                surface=editor.screen,
                color=SAVED_MAPS_HIGHLIGHT_COLOR,
                rect=(saved_map_text[0] - SAVED_MAPS_HIGHLIGHT_WIDTH,
                      saved_map_text[1] - SAVED_MAPS_HIGHLIGHT_WIDTH,
                      saved_map_text[2] + SAVED_MAPS_HIGHLIGHT_WIDTH * 2,
                      saved_map_text[3] + SAVED_MAPS_HIGHLIGHT_WIDTH * 2),
                width=5
            )

            if pygame.mouse.get_pressed()[0] == 1:
                # User selects a map
                helpers.load_map_details(editor=editor,
                                         map_name=name)

                time.sleep(0.1)  # to prevent placing tile

    if editor.back_button.draw(editor.screen):
        editor.is_loading_map = False
        editor.is_building = True
