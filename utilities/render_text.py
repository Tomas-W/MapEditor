from typing import Union, Tuple

import pygame

from settings.setup import *


def position(screen: pygame.Surface,
             text: str,
             font: pygame.font.Font,
             color: Tuple[int, int, int],
             x_pos: int,
             y_pos: int,
             get_rect: bool = False) -> Union[None, pygame.Rect]:
    """
       Generic function to draw text on screen at given position.

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


def centered_x(screen: pygame.Surface,
               text: str,
               font: pygame.font.Font,
               color: Tuple[int, int, int],
               y_pos: int,
               full_width: bool = True,
               get_rect: bool = False):
    """
       Generic function to draw text on center of x-axis of screen.

       Args:
           screen (pygame.display): Editor window.
           text (str): Text to blit to screen.
           font (pygame.font.Font): pygame.font object.
           color (tuple[int, int, int]): Text color in RGB format.
           y_pos (int): Text y-position.
           full_width (bool): Center of whole screen (True) or center of view area (False).
           get_rect (bool, optional): Flag to indicate if position information is needed.
               Default is False.

       Returns:
           None or Tuple[int, int, int, int]: If get_pos is True, returns a tuple containing
               (x-position, y-position, width, height) of the rendered text.
               Otherwise, returns None.
    """
    if full_width:
        image = font.render(text, True, color)
        rect = image.get_rect()
        screen.blit(image, ((SCREEN_WIDTH + RIGHT_MARGIN) // 2 - rect.width // 2, y_pos))

    else:
        image = font.render(text, True, color)
        rect = image.get_rect()
        screen.blit(image, (SCREEN_WIDTH // 2 - rect.width // 2, y_pos))

    if get_rect:
        centered_rect = image.get_rect()
        return centered_rect[0], y_pos, centered_rect[2], centered_rect[3]
