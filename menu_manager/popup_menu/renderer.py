from typing import Any

import utilities.buttons as buttons
import utilities.fonts as fonts
import utilities.render_text as render_text
import utilities.general as utilities

from settings.buttons import BACK_BTN_SMALL, OK_BTN_SMALL
from settings.menus import *


class PopupMenuRenderer:
    """
        Responsible for rendering all Popup Menu features and controlling the user interaction
            with the Editor.
        Draws BACK and OKE buttons to the screen with the appropriate text.
    """

    def __init__(self,
                 menu_controller: Any):
        # References
        self.editor = menu_controller.editor
        self.menu_controller = menu_controller

        utilities.limit_string_length(string_list=list(self.editor.map_name),
                                      max_length=15)

        self.rename_map_title = "Rename map"
        self.rename_map_info = self.editor.temp_map_name

        self.save_map_title = "Save map"
        self.save_map_info = self.editor.temp_map_name

        self.restart_map_title = "Restart Editor"
        self.restart_map_info = "Resets all settings to their default."

        self.crop_map_title = "Crop map"
        self.crop_map_info = "Removes all unused outer columns and rows."

        self.wipe_map_title = "Restart map"
        self.wipe_map_info = "Removes all tiles from the map."

        self.back_button = buttons.get_utility_button(editor=self.editor,
                                                      **BACK_BTN_SMALL)
        self.ok_button = buttons.get_utility_button(editor=self.editor,
                                                    **OK_BTN_SMALL)

        # Trackers
        self.clicked = False

    def set_save_map_info(self) -> None:
        self.save_map_info = f"{utilities.limit_string_length(string_list=self.editor.map_name, max_length=15)}"

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

    def display_popup_title(self,
                            text: str) -> None:
        render_text.centered_x(screen=self.editor.screen,
                               text=text,
                               font=fonts.popup_font,
                               color=POPUP_MENU_COLOR,
                               y_pos=POPUP_MENU_TITLE_Y,
                               full_width=False)

    def display_popup_info(self,
                           text: str) -> None:
        render_text.centered_x(screen=self.editor.screen,
                               text=text,
                               font=fonts.popup_font,
                               color=POPUP_MENU_COLOR,
                               y_pos=POPUP_MENU_INFO_Y,
                               full_width=False)
