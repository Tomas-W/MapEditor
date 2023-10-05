import os

import pygame
import pickle

from settings import *

EDITOR_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))

sky_img = pygame.image.load(os.path.join(EDITOR_DIR, "images/clouds.png")).convert()
background_img = pygame.image.load(os.path.join(EDITOR_DIR, "images/grass.png")).convert()


def get_sprites(location, number_sprites, width, height, scale):
    """
    Returns a list of individual sprites taken from the given sheet.

    :param location: Path to image file containing the sprites (png).
    :param number_sprites: Number of sprites to obtain (int).
    :param width: Sprite width in pixels (int).
    :param height: Sprite height in pixels (int).
    :param scale: Magnification in comparison with the original (int).

    :return: List of sprite images.
    """
    sprite_sheet = pygame.image.load(location).convert_alpha()

    sprites = []
    for i in range(0, number_sprites):
        image = pygame.Surface((width, height))
        image.blit(sprite_sheet, (0, 0), ((i * width), 0, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey((0, 0, 0))
        sprites.append(image)

    return sprites


def get_current_tab_sprites(tab_name):
    path = os.path.join(EDITOR_DIR, "images/presets", tab_name)
    sprite_names = [f for f in os.listdir(path) if f.endswith('.png') and os.path.isfile(os.path.join(path, f))]

    sprite_list = []
    for sprite in sprite_names:
        sprite_list.append(
            pygame.image.load(os.path.join(path, sprite)).convert_alpha()
        )

    return sprite_list

tile_list = get_sprites(location="images/hedge_sprites.png",
                        number_sprites=15,
                        width=32,
                        height=32,
                        scale=1)

save_image = pygame.image.load(os.path.join(EDITOR_DIR, "images/save_btn.png")).convert_alpha()
load_image = pygame.image.load(os.path.join(EDITOR_DIR, "images/load_btn.png")).convert_alpha()
back_image = pygame.image.load(os.path.join(EDITOR_DIR, "images/back_btn.png")).convert_alpha()
name_image = pygame.image.load(os.path.join(EDITOR_DIR, "images/name_btn.png")).convert_alpha()
back_button = pygame.image.load(os.path.join(EDITOR_DIR, "images/back_btn.png")).convert_alpha()


def get_all_level_objects(folder_path):
    # Create a dictionary to store images by their number
    all_level_objects = {}

    for subdir, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.png'):
                # Extract the number from the file name
                number = int(file.split('_')[0])

                # Load the image
                image = pygame.image.load(os.path.join(subdir, file)).convert_alpha()

                # Store the image by its number
                all_level_objects[number] = image

    return all_level_objects


def is_pickled(file_path):
    try:
        with open(file_path, "rb") as file:
            pickle.load(file)
        return True
    except (pickle.UnpicklingError, EOFError, FileNotFoundError):
        return False
