"""
Menu drawing functions for the Edit Menu.
All functions draw to the screen.
These functions do NOT interact with the program directly.
"""

from typing import Any, Tuple

import pygame

from menu_manager.edit_menu import actions

from utilities import render_text, fonts, helpers

from settings.menus import *


def display_preferences(menu_renderer: Any) -> None:
    """
        Blits preferences attributes and value to the screen together
            with the currently selected attribute and value.
        This is text only and obtained from MenuRenderer.preferences_dict and
            editor.selected_preference_name.
        Draws OK and BACK buttons to the screen to apply or discard the changes
                and switch back to the correct state after.
        Pressing OK will call manage_preferences_change() and
            pressing BACK will rest the MenuController state.

       Returns:
           None.
    """
    preferences_outline_recs: list[pygame.rect.Rect] = []
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
    preference_changed_text = None
    if menu_renderer.pressed_ok_button():
        preference_changed_text = actions.manage_preferences_change(menu_renderer=menu_renderer)

    if menu_renderer.pressed_back_button():
        menu_renderer.menu_controller.set_state("reset")

    # feedback
    if preference_changed_text is not None:
        render_text.centered_x(screen=menu_renderer.editor.screen,
                               text=preference_changed_text,
                               font=fonts.popup_font,
                               color=WHITE,
                               y_pos=PREFERENCE_MESSAGE_Y)


def highlight_and_return_selected_preference(menu_renderer: Any) -> None | Tuple[str, int]:
    """
        Highlights and returns the preference and value the user is currently
            hovering over/selecting by listening for a collision event/mouse click.

       Returns:
           None | Tuple[str, int]: None or selected preference and its value.
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
                return list(menu_renderer.preferences_dict.items())[i]  # is still a Tuple

    return None
