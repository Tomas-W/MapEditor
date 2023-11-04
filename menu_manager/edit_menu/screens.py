from typing import Any, List, Tuple

import pygame

from menu_manager.edit_menu import utils

from utilities import render_text, fonts, helpers

from settings.menus import *


def display_preferences(menu_renderer: Any) -> None:
    """
        Blits preferences attributes and value to the screen together
            with the currently selected attribute and value.
        This is text only and obtained from MenuRenderer.preferences_dict and
            editor.selected_preference_name.

       Returns:
           None.
    """
    preferences_outline_recs: List[pygame.rect.Rect] = []
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
                           get_rect=False)

    # Selected preference vale
    render_text.centered_x(screen=menu_renderer.editor.screen,
                           text=str(menu_renderer.editor.selected_preference_value_change),
                           font=fonts.preferences_font,
                           color=WHITE,
                           y_pos=SELECTED_PREFERENCE_VAL_Y,
                           get_rect=False)

    # Menu Options
    if menu_renderer.pressed_ok_button():
        if utils.is_new_value_allowed(name=menu_renderer.editor.selected_preference_name,
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
            menu_renderer.preferences_dict = utils.get_preferences_dict(editor=menu_renderer.editor)
            utils.update_world_data_size(editor=menu_renderer.editor)

        else:
            print(
                f"setting: '{menu_renderer.editor.selected_preference_name}'"
                f" cannot be value: '{menu_renderer.editor.selected_preference_value_change}'")

    if menu_renderer.pressed_back_button():
        menu_renderer.menu_controller.set_state("reset")


def highlight_selected_preference(menu_renderer: Any) -> None | Tuple[str, int]:
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
