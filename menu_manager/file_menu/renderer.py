from typing import Any, List

import pygame

from menu_manager.file_menu import screens, actions
from menu_manager.file_menu import utils

from utilities import buttons

from settings.setup import DARK_ORANGE
from settings.buttons import FILE_BTN, SAVE_BTN, LOAD_BTN, NAME_BTN, NEW_BTN, BACK_BTN_LARGE, OK_BTN_LARGE


class FileMenuRenderer:
    """
        Responsible for rendering all File Menu features and controlling the user interaction
            with the Editor.
        Draws File Menu buttons to the screen depending on MenuController state,
            sets the correct  MenuController state,
            loads the correct screen and
            applies changes to the Editor.
    """

    def __init__(self,
                 menu_controller: Any):
        # References
        self.editor = menu_controller.editor
        self.menu_controller = menu_controller
        self.popup_renderer = self.menu_controller.popup_renderer

        # Info
        self.saved_maps_names: List[str] = utils.get_saved_maps_names()
        self.saved_maps_outline_rects: List[pygame.rect.Rect] = []
        self.selected_map: str = None

        # Buttons
        self.file_button = buttons.get_utility_button(editor=self.editor,
                                                      **FILE_BTN)
        self.save_button = buttons.get_utility_button(editor=self.editor,
                                                      **SAVE_BTN)
        self.load_button = buttons.get_utility_button(editor=self.editor,
                                                      **LOAD_BTN)
        self.name_button = buttons.get_utility_button(editor=self.editor,
                                                      **NAME_BTN)
        self.new_button = buttons.get_utility_button(editor=self.editor,
                                                     **NEW_BTN)

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

    def draw_file_menu_button(self) -> None:
        """
            Blits File Menu button to the screen and sets the state to 'file_menu' if
                the user clicks the button.

            Returns:
                None
        """
        if self.file_button.draw():
            self.menu_controller.set_state("file_menu")

    def draw_file_menu(self) -> None:
        """
            Draws all buttons in the File Menu category to the screen and
                sets the MenuController state to the corresponding state if the user clicked on it.

            Returns:
                None
        """
        if self.save_button.draw():
            self.menu_controller.set_state("close_sub_menus")
            self.menu_controller.set_state("saving_map")

        elif self.load_button.draw():
            self.menu_controller.set_state("close_sub_menus")
            self.menu_controller.set_state("loading_map")

        elif self.name_button.draw():
            self.menu_controller.set_state("close_sub_menus")
            self.menu_controller.set_state("renaming_map")

        elif self.new_button.draw():
            self.menu_controller.set_state("close_sub_menus")
            self.menu_controller.set_state("restarting_map")

    def draw_save_map_menu(self) -> None:
        """
            Draws save map menu to the screen.
            Draws OK and BACK buttons to the screen to apply or discard the changes
                and switch back to the correct state after.

            Returns:
                None.
        """
        self.popup_renderer.display_popup_title(text=self.popup_renderer.save_map_title)
        self.popup_renderer.display_popup_info(text=self.popup_renderer.save_map_info)

        self.menu_controller.event_handler.get_map_name_input2()
        self.popup_renderer.save_map_info = self.editor.temp_map_name

        if self.popup_renderer.pressed_back_button():
            self.editor.temp_map_name = self.editor.map_name
            self.menu_controller.set_state("reset")

        if self.popup_renderer.pressed_ok_button():
            self.editor.map_name = self.editor.temp_map_name
            actions.save_map(editor=self.editor)
            self.menu_controller.set_state("reset")

    def draw_load_map_menu(self) -> None:
        """
            Draws load map menu to the screen,
                draws names of all maps in the MAPS_DIR,
                highlights user selected/hovered map.
            Draws OK and BACK buttons to the screen to load map or discard the changes
                and switch back to the correct state after.

            Returns:
                None.
        """
        self.editor.screen.fill(DARK_ORANGE)
        screens.display_load_map(menu_renderer=self)

    def draw_rename_map_menu(self) -> None:
        """
            Draws rename map menu to the screen,
                draws name of the map,
                listens for user input to change the name.
            Draws OK and BACK buttons to the screen to save the name or discard the changes
                and switch back to the correct state after.

            Returns:
                None.
        """
        self.popup_renderer.display_popup_title(text=self.popup_renderer.rename_map_title)
        self.popup_renderer.display_popup_info(text=self.popup_renderer.rename_map_info)

        self.menu_controller.event_handler.get_map_name_input2()
        self.popup_renderer.rename_map_info = self.editor.temp_map_name

        if self.popup_renderer.pressed_back_button():
            self.editor.temp_map_name = self.editor.map_name
            self.menu_controller.set_state("reset")

        if self.popup_renderer.pressed_ok_button():
            self.editor.map_name = self.editor.temp_map_name
            self.menu_controller.set_state("reset")

    def draw_restart_map_menu(self) -> None:
        """
            Draws restart map menu to the screen.
            Draws OK and BACK buttons to the screen to restart the Editor or discard the changes
                and switch back to the correct state after.

            Returns:
                None.
        """
        self.popup_renderer.display_popup_title(text=self.popup_renderer.restart_map_title)
        self.popup_renderer.display_popup_info(text=self.popup_renderer.restart_map_info)

        if self.popup_renderer.pressed_back_button():
            self.menu_controller.set_state("reset")

        if self.popup_renderer.pressed_ok_button():
            self.editor.reload_editor()
            self.menu_controller.set_state("reset")
