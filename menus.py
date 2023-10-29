from dataclasses import dataclass, field
from typing import List, Union, Dict, OrderedDict, Tuple

import pygame

from settings.setup import *
from settings.paths import *

from settings.canvas import *
from settings.panels import *
from settings.menus import *
from settings.minimap import *

import utilities.text as drawing
import utilities.fonts as fonts
import utilities.general as general
import utilities.sprites as sprites
import utilities.helpers as helpers


@dataclass
class Menu:
    editor: any

    clicked = False

    preferences_dict: OrderedDict = field(
        default_factory=general.get_empty_ordered_dict
    )
    preferences_outline_recs: List[pygame.rect.Rect] = field(
        default_factory=general.get_empty_list
    )

    saved_map_names: List[str] = field(
        default_factory=general.get_saved_map_names
    )
    saved_maps_ouline_rects: List[pygame.rect.Rect] = field(
        default_factory=general.get_empty_list
    )

    preset_names: List[str] = field(
        default_factory=general.get_preset_dir_names
    )
    preset_names_outline_rects: List[pygame.rect.Rect] = field(
        default_factory=general.get_empty_list
    )

    def draw_preferences_menu(self) -> None:
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
            Highlights the preference if the user is currently hovering over.

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
                    self.editor.selected_preference_value_change = list(self.preferences_dict.items())[i][-1]
                    print(list(self.preferences_dict.items())[i])
                    print(self.editor._rows, self.editor._columns)

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

    def draw_load_map_menu(self) -> None:
        """
            Blits load map text and name of the maps to the screen.

            Uses:
               screen (pygame.display): Editor window.
               saved_map_names (str): Map names to blit to screen.
               font (pygame.font.Font): pygame.font object.

           Returns:
               None.
        """
        self.saved_map_names = general.get_saved_map_names()
        saved_maps_ouline_rects = []

        # Draw map names
        for i, name in enumerate(self.saved_map_names):
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
                            return self.saved_map_names[i]

                if pygame.mouse.get_pressed()[0] == 1:
                    self.clicked = True

                else:
                    self.clicked = False

        return None

    def draw_presets_menu(self) -> None:
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
