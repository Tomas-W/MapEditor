from collections import OrderedDict
from typing import Self, Any

import menu_manager.menu_screens as menu_screens
from settings.buttons import *
from settings.panels import *

import menu_manager.menu_utils as menu_utils

from utilities import buttons
from utilities import general
from utilities import helpers


class MenuRenderer:

    def __init__(self,
                 menu_controller: Any) -> Self:

        self.menu_controller = menu_controller
        self.editor = self.menu_controller.editor

        self.preferences_dict: OrderedDict = menu_utils.get_preferences_dict(
            editor=self.menu_controller.editor
        )
        self.preferences_outline_recs: List[pygame.rect.Rect] = []

        self.saved_maps_names: List[str] = menu_utils.get_saved_maps_names()
        self.saved_maps_outline_rects: List[pygame.rect.Rect] = []

        self.preset_names: List[str] = menu_utils.get_presets_dir_names()
        self.shortened_preset_names: List[str] = general.limit_string_length(
            string_list=self.preset_names,
            max_length=PRESETS_MAX_NAME_LENGTH
        )
        self.preset_names_outline_rects: List[pygame.rect.Rect] = []

        # Preset Menu
        self.sets_button = buttons.get_utility_button(editor=self.editor,
                                                      **SETS_BTN)
        # File Menu buttons
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

        # Edit Menu
        self.edit_button = buttons.get_utility_button(editor=self.editor,
                                                      **EDIT_BTN)
        self.pref_button = buttons.get_utility_button(editor=self.editor,
                                                      **PREF_BTN)
        self.crop_button = buttons.get_utility_button(editor=self.editor,
                                                      **CROP_BTN)

        # General Menu buttons
        self.back_button = buttons.get_utility_button(editor=self.editor,
                                                      **BACK_BTN)
        self.ok_button = buttons.get_utility_button(editor=self.editor,
                                                    **OK_BTN)

        self.clicked = False

    # ################################################### #
    # ##################### PRESETS ##################### #
    def draw_presets_button(self) -> None:
        """
            Blits presets button to the screen.
        """
        if self.sets_button.draw():
            self.editor.is_displaying_presets = not self.editor.is_displaying_presets

    def draw_presets_menu(self) -> None:
        menu_screens.display_presets(menu_renderer=self)
        menu_screens.display_presets_previews(menu_renderer=self)
        selected_preset = menu_screens.highlight_selected_preset(menu_renderer=self)
        if selected_preset is not None:
            self.editor.load_new_preset(selected_preset=selected_preset)

    # ################################################### #
    # ###################### MENUS ###################### #
    def draw_menu_buttons(self) -> None:
        if self.file_button.draw():
            self.menu_controller.set_state("file_menu")

        if self.edit_button.draw():
            self.menu_controller.set_state("edit_menu")

    def draw_file_menu(self) -> None:
        if self.save_button.draw():
            self.menu_controller.set_state("saving_map")

        if self.load_button.draw():
            self.menu_controller.set_state("loading_map")

        if self.name_button.draw():
            self.menu_controller.set_state("renaming_map")

        if self.new_button.draw():
            self.menu_controller.set_state("restart_map")

    def draw_edit_menu(self) -> None:
        if self.pref_button.draw():
            self.preferences_dict = menu_utils.get_preferences_dict(editor=self.editor)
            self.editor.selected_preference_value = self.editor.rows
            self.editor.selected_preference_value_change = self.editor.rows
            self.menu_controller.set_state("changing_preferences")

        if self.crop_button.draw():
            self.menu_controller.set_state("cropping_map")

    # ################################################### #
    # ################## MENU OPTIONS ################### #
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

    # ################################################### #
    # #################### FILE MENU #################### #
    def draw_save_map_menu(self) -> None:
        helpers.save_map_details(editor=self.editor)
        self.menu_controller.set_state("reset")

    def draw_load_map_menu(self) -> None:
        self.editor.screen.fill(DARK_ORANGE)
        menu_screens.display_load_map(menu_renderer=self)
        selected_map = menu_screens.highlight_selected_map(menu_renderer=self)
        if selected_map is not None:
            map_attributes = helpers.deserialize_map_details(editor=self.editor,
                                                             map_name=selected_map)
            helpers.update_class_dict(cls=self.editor,
                                      attributes=map_attributes)
            self.menu_controller.set_state("reset")

    def draw_rename_map_menu(self) -> None:
        self.editor.screen.fill(DARK_ORANGE)
        menu_screens.display_rename(menu_renderer=self)
        self.menu_controller.event_handler.get_map_name_input()

    def draw_restart_map_menu(self) -> None:
        self.menu_controller.set_state("restart_map")
        self.editor.restart_self()

    # ################################################### #
    # #################### EDIT MENU #################### #
    def draw_preferences_menu(self) -> None:
        self.editor.screen.fill(DARK_ORANGE)
        menu_screens.display_preferences(menu_renderer=self)
        self.menu_controller.event_handler.get_preference_input()
        selected_preference = menu_screens.highlight_selected_preference(menu_renderer=self)
        if selected_preference is not None:
            self.editor.selected_preference_name = selected_preference[0]
            self.editor.selected_preference_value = selected_preference[1]
            self.editor.selected_preference_value_change = self.editor.selected_preference_value

    def draw_crop_menu(self) -> None:
        self.editor.world_data = general.crop_world_data(world_data=self.editor.world_data)
        self.editor.rows = len(self.editor.world_data)
        self.editor.columns = len(self.editor.world_data[0])
        self.editor.background = helpers.update_background(editor=self.editor)
        self.menu_controller.set_state("reset")
