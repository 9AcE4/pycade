#=============================#
# IMPORTS                     #
#=============================#
#-----------------------------
import pygame

from engine.controls import handle_global_events
from engine.window import create_window
from games.launcher import create_game
from ui.games.selection import ACTION_BACK
from ui.games.selection import ACTION_SELECT
from ui.games.selection import GameSelectionScreen
from ui.hub.mainscreen import MainScreen
from ui.splash import Splash
#-----------------------------


#=============================#
# SCREEN CONFIG               #
#=============================#
#-----------------------------
SCREEN_HUB = "HUB"
SCREEN_GAME_LIBRARY = "GAME_LIBRARY"
SCREEN_GAME = "GAME"

GAME_ACTION_BACK = "BACK"
#-----------------------------


#=============================#
# PYCADE COORDINATOR          #
#=============================#
#-----------------------------
class PyCadeCoordinator:
    def __init__(self):
        self.window = None
        self.logical_surface = None

        self.splash = None
        self.main_screen = None
        self.game_selection_screen = None

        self.active_screen = SCREEN_HUB
        self.active_game = None

        self.hub_elapsed_ms = 0

        self.running = False
        self.clock = None

    def setup(self):
        pygame.init()

        self.window, self.logical_surface = (
            create_window()
        )

        self.splash = Splash()
        self.main_screen = MainScreen()
        self.game_selection_screen = (
            GameSelectionScreen()
        )

        # Temporary:
        # Later this will only be called after
        # scores, settings and other startup data
        # have actually finished loading.
        self.splash.set_ready()

        self.clock = pygame.time.Clock()

        self.running = True

    def run(self):
        self.setup()

        try:
            while self.running:
                hub_was_drawn = self.run_frame()

                self.present_frame()

                frame_elapsed_ms = self.clock.tick(
                    60
                )

                if hub_was_drawn:
                    self.hub_elapsed_ms += (
                        frame_elapsed_ms
                    )

        finally:
            pygame.quit()
#-----------------------------


#=============================#
# FRAME                       #
#=============================#
#-----------------------------
    def run_frame(self):
        events = pygame.event.get()

        self.running = handle_global_events(
            events
        )

        if not self.running:
            return False

        if not self.splash.is_finished():
            self.splash.update(
                events
            )

            self.splash.draw(
                self.logical_surface
            )

            return False

        self.update_active_screen(
            events
        )

        return self.draw_active_screen()
#-----------------------------


#=============================#
# SCREEN UPDATE               #
#=============================#
#-----------------------------
    def update_active_screen(
        self,
        events
    ):
        if self.active_screen == SCREEN_HUB:
            self.update_hub(
                events
            )

        elif self.active_screen == SCREEN_GAME_LIBRARY:
            self.update_game_library(
                events
            )

        elif self.active_screen == SCREEN_GAME:
            self.update_game(
                events
            )
#-----------------------------


#=============================#
# HUB UPDATE                  #
#=============================#
#-----------------------------
    def update_hub(
        self,
        events
    ):
        action = self.main_screen.update(
            events
        )

        if action == "EXIT":
            self.running = False
            return

        if action == "GAMES":
            self.active_screen = (
                SCREEN_GAME_LIBRARY
            )
#-----------------------------


#=============================#
# GAME LIBRARY UPDATE         #
#=============================#
#-----------------------------
    def update_game_library(
        self,
        events
    ):
        action = self.game_selection_screen.update(
            events
        )

        if action == ACTION_BACK:
            self.active_screen = SCREEN_HUB
            return

        if action != ACTION_SELECT:
            return

        selected_game = (
            self.game_selection_screen
            .get_selected_game()
        )

        if selected_game is None:
            return

        game = create_game(
            selected_game
        )

        if game is None:
            return

        self.active_game = game
        self.active_screen = SCREEN_GAME
#-----------------------------


#=============================#
# GAME UPDATE                 #
#=============================#
#-----------------------------
    def update_game(
        self,
        events
    ):
        if self.active_game is None:
            self.active_screen = (
                SCREEN_GAME_LIBRARY
            )
            return

        action = self.active_game.update(
            events
        )

        if action == GAME_ACTION_BACK:
            self.active_game = None
            self.active_screen = (
                SCREEN_GAME_LIBRARY
            )
#-----------------------------


#=============================#
# SCREEN DRAW                 #
#=============================#
#-----------------------------
    def draw_active_screen(self):
        if self.active_screen == SCREEN_HUB:
            self.main_screen.draw(
                self.logical_surface,
                self.hub_elapsed_ms
            )

            return True

        if self.active_screen == SCREEN_GAME_LIBRARY:
            self.game_selection_screen.draw(
                self.logical_surface
            )

            return False

        if self.active_screen == SCREEN_GAME:
            if self.active_game is not None:
                self.active_game.draw(
                    self.logical_surface
                )

            return False

        return False
#-----------------------------


#=============================#
# FRAME PRESENTATION          #
#=============================#
#-----------------------------
    def present_frame(self):
        pygame.transform.scale(
            self.logical_surface,
            self.window.get_size(),
            self.window
        )

        pygame.display.flip()
#-----------------------------