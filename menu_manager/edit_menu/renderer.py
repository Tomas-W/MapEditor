from collections import OrderedDict
from typing import Any, List

import pygame

from menu_manager.edit_menu import screens
from menu_manager.edit_menu import utils

from utilities import buttons, helpers

from settings.buttons import EDIT_BTN, PREF_BTN, CROP_BTN, BACK_BTN, OK_BTN
from settings.setup import DARK_ORANGE


class EditMenuRenderer:
    """
        Responsible for rendering all Edit Menu features.
        Blits Edit Menu Category buttons to the screen,
            sets the correct Menu state in the MenuController and
            loads the correct screen.
    """

    def __init__(self,
                 menu_controller: Any):
        # References
        self.editor = menu_controller.editor
        self.menu_controller = menu_controller

        # Info
        self.preferences_dict: OrderedDict = utils.get_preferences_dict(
            editor=self.menu_controller.editor
        )
        self.preferences_outline_recs: List[pygame.rect.Rect] = []

        # Buttons
        self.edit_button = buttons.get_utility_button(editor=self.editor,
                                                      **EDIT_BTN)
        self.pref_button = buttons.get_utility_button(editor=self.editor,
                                                      **PREF_BTN)
        self.crop_button = buttons.get_utility_button(editor=self.editor,
                                                      **CROP_BTN)

        self.back_button = buttons.get_utility_button(editor=self.editor,
                                                      **BACK_BTN)
        self.ok_button = buttons.get_utility_button(editor=self.editor,
                                                    **OK_BTN)

        # Trackers
        self.clicked = False

    def draw_edit_menu_button(self) -> None:
        if self.edit_button.draw():
            self.menu_controller.set_state("edit_menu")

    def draw_edit_menu(self) -> None:
        if self.pref_button.draw():
            self.preferences_dict = utils.get_preferences_dict(editor=self.editor)
            self.editor.selected_preference_value = self.editor.rows
            self.editor.selected_preference_value_change = self.editor.rows
            self.menu_controller.set_state("changing_preferences")

        if self.crop_button.draw():
            self.menu_controller.set_state("cropping_map")

    def pressed_ok_button(self) -> bool:
        """
            Draws an OK button on the screen and returns True if the user clicked
                on it, False otherwise.

            Returns:
                bool: True if user clicked, False otherwise.
        """
        return self.ok_button.draw()

    def pressed_back_button(self) -> bool:
        """
            Draws a BACK button on the screen and returns True if the user clicked
                on it, False otherwise.

            Returns:
                bool: True if user clicked, False otherwise.
        """
        return self.back_button.draw()

    def draw_preferences_menu(self) -> None:
        self.editor.screen.fill(DARK_ORANGE)
        screens.display_preferences(menu_renderer=self)
        self.menu_controller.event_handler.get_preference_input()
        selected_preference = screens.highlight_selected_preference(menu_renderer=self)
        if selected_preference is not None:
            self.editor.selected_preference_name = selected_preference[0]
            self.editor.selected_preference_value = selected_preference[1]
            self.editor.selected_preference_value_change = self.editor.selected_preference_value

    def draw_crop_menu(self) -> None:
        self.editor.world_data = utils.crop_world_data(world_data=self.editor.world_data)
        self.editor.rows = len(self.editor.world_data)
        self.editor.columns = len(self.editor.world_data[0])
        self.editor.background = helpers.update_background(editor=self.editor)
        self.menu_controller.set_state("reset")
