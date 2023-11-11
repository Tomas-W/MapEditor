"""
Menu drawing functions for the Preset Menu.
All functions draw to the screen.
These functions do NOT interact with the program directly.
"""

from typing import Any, List

import pygame

from utilities import fonts, render_text, sprites

from settings.panels import *


def display_preset_names(presets_renderer: Any) -> None:
    """
        Blits preset names to the right panel.

       Returns:
           None.
    """
    presets_rects_outlines: List[pygame.rect.Rect] = []

    for i, name in enumerate(presets_renderer.preset_names):
        text_pos = render_text.position(screen=presets_renderer.editor.screen,
                                        text=str(name),
                                        font=fonts.presets_font,
                                        color=PRESETS_NAME_COLOR,
                                        x_pos=PRESETS_NAME_X_OFFSET,
                                        y_pos=PRESETS_NAME_Y_OFFSET + i * PRESETS_NAME_Y_SPACING,
                                        get_rect=True)

        # Create and save a rect outline for hover functionality
        text_rect = pygame.rect.Rect(text_pos)
        text_rect[2] = SCREEN_WIDTH + RIGHT_MARGIN - text_rect[0]
        presets_rects_outlines.append(text_rect)

    # Store hover rects
    presets_renderer.preset_names_outline_rects = presets_rects_outlines


def display_presets_previews(presets_renderer: Any) -> None:
    """
        Blits a preview of the first image of each of the presets in the PRESETS_DIR
            next to its name.

        Returns:
            None
    """
    for i, name in enumerate(presets_renderer.preset_names):
        preview_img = pygame.transform.scale(surface=sprites.get_preview_image(preset_name=name),
                                             size=(PREVIEW_WIDTH,
                                                   PREVIEW_HEIGHT))
        presets_renderer.editor.screen.blit(source=preview_img,
                                            dest=(PREVIEW_X,
                                                  PREVIEW_Y + i * PRESETS_NAME_Y_SPACING))


def highlight_selected_preset(presets_renderer: Any) -> None | str:
    """
        Blits a rect around the hovered over preset

       Returns:
           None.
    """
    for i, outline_rect in enumerate(presets_renderer.preset_names_outline_rects):

        if outline_rect.collidepoint(presets_renderer.editor.mouse_pos):
            pygame.draw.rect(
                surface=presets_renderer.editor.screen,
                color=PRESETS_HIGHLIGHT_COLOR,
                rect=(outline_rect[0] + PRESETS_HIGHLIGHT_LEFT_OFFSET,
                      outline_rect[1] + PRESETS_HIGHLIGHT_TOP_OFFSET * 1.5,
                      outline_rect[2] - 16,
                      outline_rect[3] + PRESETS_HIGHLIGHT_BOTTOM_OFFSET * 3),
                width=PRESETS_HIGHLIGHT_WIDTH
            )

            # Selection on mouse release so need to check for previous mouse press
            if presets_renderer.clicked:
                for event in presets_renderer.editor.events:
                    if event.type == pygame.MOUSEBUTTONUP:
                        return presets_renderer.preset_names[i]

            if pygame.mouse.get_pressed()[0] == 1:
                presets_renderer.clicked = True

            else:
                presets_renderer.clicked = False

    # No hover detected
    return None
