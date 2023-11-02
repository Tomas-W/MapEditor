import pygame


class EventHandler:

    def __init__(self,
                 editor: any):

        self.editor = editor

    def run(self):
        self.quitting_events()

        self.undo_redo_events()

        self.scrolling_events()

    def quitting_events(self) -> None:
        """
            Listens for quit event.
        """
        for event in self.editor.events:
            if event.type == pygame.QUIT:
                self.editor.is_running = False

    def undo_redo_events(self) -> None:
        for event in self.editor.events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    self.editor.undo_tile_placement()

                if event.key == pygame.K_x:
                    self.editor.redo_tile_placement()

        keys = self.editor.keys

        if keys[pygame.K_z] and keys[pygame.K_LSHIFT]:
            self.editor.undo_tile_placement()
        if keys[pygame.K_x] and keys[pygame.K_LSHIFT]:
            self.editor.redo_tile_placement()

    def scrolling_events(self) -> None:
        """
            Gets user inputs and changes scroll values.
        """
        keys = self.editor.keys

        # Activate scrolling
        if keys[pygame.K_a]:
            self.editor.scroll_left = True
        if keys[pygame.K_d]:
            self.editor.scroll_right = True
        if keys[pygame.K_w]:
            self.editor.scroll_up = True
        if keys[pygame.K_s]:
            self.editor.scroll_down = True
        if keys[pygame.K_LSHIFT]:
            self.editor.scroll_speed = self.editor.max_scroll_speed

        # De-activate scrolling
        if not keys[pygame.K_a]:
            self.editor.scroll_left = False
        if not keys[pygame.K_d]:
            self.editor.scroll_right = False
        if not keys[pygame.K_w]:
            self.editor.scroll_up = False
        if not keys[pygame.K_s]:
            self.editor.scroll_down = False
        if not keys[pygame.K_LSHIFT]:
            self.editor.scroll_speed = self.editor.base_scroll_speed

    # Called from menu_handler
    def get_map_name_input(self) -> None:
        """
            Listens for keydown events to change the name of the map.
        """
        for events in self.editor.events:
            if events.type == pygame.KEYDOWN:

                if events.key == pygame.K_BACKSPACE:
                    # Delete last character
                    self.editor.temp_map_name = self.editor.temp_map_name[:-1]

                elif events.key == pygame.K_RETURN:
                    # Exit out
                    self.editor.is_renaming_map = False
                    self.editor.is_building = True
                    self.editor.map_name = self.editor.temp_map_name

                else:
                    # Add new character to end
                    self.editor.temp_map_name += events.unicode

    def get_preference_input(self) -> None:
        """
            Listens for keydown events to change the value of a preference.
        """
        for events in self.editor.events:
            if events.type == pygame.KEYDOWN:
                if events.key == pygame.K_BACKSPACE:
                    # Delete last character
                    self.editor.selected_preference_value_change = str(
                        self.editor.selected_preference_value_change)[:-1]

                elif events.key in range(pygame.K_0, pygame.K_9 + 1):
                    self.editor.selected_preference_value_change = str(
                        self.editor.selected_preference_value_change) + events.unicode
