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
