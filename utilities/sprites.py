import pygame
import pickle
from typing import List, Dict

from settings import *

EDITOR_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))

sky_img = pygame.image.load(os.path.join(EDITOR_DIR, "images/clouds.png")).convert()
background_img = pygame.image.load(os.path.join(EDITOR_DIR, "images/grass.png")).convert()


def get_sprites(location: str,
                number_sprites: int,
                width: int,
                height: int,
                scale: int) -> List[pygame.Surface]:
    """
        Returns a list of individual sprites taken from the given sheet.

        Args:
            location (str): Path to image file containing the sprites (png).
            number_sprites (int): Number of sprites to obtain.
            width (int): Sprite width in pixels.
            height (int): Sprite height in pixels.
            scale (int): Scaling in comparison with the original.

        Returns:
            List[pygame.Surface]: List of sprite images.
    """
    sprite_sheet = pygame.image.load(location).convert_alpha()

    sprites = []
    for i in range(0, number_sprites):
        image = pygame.Surface((width, height))
        image.blit(sprite_sheet, (0, 0), ((i * width), 0, width, height))
        if not scale == 1:
            image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey((0, 0, 0))
        sprites.append(image)

    return sprites


def get_current_tab_sprites(tab_name: str) -> List[pygame.Surface]:
    """
        Get a list of sprites for the current tab.

        Args:
            tab_name (str): Name of the current tab.

        Returns:
            List[pygame.Surface]: List of sprite images.
        """
    path = os.path.join(EDITOR_DIR, "images/presets", tab_name)
    sprite_names = [f for f in os.listdir(path) if f.endswith('.png') and os.path.isfile(os.path.join(path, f))]

    sprite_list = []
    for sprite in sprite_names:
        sprite_list.append(
            pygame.image.load(os.path.join(path, sprite)).convert_alpha()
        )

    return sprite_list


save_button_image = pygame.image.load(os.path.join(EDITOR_DIR, "images/save_btn.png")).convert_alpha()
load_button_image = pygame.image.load(os.path.join(EDITOR_DIR, "images/load_btn.png")).convert_alpha()
back_button_image = pygame.image.load(os.path.join(EDITOR_DIR, "images/back_btn.png")).convert_alpha()
name_button_image = pygame.image.load(os.path.join(EDITOR_DIR, "images/name_btn.png")).convert_alpha()
ok_button_image = pygame.image.load(os.path.join(EDITOR_DIR, "images/ok_btn.png")).convert_alpha()


def get_all_level_objects(folder_path: str) -> Dict[int, pygame.Surface]:
    """
        Get all level objects from a folder.

        Args:
            folder_path (str): Path to the folder containing level objects.

        Returns:
            dict: A dictionary with level objects indexed by number.
        """
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


def is_pickled(file_path: str) -> bool:
    """
        Check if a file is pickled.

        Args:
            file_path (str): Path to the file.

        Returns:
            bool: True if the file is pickled, False otherwise.
        """
    try:
        with open(file_path, "rb") as file:
            pickle.load(file)
        return True

    except (pickle.UnpicklingError, EOFError, FileNotFoundError):
        return False
