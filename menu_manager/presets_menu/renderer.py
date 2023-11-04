from typing import Any, List

import pygame

from menu_manager.presets_menu import screens
from menu_manager.presets_menu import utis

from utilities import general
from utilities import buttons

from settings.buttons import SETS_BTN
from settings.panels import PRESETS_MAX_NAME_LENGTH


class PresetsMenuRenderer:

    def __init__(self,
                 menu_controller: Any):
        # References
        self.editor = menu_controller.editor
        self.menu_controller = menu_controller

        # Info
        self.preset_names: List[str] = utis.get_presets_dir_names()
        self.shortened_preset_names: List[str] = general.limit_string_length(
            string_list=self.preset_names,
            max_length=PRESETS_MAX_NAME_LENGTH
        )
        self.preset_names_outline_rects: List[pygame.rect.Rect] = []

        # Buttons
        self.sets_button = buttons.get_utility_button(editor=self.editor,
                                                      **SETS_BTN)

        # Trackers
        self.clicked = False

    def draw_presets_button(self) -> None:
        """
            Blits presets button to the screen.
        """
        if self.sets_button.draw():
            self.editor.is_displaying_presets = not self.editor.is_displaying_presets

    def draw_presets_menu(self) -> None:
        screens.display_preset_names(presets_renderer=self)
        screens.display_presets_previews(presets_renderer=self)
        selected_preset = screens.highlight_selected_preset(presets_renderer=self)
        if selected_preset is not None:
            self.editor.load_new_preset(selected_preset=selected_preset)
