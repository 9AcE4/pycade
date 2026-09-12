#=============================#
# IMPORTS                     #
#=============================#
#-----------------------------
import pygame

from engine.controls import handle_global_events
from engine.window import create_window
from ui.games.selection import ACTION_BACK
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
#-----------------------------


#=============================#
# MAIN FUNCTION               #
#=============================#
#-----------------------------
def main():
    pygame.init()

    window, logical_surface = create_window()

    splash = Splash()
    main_screen = MainScreen()
    game_selection_screen = GameSelectionScreen()

    # Temporary:
    # Later this will only be called after
    # scores, settings and other startup data
    # have actually finished loading.
    splash.set_ready()

    running = True
    active_screen = SCREEN_HUB
    hub_elapsed_ms = 0

    clock = pygame.time.Clock()

    while running:
        hub_was_drawn = False

        events = pygame.event.get()

        running = handle_global_events(
            events
        )

        if not running:
            break

        if splash.is_finished():
            if active_screen == SCREEN_HUB:
                action = main_screen.update(
                    events
                )

                if action == "EXIT":
                    running = False
                    break

                if action == "GAMES":
                    active_screen = (
                        SCREEN_GAME_LIBRARY
                    )

            elif active_screen == SCREEN_GAME_LIBRARY:
                action = game_selection_screen.update(
                    events
                )

                if action == ACTION_BACK:
                    active_screen = SCREEN_HUB

            if active_screen == SCREEN_HUB:
                main_screen.draw(
                    logical_surface,
                    hub_elapsed_ms
                )

                hub_was_drawn = True

            elif active_screen == SCREEN_GAME_LIBRARY:
                game_selection_screen.draw(
                    logical_surface
                )
        else:
            splash.update(
                events
            )
            splash.draw(
                logical_surface
            )

        pygame.transform.scale(
            logical_surface,
            window.get_size(),
            window
        )

        pygame.display.flip()

        frame_elapsed_ms = clock.tick(60)

        if hub_was_drawn:
            hub_elapsed_ms += frame_elapsed_ms

    pygame.quit()
#-----------------------------


#=============================#
# ENTRY POINT                 #
#=============================#
#-----------------------------
if __name__ == "__main__":
    main()
#-----------------------------
