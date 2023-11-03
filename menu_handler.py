from collections import OrderedDict
from typing import List, Union, Tuple, Self

from settings.buttons import *
from settings.paths import *

from settings.panels import *
from settings.menus import *
from settings.minimap import *

import utilities.buttons as buttons
import utilities.drawing as drawing
import utilities.fonts as fonts
import utilities.general as general
import utilities.sprites as sprites
import utilities.helpers as helpers


class MenuHandler:
    def __init__(self,
                 editor: any) -> Self:
        self.editor = editor
        self.event_handler = self.editor.event_handler

        self.preferences_dict: OrderedDict = self.get_preferences_dict()
        self.preferences_outline_recs: List[pygame.rect.Rect] = []

        self.saved_maps_names: List[str] = self.get_saved_maps_names()
        self.saved_maps_ouline_rects: List[pygame.rect.Rect] = []

        self.preset_names: List[str] = self.get_presets_dir_names()
        self.shortened_preset_names: List[str] = self.get_shortened_presets_dir_names()
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

        self.is_saving_map = False
        self.is_loading_map = False
        self.is_renaming_map = False
        self.is_restarting_map = False

        self.is_changing_preferences = False
        self.is_cropping_map = False

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
                self.editor.is_building = True

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

            case "changing_prefs":
                self.set_state("reset")
                self.editor.is_building = False
                self.is_changing_preferences = True

            case "cropping_map":
                self.set_state("reset")
                self.editor.is_building = False
                self.is_cropping_map = True

    def run(self) -> None:

        self.draw_presets_button()
        self.draw_menu_buttons()

        if self.editor.is_displaying_presets:
            self.draw_presets_menu()

        if self.editor.is_in_file_menu:
            self.draw_file_menu()

        elif self.editor.is_in_edit_menu:
            self.draw_edit_menu()

        if self.is_saving_map:
            self.draw_save_map_menu()

        elif self.is_loading_map:
            self.draw_load_map_menu()

        elif self.is_restarting_map:
            self.draw_restart_map_menu()

        elif self.is_renaming_map:
            self.draw_rename_map_menu()

        elif self.is_changing_preferences:
            self.draw_preferences_menu()

        elif self.is_cropping_map:
            self.draw_crop_menu()

# ################################################### #
# ##################### PRESETS ##################### #
    def draw_presets_button(self) -> None:
        """
            Blits presets button to the screen.
        """
        if self.sets_button.draw():
            self.editor.is_displaying_presets = not self.editor.is_displaying_presets

    def draw_presets_menu(self) -> None:
        self.display_presets()
        self.display_presets_previews()
        selected_preset = self.highlight_selected_preset()
        if selected_preset is not None:
            self.editor.load_new_preset(selected_preset=selected_preset)

# ################################################### #
# ###################### MENUS ###################### #
    def draw_menu_buttons(self) -> None:
        if self.file_button.draw():
            self.set_state("file_menu")

        if self.edit_button.draw():
            self.set_state("edit_menu")

    def draw_file_menu(self) -> None:
        if self.save_button.draw():
            self.set_state("saving_map")

        if self.load_button.draw():
            self.set_state("loading_map")

        if self.name_button.draw():
            self.set_state("renaming_map")

        if self.new_button.draw():
            self.set_state("restart_map")

    def draw_edit_menu(self) -> None:
        if self.pref_button.draw():
            self.preferences_dict = self.get_preferences_dict()
            self.editor.selected_preference_value = self.editor.rows
            self.editor.selected_preference_value_change = self.editor.rows
            self.set_state("changing_prefs")

        if self.crop_button.draw():
            self.set_state("cropping_map")

# ################################################### #
# #################### FILE MENU #################### #
    def draw_save_map_menu(self) -> None:
        helpers.save_map_details(editor=self.editor)
        self.set_state("reset")

    def draw_load_map_menu(self) -> None:
        self.editor.screen.fill(DARK_ORANGE)
        self.display_map_names()
        selected_map = self.highlight_selected_map()
        if selected_map is not None:
            map_attributes = helpers.deserialize_map_details(editor=self.editor,
                                                             map_name=selected_map)
            helpers.update_class_dict(cls=self.editor,
                                      attributes=map_attributes)
            self.is_loading_map = False
            self.editor.is_building = True

    def draw_rename_map_menu(self) -> None:
        self.editor.screen.fill(DARK_ORANGE)
        self.draw_rename_menu()
        self.event_handler.get_map_name_input()
        self.draw_map_name_btns()

    def draw_restart_map_menu(self) -> None:
        self.set_state("restart_map")
        self.editor.restart_self()

