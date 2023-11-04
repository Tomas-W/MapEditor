from typing import Self

from .menu_renderer import MenuRenderer


class MenuController:
    def __init__(self,
                 editor: any) -> Self:
        self.editor = editor
        self.event_handler = self.editor.event_handler

        self.is_saving_map = False
        self.is_loading_map = False
        self.is_renaming_map = False
        self.is_restarting_map = False

        self.is_changing_preferences = False
        self.is_cropping_map = False

        self.menu_renderer = MenuRenderer(menu_controller=self)

    def set_state(self,
                  state: str) -> None:
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
        # Presets
        self.menu_renderer.draw_presets_button()
        if self.editor.is_displaying_presets:
            self.menu_renderer.draw_presets_menu()

        # Menu buttons
        self.menu_renderer.draw_menu_buttons()

        if self.editor.is_in_file_menu:
            self.menu_renderer.draw_file_menu()

        elif self.editor.is_in_edit_menu:
            self.menu_renderer.draw_edit_menu()

        # File Menu
        if self.is_saving_map:
            self.menu_renderer.draw_save_map_menu()

        elif self.is_loading_map:
            self.menu_renderer.draw_load_map_menu()

        elif self.is_restarting_map:
            self.menu_renderer.draw_restart_map_menu()

        elif self.is_renaming_map:
            self.menu_renderer.draw_rename_map_menu()

        # Edit Menu
        elif self.is_changing_preferences:
            self.menu_renderer.draw_preferences_menu()

        elif self.is_cropping_map:
            self.menu_renderer.draw_crop_menu()
