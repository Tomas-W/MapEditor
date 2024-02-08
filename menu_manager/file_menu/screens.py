"""
Menu drawing functions for the File Menu.
All functions draw to the screen.
These functions do NOT interact with the program directly.
"""


from typing import Any

import pygame

from menu_manager.file_menu import utils, actions

from utilities import fonts, render_text, helpers

from settings.menus import *


def display_load_map(menu_renderer: Any) -> None:
    """
        Blits load map text and name of the maps to the screen.

        Uses:
           screen (pygame.display): Editor window.
           saved_map_names (str): Map names to blit to screen.
           font (pygame.font.Font): pygame.font object.

       Returns:
           None.
    """
    menu_renderer.saved_maps_names = utils.get_saved_maps_names()
    saved_maps_outline_rects: list[pygame.rect.Rect] = []

    # Draw map names
    for i, name in enumerate(menu_renderer.saved_maps_names):
        saved_map_text = render_text.position(screen=menu_renderer.editor.screen,
                                              text=str(name),
                                              font=fonts.load_map_font,
                                              color=SAVED_MAPS_COLOR,
                                              x_pos=SAVED_MAPS_X,
                                              y_pos=i * SAVED_MAPS_Y_SPACING + SAVED_MAPS_Y,
                                              get_rect=True)

        saved_map_rect = pygame.Rect(saved_map_text)
        selection_map_rect = helpers.get_enlarged_rect(rect=saved_map_rect,
                                                       pixels=SAVED_MAPS_HIGHLIGHT_WIDTH * 2)
        saved_maps_outline_rects.append(selection_map_rect)

    menu_renderer.saved_maps_outline_rects = saved_maps_outline_rects

    # Highlight and select
    highlight_selected_map(menu_renderer=menu_renderer)
    if menu_renderer.selected_map is not None:
        # Blit load map name
        render_text.centered_x(screen=menu_renderer.editor.screen,
                               text=LOAD_MAP_TEXT,
                               font=fonts.load_map_font,
                               color=SAVED_MAPS_COLOR,
                               y_pos=LOAD_MAP_NAME_Y,
                               get_rect=False)
        # Blit selected map name
        render_text.centered_x(screen=menu_renderer.editor.screen,
                               text=menu_renderer.selected_map,
                               font=fonts.load_map_font,
                               color=SAVED_MAPS_COLOR,
                               y_pos=SELECTED_MAP_NAME_Y,
                               get_rect=False)

    # Cancel and return
    if menu_renderer.back_button.draw():
        menu_renderer.selected_map = None
        menu_renderer.menu_controller.set_state("reset")

    # Load map if selected and return
    if menu_renderer.ok_button.draw():
        if menu_renderer.selected_map is not None:
            actions.load_new_map(editor=menu_renderer.editor,
                                 selected_map=menu_renderer.selected_map)
            menu_renderer.selected_map = None
            menu_renderer.menu_controller.set_state("reset")


def highlight_selected_map(menu_renderer: Any) -> None | str:
    """
        Highlights the map if the user is currently hovering over.

        Uses:
           screen (pygame.display): Editor window.
           saved_maps_outline_rects (list): All recs containing the maps.

       Returns:
           Union[None, str].
    """
    for i, outline_rect in enumerate(menu_renderer.saved_maps_outline_rects):
        if outline_rect.collidepoint(menu_renderer.editor.mouse_pos):
            pygame.draw.rect(
                surface=menu_renderer.editor.screen,
                color=SAVED_MAPS_HIGHLIGHT_COLOR,
                rect=outline_rect,
                width=SAVED_MAPS_HIGHLIGHT_WIDTH
            )
            if menu_renderer.clicked:
                for event in menu_renderer.editor.events:
                    if event.type == pygame.MOUSEBUTTONUP:
                        menu_renderer.selected_map = menu_renderer.saved_maps_names[i]

            if pygame.mouse.get_pressed()[0] == 1:
                menu_renderer.clicked = True

            else:
                menu_renderer.clicked = False


def display_rename(menu_renderer: Any) -> None:
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
    render_text.centered_x(screen=menu_renderer.editor.screen,
                           text=str(CHANGE_NAME_TEXT),
                           font=fonts.load_map_font,
                           y_pos=CHANGE_NAME_TITLE_Y,
                           color=CHANGE_NAME_TITLE_COLOR)

    # Name
    render_text.centered_x(screen=menu_renderer.editor.screen,
                           text=str(menu_renderer.editor.temp_map_name),
                           font=fonts.load_map_font,
                           y_pos=CHANGE_NAME_Y,
                           color=CHANGE_NAME_COLOR)

    if menu_renderer.back_button.draw():
        menu_renderer.editor.temp_map_name = menu_renderer.editor.map_name
        menu_renderer.menu_controller.set_state("reset")

    # Save new map name
    if menu_renderer.ok_button.draw():
        menu_renderer.editor.map_name = menu_renderer.editor.temp_map_name
        menu_renderer.menu_controller.popup_renderer.set_save_map_info()
        menu_renderer.menu_controller.set_state("reset")