# ################################################### #
# #################### EDIT MENU #################### #
    def draw_preferences_menu(self) -> None:
        self.editor.screen.fill(DARK_ORANGE)
        self.display_preferences()
        self.event_handler.get_preference_input()
        self.draw_preference_buttons()
        selected_preference = self.highlight_selected_preference()
        if selected_preference is not None:
            self.editor.selected_preference_name = selected_preference[0]
            self.editor.selected_preference_value = selected_preference[1]
            self.editor.selected_preference_value_change = self.editor.selected_preference_value

    def draw_crop_menu(self) -> None:
        self.editor.world_data = general.crop_world_data(world_data=self.editor.world_data)
        self.editor.rows = len(self.editor.world_data)
        self.editor.columns = len(self.editor.world_data[0])
        self.editor.background = helpers.update_background(editor=self.editor)

    def draw_preference_buttons(self) -> None:
        # Do not save value and go back
        if self.back_button.draw():
            self.set_state("reset")

            helpers.update_world_data_size(editor=self.editor)

        # Save new value
        if self.ok_button.draw():
            if general.is_new_value_allowed(name=self.editor.selected_preference_name,
                                            value=int(
                                                self.editor.selected_preference_value_change)):
                print(
                    f"{self.editor.selected_preference_name} changed from {self.editor.selected_preference_value} to {self.editor.selected_preference_value_change}")
                self.editor.selected_preference_value = self.editor.selected_preference_value_change

                attributes_dict = {
                    self.editor.selected_preference_name: int(self.editor.selected_preference_value)
                }
                helpers.update_class_dict(cls=self.editor,
                                          attributes=attributes_dict)
                self.editor.background = helpers.update_background(editor=self.editor)
                self.editor.menu_handler.preferences_dict = self.get_preferences_dict()

            else:
                print(
                    f"name: '{self.editor.selected_preference_name}' cannot be value: '{self.editor.selected_preference_value_change}"'')

    def draw_map_name_btns(self):
        # Do not save new map name
        if self.back_button.draw():
            self.editor.temp_map_name = self.editor.map_name
            self.set_state("reset")

        # Save new map name
        if self.ok_button.draw():
            self.editor.map_name = self.editor.temp_map_name
            self.set_state("reset")

    def get_preferences_dict(self) -> OrderedDict[str, int]:
        preferences_dict: OrderedDict[str, int] = OrderedDict([
            ("rows", self.editor.rows),
            ("columns", self.editor.columns),
            ("grid_size_x", self.editor.grid_size_x),
            ("grid_size_y", self.editor.grid_size_y)])
        return preferences_dict

    @staticmethod
    def get_saved_maps_names() -> List[str]:
        """
            Get a list with the name of the saved maps in the maps folder.

            Returns:
                 List[str]: Names of al saved maps.
        """
        return os.listdir(MAPS_DIR)

    @staticmethod
    def get_presets_dir_names() -> List[str]:
        """
           Get a list of folders in the 'presets' folder.

           Returns:
               List[str]: List of names of folders in 'presets' folder.
           """
        return sorted([f.name for f in os.scandir(PRESET_DIR) if f.is_dir()])

    def get_shortened_presets_dir_names(self) -> List[str]:
        """
           Get a list of folders in the 'presets' folder and returns a list where
            the names have been capped to 15 and have trailing '..'

           Returns:
               List[str]: List of names of shortened folders in 'presets' folder.
           """
        names = self.preset_names

        for i, name in enumerate(names):
            if len(name) > PRESETS_MAX_NAME_LENGTH:
                names[i] = name[:PRESETS_MAX_NAME_LENGTH - 1] + ".."

        return names

    def display_preferences(self) -> None:
        """
            Blits preferences text and value to the screen.

            Uses:
               screen (pygame.display): Editor window.
               font (pygame.font.Font): pygame.font object.

           Returns:
               None.
        """
        preferences_outline_recs = []
        # Preferences
        for i, (key, val) in enumerate(self.preferences_dict.items()):
            preference = drawing.draw(screen=self.editor.screen,
                                      text=str(key),
                                      font=fonts.preferences_font,
                                      color=PREFERENCES_HIGHLIGHT_WIDTH,
                                      x_pos=PREFERENCES_X,
                                      y_pos=i * PREFERENCES_Y_SPACING + PREFERENCES_Y,
                                      get_rect=True)

            preference_rect = pygame.Rect(preference)
            preference_outline_rect = helpers.get_enlarged_rect(rect=preference_rect,
                                                                pixels=PREFERENCES_HIGHLIGHT_WIDTH)
            preferences_outline_recs.append(preference_outline_rect)

        self.preferences_outline_recs = preferences_outline_recs

        # Selected preference key
        drawing.draw_centered_x(screen=self.editor.screen,
                                text=str(self.editor.selected_preference_name),
                                font=fonts.preferences_font,
                                color=WHITE,
                                y_pos=SELECTED_PREFERENCE_KEY_Y,
                                get_rect=False
                                )

        # Selected preference vale
        drawing.draw_centered_x(screen=self.editor.screen,
                                text=str(self.editor.selected_preference_value_change),
                                font=fonts.preferences_font,
                                color=WHITE,
                                y_pos=SELECTED_PREFERENCE_VAL_Y,
                                get_rect=False
                                )

    def highlight_selected_preference(self) -> Union[None, Tuple[str, int]]:
        """
            Highlights the preference the user is currently hovering over.

            Uses:
               screen (pygame.display): Editor window.
               saved_maps_outline_rects (list): All recs containing the preferences.

           Returns:
               Union[None, Tuple[str, int]].
        """
        for i, outline_rect in enumerate(self.preferences_outline_recs):
            if outline_rect.collidepoint(self.editor.mouse_pos):
                pygame.draw.rect(
                    surface=self.editor.screen,
                    color=PREFERENCES_COLOR,
                    rect=outline_rect,
                    width=5
                )
                if pygame.mouse.get_pressed()[0] == 1:
                    self.editor.selected_preference_value_change = \
                        list(self.preferences_dict.items())[i][-1]

                    return list(self.preferences_dict.items())[i]

        return None

    def draw_rename_menu(self) -> None:
        """
            Blits change name text and name of the map to the screen.

            Uses:
               screen (pygame.display): Editor window.
               temp_map_name (str): Map name to blit to screen.
               font (pygame.font.Font): pygame.font object.

           Returns:
               None.
        """
        # Title
        drawing.draw_centered_x(screen=self.editor.screen,
                                text=str(CHANGE_NAME_TEXT),
                                font=fonts.load_map_font,
                                y_pos=CHANGE_NAME_TITLE_Y,
                                color=CHANGE_NAME_TITLE_COLOR)

        # Name
        drawing.draw_centered_x(screen=self.editor.screen,
                                text=str(self.editor.temp_map_name),
                                font=fonts.load_map_font,
                                y_pos=CHANGE_NAME_Y,
                                color=CHANGE_NAME_COLOR)

    def display_map_names(self) -> None:
        """
            Blits load map text and name of the maps to the screen.

            Uses:
               screen (pygame.display): Editor window.
               saved_map_names (str): Map names to blit to screen.
               font (pygame.font.Font): pygame.font object.

           Returns:
               None.
        """
        self.saved_maps_names = self.get_saved_maps_names()
        saved_maps_ouline_rects = []

        # Draw map names
        for i, name in enumerate(self.saved_maps_names):
            saved_map_text = drawing.draw(screen=self.editor.screen,
                                          text=str(name),
                                          font=fonts.load_map_font,
                                          color=SAVED_MAPS_COLOR,
                                          x_pos=SAVED_MAPS_X,
                                          y_pos=i * SAVED_MAPS_Y_SPACING + SAVED_MAPS_Y,
                                          get_rect=True)

            saved_map_rect = pygame.Rect(saved_map_text)
            selection_map_rect = helpers.get_enlarged_rect(rect=saved_map_rect,
                                                           pixels=SAVED_MAPS_HIGHLIGHT_WIDTH * 2)
            saved_maps_ouline_rects.append(selection_map_rect)

        self.saved_maps_ouline_rects = saved_maps_ouline_rects

    def highlight_selected_map(self) -> Union[None, str]:
        """
            Highlights the map if the user is currently hovering over.

            Uses:
               screen (pygame.display): Editor window.
               saved_maps_outline_rects (list): All recs containing the maps.

           Returns:
               Union[None, str].
        """
        for i, outline_rect in enumerate(self.saved_maps_ouline_rects):
            if outline_rect.collidepoint(self.editor.mouse_pos):
                pygame.draw.rect(
                    surface=self.editor.screen,
                    color=SAVED_MAPS_HIGHLIGHT_COLOR,
                    rect=outline_rect,
                    width=SAVED_MAPS_HIGHLIGHT_WIDTH
                )
                if self.clicked:
                    for event in self.editor.events:
                        if event.type == pygame.MOUSEBUTTONUP:
                            return self.saved_maps_names[i]

                if pygame.mouse.get_pressed()[0] == 1:
                    self.clicked = True

                else:
                    self.clicked = False

        return None

    def display_presets(self) -> None:
        """
            Blits presets menu to the screen.

            Uses:
               screen (pygame.display): Editor window.
               preset_names (str): Preset names to blit to screen.
               presets_font (pygame.font.Font): pygame.font object.

           Returns:
               None.
        """
        presets_rects_outlines = []

        for i, name in enumerate(self.preset_names):
            text_pos = drawing.draw(screen=self.editor.screen,
                                    text=str(name),
                                    font=fonts.presets_font,
                                    color=PRESETS_NAME_COLOR,
                                    x_pos=PRESETS_NAME_X_OFFSET,
                                    y_pos=PRESETS_NAME_Y_OFFSET + i * PRESETS_NAME_Y_SPACING,
                                    get_rect=True)

            text_rect = pygame.rect.Rect(text_pos)
            text_rect[2] = SCREEN_WIDTH + RIGHT_MARGIN - text_rect[0]

            presets_rects_outlines.append(text_rect)

        self.preset_names_outline_rects = presets_rects_outlines

    def display_presets_previews(self) -> None:
        """
            Shows a preview of the first image in the displayed presets-folder next to its name.

            Returns:
                None
        """
        for i, name in enumerate(self.preset_names):
            preview_img = pygame.transform.scale(
                surface=sprites.get_preview_image(preset_name=name),
                size=(PREVIEW_WIDTH,
                      PREVIEW_HEIGHT))
            self.editor.screen.blit(source=preview_img,
                                    dest=(
                                        PREVIEW_X,
                                        PREVIEW_Y + i * PRESETS_NAME_Y_SPACING
                                    ))

    def highlight_selected_preset(self) -> Union[None, str]:
        """
            Highlights the preset if the user is currently hovering over.

            Uses:
               screen (pygame.display): Editor window.
               preset_name_rects_outlines (str): All preset outline rects.

           Returns:
               None.
        """
        for i, outline_rect in enumerate(self.preset_names_outline_rects):

            if outline_rect.collidepoint(self.editor.mouse_pos):
                pygame.draw.rect(
                    surface=self.editor.screen,
                    color=PRESETS_HIGHLIGHT_COLOR,
                    rect=(outline_rect[0] + PRESETS_HIGHLIGHT_LEFT_OFFSET,
                          outline_rect[1] + PRESETS_HIGHLIGHT_TOP_OFFSET * 1.5,
                          outline_rect[2] - 16,
                          outline_rect[3] + PRESETS_HIGHLIGHT_BOTTOM_OFFSET * 3),
                    width=PRESETS_HIGHLIGHT_WIDTH
                )

                if self.clicked:
                    for event in self.editor.events:
                        if event.type == pygame.MOUSEBUTTONUP:
                            return self.preset_names[i]

                if pygame.mouse.get_pressed()[0] == 1:
                    self.clicked = True

                else:
                    self.clicked = False

        return None
