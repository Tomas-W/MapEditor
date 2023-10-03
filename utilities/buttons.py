import pygame

from utilities.sprites import tile_list, save_image, load_image, back_image, name_image
from settings import *


class Button:
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):
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


def get_tile_buttons():
    button_list = []
    button_col = 0
    button_row = 0
    for i in range(len(tile_list)):
        tile_button = Button(x=SCREEN_WIDTH + (85 * button_col + 50),
                             y=110 * button_row + 40,
                             image=tile_list[i],
                             scale=1)
        button_list.append(tile_button)
        button_col += 1
        if button_col == 3:
            button_row += 1
            button_col = 0

    return button_list


def get_save_button():
    return Button(15,
                  y=SCREEN_HEIGHT + 15,
                  image=save_image,
                  scale=1)


def get_load_button():
    return Button(x=15,
                  y=SCREEN_HEIGHT + 60,
                  image=load_image,
                  scale=1)


def get_name_button():
    return Button(x=15,
                  y=SCREEN_HEIGHT + 105,
                  image=name_image,
                  scale=1)


def get_back_button():
    return Button(x=(SCREEN_WIDTH + RIGHT_MARGIN) // 2 - 32,
                  y=SCREEN_HEIGHT + BOTTOM_MARGIN - 50,
                  image=back_image,
                  scale=1)
