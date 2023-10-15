from dataclasses import dataclass, field
from typing import List, Union

import pygame

from settings import bottom_panel, canvas, minimap, paths, right_panel, setup

import utilities.drawing as drawing
import utilities.fonts as fonts
import utilities.sprites as sprites
import utilities.helpers as helpers


@dataclass
class Menu:
    editor: any

    saved_map_names: List[str] = field(default_factory=helpers.get_saved_map_names)
    saved_maps_ouline_rects: List[pygame.rect.Rect] = field(default_factory=helpers.get_empty_list)

    preset_names: List[str] = field(default_factory=helpers.get_preset_dir_names)
    preset_name_rects_outlines: List[pygame.rect.Rect] = field(
        default_factory=helpers.get_empty_list)

    def draw_settings_menu(self) -> None:
        pass

    def draw_rename_menu(self) -> None:
        """
            Blits change name text and name of the map to the screen.

            Uses:
               screen (pygame.display): Editor window.
               map_name (str): Map name to blit to screen.
               font (pygame.font.Font): pygame.font object.

           Returns:
               None.
        """
        # Title
        drawing.draw_text_centered_x(screen=self.editor.screen,
                                     text=canvas.CHANGE_NAME_TEXT,
                                     font=fonts.load_map_font,
                                     y_pos=canvas.CHANGE_NAME_TITLE_Y_OFFSET,
                                     color=canvas.CHANGE_NAME_TITLE_COLOR)

        # Name
        drawing.draw_text_centered_x(screen=self.editor.screen,
                                     text=self.editor.temp_map_name,
                                     font=fonts.load_map_font,
                                     y_pos=canvas.CHANGE_NAME_Y_OFFSET,
                                     color=canvas.CHANGE_NAME_COLOR)

    def draw_load_map_menu(self):
        self.saved_map_names = helpers.get_saved_map_names()
        saved_maps_ouline_rects = []

        # Draw map names
        for i, name in enumerate(self.saved_map_names):
            saved_map_text = drawing.draw_text(screen=self.editor.screen,
                                               text=name,
                                               font=fonts.load_map_font,
                                               color=canvas.SAVED_MAPS_COLOR,
                                               x_pos=canvas.SAVED_MAPS_X_OFFSET,
                                               y_pos=i * canvas.SAVED_MAPS_Y_SPACING + canvas.SAVED_MAPS_Y_OFFSET,
                                               get_rect=True)

            saved_map_rect = pygame.Rect(saved_map_text)
            selection_map_rect = helpers.get_enlarged_rect(rect=saved_map_rect,
                                                           pixels=canvas.SAVED_MAPS_HIGHLIGHT_WIDTH)
            saved_maps_ouline_rects.append(selection_map_rect)

        self.saved_maps_ouline_rects = saved_maps_ouline_rects

    def highlight_selected_map(self) -> Union[None, str]:
        for i, outline_rect in enumerate(self.saved_maps_ouline_rects):
            if outline_rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(
                    surface=self.editor.screen,
                    color=canvas.SAVED_MAPS_HIGHLIGHT_COLOR,
                    rect=outline_rect,
                    width=5
                )
                if pygame.mouse.get_pressed()[0] == 1:
                    return self.saved_map_names[i]

        return None

    def draw_presets_menu(self) -> None:
        presets_rects_outlines = []

        for i, name in enumerate(self.preset_names):
            text_pos = drawing.draw_text(screen=self.editor.screen,
                                         text=name,
                                         font=self.editor.tab_font,
                                         color=right_panel.TAB_NAME_COLOR,
                                         x_pos=right_panel.TAB_NAME_X_OFFSET,
                                         y_pos=right_panel.TAB_NAME_Y_OFFSET + i * right_panel.TAB_NAME_Y_SPACING,
                                         get_rect=True)

            text_rect = pygame.rect.Rect(text_pos)
            text_rect[2] = setup.SCREEN_WIDTH + setup.RIGHT_MARGIN - text_rect[0]

            presets_rects_outlines.append(text_rect)

        self.preset_name_rects_outlines = presets_rects_outlines

    def highlight_selected_preset(self) -> Union[None, str]:
        for i, outline_rect in enumerate(self.preset_name_rects_outlines):
            if outline_rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(
                    surface=self.editor.screen,
                    color=right_panel.TAB_HIGHLIGHT_COLOR,
                    rect=(outline_rect[0] + right_panel.TAB_HIGHLIGHT_LEFT_OFFSET,
                          outline_rect[1] + right_panel.TAB_HIGHLIGHT_TOP_OFFSET * 1.5,
                          outline_rect[2] - 16,
                          outline_rect[3] + right_panel.TAB_HIGHLIGHT_BOTTOM_OFFSET * 3),
                    width=right_panel.TAB_HIGHLIGHT_WIDTH
                )
                if pygame.mouse.get_pressed()[0] == 1:
                    return self.preset_names[i]

        return None

    def display_presets_previews(self) -> None:
        """
            Shows a preview of the first image in the displayed presets-folder next to its name.

            Returns:
                None
        """
        for i, name in enumerate(self.preset_names):
            preview_img = pygame.transform.scale(
                surface=sprites.get_preview_image(tab_name=name),
                size=(right_panel.PREVIEW_WIDTH,
                      right_panel.PREVIEW_HEIGHT))
            self.editor.screen.blit(source=preview_img,
                                    dest=(
                                        right_panel.PREVIEW_X,
                                        right_panel.PREVIEW_Y_OFFSET + i * right_panel.TAB_NAME_Y_SPACING
                                    ))
