from collections import OrderedDict
from typing import Any

import pygame

from menu_manager.edit_menu import screens, actions
from menu_manager.edit_menu import utils

from utilities import buttons

from settings.buttons import EDIT_BTN, PREF_BTN, CROP_BTN, BACK_BTN_LARGE, OK_BTN_LARGE, WIPE_BTN
from settings.setup import DARK_ORANGE


class EditMenuRenderer:
    """
        Responsible for rendering all Edit Menu features and controlling the user interaction
            with the Editor.
        Draws Edit Menu buttons to the screen depending on MenuController state,
            sets the correct  MenuController state,
            loads the correct screen and
            applies changes to the Editor.
    """

    def __init__(self,
                 menu_controller: Any):
        # References
        self.editor = menu_controller.editor
        self.menu_controller = menu_controller
        self.popup_renderer = menu_controller.popup_renderer

        # Info
        self.preferences_dict: OrderedDict[str, int] = utils.get_preferences_dict(
            editor=self.menu_controller.editor
        )
        self.preferences_outline_recs: list[pygame.rect.Rect] = []

        # Buttons
        self.edit_button = buttons.get_utility_button(editor=self.editor,
                                                      **EDIT_BTN)
        self.pref_button = buttons.get_utility_button(editor=self.editor,
                                                      **PREF_BTN)
        self.crop_button = buttons.get_utility_button(editor=self.editor,
                                                      **CROP_BTN)
        self.wipe_button = buttons.get_utility_button(editor=self.editor,
                                                      **WIPE_BTN)

        self.back_button = buttons.get_utility_button(editor=self.editor,
                                                      **BACK_BTN_LARGE)
        self.ok_button = buttons.get_utility_button(editor=self.editor,
                                                    **OK_BTN_LARGE)

        # Trackers
        self.clicked = False

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

    def draw_edit_menu_button(self) -> None:
        """
            Draws the Edit Menu button to the screen and sets the MenuController state to
                the 'edit_menu' state if the user clicked on it.

            Returns:
                None.
        """
        if self.edit_button.draw():
            self.menu_controller.set_state("edit_menu")

    def draw_edit_menu(self) -> None:
        """
            Draws all buttons in the Edit Menu category to the screen and
                sets the MenuController state to the corresponding state if the user clicked on it.

            Returns:
                None
        """
        if self.pref_button.draw():
            actions.prepare_preferences_menu(editor=self.editor,
                                             edit_menu_renderer=self)
            self.menu_controller.set_state("close_sub_menus")
            self.menu_controller.set_state("changing_preferences")

        elif self.crop_button.draw():
            self.menu_controller.set_state("close_sub_menus")
            self.menu_controller.set_state("cropping_map")

        elif self.wipe_button.draw():
            self.menu_controller.set_state("close_sub_menus")
            self.menu_controller.set_state("wiping_map")

    def draw_preferences_menu(self) -> None:
        """
            Draws the preferences menu to the screen,
                listens for collision events between the mouse and the settings text,
                draws a select animation if a collision takes place,
                loads the selected preference for the user to edit (if so) and
                listens for user input.
            Draws OK and BACK buttons to the screen to apply or discard the changes
                and switch back to the correct state after.

            Returns:
                None.
        """
        self.editor.screen.fill(DARK_ORANGE)
        screens.display_preferences(menu_renderer=self)
        selected_preference = screens.highlight_and_return_selected_preference(menu_renderer=self)
        self.menu_controller.event_handler.get_preference_input()
        if selected_preference is not None:
            actions.load_selected_preference(editor=self.editor,
                                             selected_preference=selected_preference)

    def draw_crop_menu(self) -> None:
        """
            Draws the crop menu to the screen.
            Draws OK and BACK buttons to the screen to apply or discard the changes
                and switch back to the correct state after.
            Pressing OK wil result in the map being cropped on all sides until the first tile.

            Returns:
                None.
        """
        self.popup_renderer.display_popup_title(text=self.popup_renderer.crop_map_title)
        self.popup_renderer.display_popup_info(text=self.popup_renderer.crop_map_info)

        if self.popup_renderer.pressed_back_button():
            self.menu_controller.set_state("reset")

        if self.popup_renderer.pressed_ok_button():
            self.editor.world_data = utils.crop_world_data(world_data=self.editor.world_data)
            self.editor.rows = self.editor.world_data.shape[0]
            self.editor.columns = self.editor.world_data.shape[1]
            # self.editor.background = helpers.update_background(editor=self.editor)
            self.menu_controller.set_state("reset")

    def draw_wipe_menu(self) -> None:
        """
            Draws the wipe menu to the screen.
            Draws OK and BACK buttons to the screen to apply or discard the changes
                and switch back to the correct state after.
            Pressing OK wil result in the world_data being reset.

            Returns:
                None.
        """
        self.popup_renderer.display_popup_title(text=self.popup_renderer.wipe_map_title)
        self.popup_renderer.display_popup_info(text=self.popup_renderer.wipe_map_info)

        if self.popup_renderer.pressed_back_button():
            self.menu_controller.set_state("reset")

        if self.popup_renderer.pressed_ok_button():
            self.editor.wipe_map()
            self.menu_controller.set_state("reset")
