from typing import Any, Self

from menu_manager.presets_menu.renderer import PresetsMenuRenderer
from menu_manager.file_menu.renderer import FileMenuRenderer
from menu_manager.edit_menu.renderer import EditMenuRenderer


class MenuController:
    """
        Top level class of Menu management. Responsible for all menus throughout the Editor.
        Blits Menu Category buttons to the screen,
            keeps track of all states and
             calls the correct MenuRenderer to handle the menu itself.

        Args:
            editor (Any): Current Editor instance.

        Returns:
            Self.
    """
    def __init__(self,
                 editor: Any) -> Self:
        # References
        self.editor = editor
        self.event_handler = self.editor.event_handler

        # States
        self.is_saving_map = False
        self.is_loading_map = False
        self.is_renaming_map = False
        self.is_restarting_map = False

        self.is_changing_preferences = False
        self.is_cropping_map = False

        # Renderers
        self.presets_renderer = PresetsMenuRenderer(menu_controller=self)
        self.file_menu_renderer = FileMenuRenderer(menu_controller=self)
        self.edit_menu_renderer = EditMenuRenderer(menu_controller=self)

    def set_state(self,
                  state: str) -> None:
        """
            Checks provided state and sets all Menu state attributes to their pre-set values.

            Returns:
                None
        """
        match state:

            case "reset":
                self.editor.is_building = True

                self.is_saving_map = False
                self.is_loading_map = False
                self.is_renaming_map = False
                self.is_restarting_map = False

                self.is_changing_preferences = False
                self.is_cropping_map = False

            case "building":
                self.set_state("reset")

            case "file_menu":
                self.editor.is_in_file_menu = not self.editor.is_in_file_menu
                self.editor.is_in_edit_menu = False

            case "edit_menu":
                self.editor.is_in_edit_menu = not self.editor.is_in_edit_menu
                self.editor.is_in_file_menu = False

            case "saving_map":
                self.set_state("reset")
                self.editor.is_building = False
                self.is_saving_map = True

            case "loading_map":
                self.set_state("reset")
                self.editor.is_building = False
                self.is_loading_map = True

            case "renaming_map":
                self.set_state("reset")
                self.editor.is_building = False
                self.is_renaming_map = True

            case "restart_map":
                self.is_restarting_map = not self.is_restarting_map

            case "changing_preferences":
                self.set_state("reset")
                self.editor.is_building = False
                self.is_changing_preferences = True

            case "cropping_map":
                self.set_state("reset")
                self.is_cropping_map = True

    def run(self) -> None:
        """
            Main function of the MenuController.
            Checks the current Menu state and calls the correct MenuRenderer to handle
                the menu itself.

             Returns:
                 None
        """
        # Presets
        self.presets_renderer.draw_presets_button()

        if self.editor.is_displaying_presets:
            self.presets_renderer.draw_presets_menu()

        # File Menu
        self.file_menu_renderer.draw_file_menu_button()

        if self.editor.is_in_file_menu:
            self.file_menu_renderer.draw_file_menu()

        if self.is_saving_map:
            self.file_menu_renderer.draw_save_map_menu()

        elif self.is_loading_map:
            self.file_menu_renderer.draw_load_map_menu()

        elif self.is_restarting_map:
            self.file_menu_renderer.draw_restart_map_menu()

        elif self.is_renaming_map:
            self.file_menu_renderer.draw_rename_map_menu()

        # Edit Menu
        self.edit_menu_renderer.draw_edit_menu_button()

        if self.editor.is_in_edit_menu:
            self.edit_menu_renderer.draw_edit_menu()

        if self.is_changing_preferences:
            self.edit_menu_renderer.draw_preferences_menu()

        elif self.is_cropping_map:
            self.edit_menu_renderer.draw_crop_menu()
