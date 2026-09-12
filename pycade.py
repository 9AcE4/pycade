#=============================#
# IMPORTS                     #
#=============================#
#-----------------------------
import pygame

from engine.controls import handle_global_events
from engine.window import create_window
from ui.hub.mainscreen import MainScreen
from ui.splash import Splash
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

    # Temporary:
    # Later this will only be called after
    # scores, settings and other startup data
    # have actually finished loading.
    splash.set_ready()

    running = True
    clock = pygame.time.Clock()

    while running:
        events = pygame.event.get()

        running = handle_global_events(
            events
        )

        if not running:
            break

        if splash.is_finished():
            action = main_screen.update(
                events
            )

            if action == "EXIT":
                running = False
                break

            main_screen.draw(
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

        clock.tick(60)

    pygame.quit()
#-----------------------------


#=============================#
# ENTRY POINT                 #
#=============================#
#-----------------------------
if __name__ == "__main__":
    main()
#-----------------------------