#=============================#
# IMPORTS                     #
#=============================#
#-----------------------------
import pygame

from engine.window import create_window
from engine.controls import handle_global_events
#-----------------------------

#=============================#
# MAIN FUNCTION               #
#=============================#
#-----------------------------
def main():
    pygame.init()

    window, logical_surface = create_window()

    running = True

    while running:
        running = handle_global_events()

        logical_surface.fill((0, 0, 0))

        pygame.transform.scale(
            logical_surface,
            window.get_size(),
            window
        )

        pygame.display.flip()

    pygame.quit()
#-----------------------------

#=============================#
# ENTRY POINT                 #
#=============================#
#-----------------------------
if __name__ == "__main__":
    main()
#-----------------------------