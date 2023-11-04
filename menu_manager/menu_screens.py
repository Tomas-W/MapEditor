from typing import Union, Tuple, Any

import pygame

from menu_manager import menu_utils

from settings.menus import *
from settings.panels import *
from settings.setup import *
from utilities import helpers, fonts, render_text, sprites, general


def display_preferences(menu_renderer: Any) -> None:
    """
        Blits preferences attributes and value to the screen together
            with the currently selected attribute and value.
        This is text only and obtained from MenuRenderer.preferences_dict and
            editor.selected_preference_name.

       Returns:
           None.
    """
    preferences_outline_recs = []
    # Preferences
    for i, (key, val) in enumerate(menu_renderer.preferences_dict.items()):
        preference = render_text.position(screen=menu_renderer.editor.screen,
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

    menu_renderer.preferences_outline_recs = preferences_outline_recs

    # Selected preference key
    render_text.centered_x(screen=menu_renderer.editor.screen,
                           text=str(menu_renderer.editor.selected_preference_name),
                           font=fonts.preferences_font,
                           color=WHITE,
                           y_pos=SELECTED_PREFERENCE_KEY_Y,
                           get_rect=False
                           )

    # Selected preference vale
    render_text.centered_x(screen=menu_renderer.editor.screen,
                           text=str(menu_renderer.editor.selected_preference_value_change),
                           font=fonts.preferences_font,
                           color=WHITE,
                           y_pos=SELECTED_PREFERENCE_VAL_Y,
                           get_rect=False
                           )

    # Menu Options
    if menu_renderer.pressed_ok_button():
        if general.is_new_value_allowed(name=menu_renderer.editor.selected_preference_name,
                                        value=int(
                                            menu_renderer.editor.selected_preference_value_change)):
            print(
                f"setting: '{menu_renderer.editor.selected_preference_name}'"
                f" changed from '{menu_renderer.editor.selected_preference_value}'"
                f" to '{menu_renderer.editor.selected_preference_value_change}'")
            menu_renderer.editor.selected_preference_value = menu_renderer.editor.selected_preference_value_change

            attributes_dict = {
                menu_renderer.editor.selected_preference_name: int(
                    menu_renderer.editor.selected_preference_value)
            }
            helpers.update_class_dict(cls=menu_renderer.editor,
                                      attributes=attributes_dict)
            menu_renderer.editor.background = helpers.update_background(editor=menu_renderer.editor)
            menu_renderer.preferences_dict = menu_utils.get_preferences_dict(editor=menu_renderer.editor)
            helpers.update_world_data_size(editor=menu_renderer.editor)

        else:
            print(
                f"setting: '{menu_renderer.editor.selected_preference_name}'"
                f" cannot be value: '{menu_renderer.editor.selected_preference_value_change}'")

    if menu_renderer.pressed_back_button():
        menu_renderer.menu_controller.set_state("reset")


def highlight_selected_preference(menu_renderer: Any) -> Union[None, Tuple[str, int]]:
    """
        Highlights the preference the user is currently hovering over.

        Uses:
           screen (pygame.display): Editor window.
           saved_maps_outline_rects (list): All recs containing the preferences.

       Returns:
           Union[None, Tuple[str, int]].
    """
    for i, outline_rect in enumerate(menu_renderer.preferences_outline_recs):
        if outline_rect.collidepoint(menu_renderer.editor.mouse_pos):
            pygame.draw.rect(
                surface=menu_renderer.editor.screen,
                color=PREFERENCES_COLOR,
                rect=outline_rect,
                width=5
            )
            if pygame.mouse.get_pressed()[0] == 1:
                menu_renderer.editor.selected_preference_value_change = \
                    list(menu_renderer.preferences_dict.items())[i][-1]

                return list(menu_renderer.preferences_dict.items())[i]

    return None


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
        menu_renderer.menu_controller.set_state("reset")


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
    menu_renderer.saved_maps_names = menu_utils.get_saved_maps_names()
    saved_maps_ouline_rects = []

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
        saved_maps_ouline_rects.append(selection_map_rect)

    menu_renderer.saved_maps_outline_rects = saved_maps_ouline_rects


def highlight_selected_map(menu_renderer: Any) -> Union[None, str]:
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
                        return menu_renderer.saved_maps_names[i]

            if pygame.mouse.get_pressed()[0] == 1:
                menu_renderer.clicked = True

            else:
                menu_renderer.clicked = False

    return None


def display_presets(menu_renderer: Any) -> None:
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

    for i, name in enumerate(menu_renderer.preset_names):
        text_pos = render_text.position(screen=menu_renderer.editor.screen,
                                        text=str(name),
                                        font=fonts.presets_font,
                                        color=PRESETS_NAME_COLOR,
                                        x_pos=PRESETS_NAME_X_OFFSET,
                                        y_pos=PRESETS_NAME_Y_OFFSET + i * PRESETS_NAME_Y_SPACING,
                                        get_rect=True)

        text_rect = pygame.rect.Rect(text_pos)
        text_rect[2] = SCREEN_WIDTH + RIGHT_MARGIN - text_rect[0]

        presets_rects_outlines.append(text_rect)

    menu_renderer.preset_names_outline_rects = presets_rects_outlines


def display_presets_previews(menu_renderer: Any) -> None:
    """
        Shows a preview of the first image in the displayed presets-folder next to its name.

        Returns:
            None
    """
    for i, name in enumerate(menu_renderer.preset_names):
        preview_img = pygame.transform.scale(
            surface=sprites.get_preview_image(preset_name=name),
            size=(PREVIEW_WIDTH,
                  PREVIEW_HEIGHT))
        menu_renderer.editor.screen.blit(source=preview_img,
                                dest=(
                                    PREVIEW_X,
                                    PREVIEW_Y + i * PRESETS_NAME_Y_SPACING
                                ))


def highlight_selected_preset(menu_renderer: Any) -> Union[None, str]:
    """
        Highlights the preset if the user is currently hovering over.

        Uses:
           screen (pygame.display): Editor window.
           preset_name_rects_outlines (str): All preset outline rects.

       Returns:
           None.
    """
    for i, outline_rect in enumerate(menu_renderer.preset_names_outline_rects):

        if outline_rect.collidepoint(menu_renderer.editor.mouse_pos):
            pygame.draw.rect(
                surface=menu_renderer.editor.screen,
                color=PRESETS_HIGHLIGHT_COLOR,
                rect=(outline_rect[0] + PRESETS_HIGHLIGHT_LEFT_OFFSET,
                      outline_rect[1] + PRESETS_HIGHLIGHT_TOP_OFFSET * 1.5,
                      outline_rect[2] - 16,
                      outline_rect[3] + PRESETS_HIGHLIGHT_BOTTOM_OFFSET * 3),
                width=PRESETS_HIGHLIGHT_WIDTH
            )

            if menu_renderer.clicked:
                for event in menu_renderer.editor.events:
                    if event.type == pygame.MOUSEBUTTONUP:
                        return menu_renderer.preset_names[i]

            if pygame.mouse.get_pressed()[0] == 1:
                menu_renderer.clicked = True

            else:
                menu_renderer.clicked = False

    return None
