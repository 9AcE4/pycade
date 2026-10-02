#=============================#
# IMPORTS                     #
#=============================#
#-----------------------------
import pygame
#-----------------------------

#=============================#
# CONSTANTS                   #
#=============================#
#-----------------------------
LOGICAL_WIDTH = 640
LOGICAL_HEIGHT = 360

DEFAULT_SCALE = 1
#-----------------------------

#=============================#
# FUNCTIONS                   #
#=============================#
#-----------------------------
def create_window(scale=DEFAULT_SCALE):
    width = LOGICAL_WIDTH * scale
    height = LOGICAL_HEIGHT * scale

    window = pygame.display.set_mode(
        (width, height)
    )

    pygame.display.set_caption("PyCade")

    logical_surface = pygame.Surface(
        (LOGICAL_WIDTH, LOGICAL_HEIGHT)
    )

    return window, logical_surface
#-----------------------------
