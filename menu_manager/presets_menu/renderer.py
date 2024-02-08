from typing import Any

import pygame

from menu_manager.presets_menu import screens, actions
from menu_manager.presets_menu import utis

from utilities import general
from utilities import buttons

from settings.buttons import SETS_BTN
from settings.presets import PRESETS_MAX_NAME_LENGTH


class PresetsMenuRenderer:

    def __init__(self,
                 menu_controller: Any):
        """
            Responsible for rendering all Preset Menu features and controlling the user interaction
                with the Editor.
            Draws Preset Menu buttons to the screen depending on MenuController state,
                sets the correct  MenuController state,
                loads the correct screen and
                applies changes to the Editor.
        """
        # References
        self.editor = menu_controller.editor
        self.menu_controller = menu_controller

        # Info
        self.preset_names: list[str] = utis.get_presets_dir_names()
        self.shortened_preset_names: list[str] = general.limit_string_length(
            string_list=self.preset_names,
            max_length=PRESETS_MAX_NAME_LENGTH
        )
        self.preset_names_outline_rects: list[pygame.rect.Rect] = []

        # Buttons
        self.sets_button = buttons.get_utility_button(editor=self.editor,
                                                      **SETS_BTN)

        # Trackers
        self.clicked = False

    def draw_presets_button(self) -> None:
        """
            Blits Preset Menu button to the screen and sets the state to 'preset_menu' if
                the user clicks the button.

            Returns:
                None
        """
        if self.sets_button.draw():
            self.menu_controller.set_state("preset_menu")

    def draw_presets_menu(self) -> None:
        """
            Draws Preset Menu to the screen,
                draws names of all presets in the PRESET_DIR,
                draws a preview image next to the name,
                highlights user selected/hovered preset and
                loads the preset the user selected.
            Menu is closed after selection or when the user clicks the Preset Menu
                button again.

            Returns:
                None.
        """
        screens.display_preset_names(presets_renderer=self)
        screens.display_presets_previews(presets_renderer=self)
        selected_preset = screens.highlight_selected_preset(presets_renderer=self)
        if selected_preset is not None:
            actions.load_new_preset(editor=self.editor,
                                    menu_controller=self.menu_controller,
                                    selected_preset=selected_preset)
