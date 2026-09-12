#=============================#
# IMPORTS                     #
#=============================#
#-----------------------------
import pygame

from ascii.frames import DOUBLE
#-----------------------------


#=============================#
# SHARED UI CONFIG            #
#=============================#
#-----------------------------
FONT_NAME = "consolas"

LOGO_FONT_SIZE = 8
FRAME_FONT_SIZE = 11
MENU_FONT_SIZE = 14
TITLE_FONT_SIZE = 14
TEXT_FONT_SIZE = 11
FOOTER_FONT_SIZE = 9

LOGO_Y = 21

PANEL_Y = 108
PANEL_ROWS = 16

LEFT_PANEL_COLUMNS = 28
RIGHT_PANEL_COLUMNS = 60

PANEL_GAP = 12

FOOTER_Y = 338
#-----------------------------


#=============================#
# PANEL POSITIONS             #
#=============================#
#-----------------------------
def get_panel_positions(surface):
    frame_font = pygame.font.SysFont(
        FONT_NAME,
        FRAME_FONT_SIZE
    )

    left_top = (
        DOUBLE["top_left"]
        + DOUBLE["horizontal"] * (LEFT_PANEL_COLUMNS - 2)
        + DOUBLE["top_right"]
    )

    right_top = (
        DOUBLE["top_left"]
        + DOUBLE["horizontal"] * (RIGHT_PANEL_COLUMNS - 2)
        + DOUBLE["top_right"]
    )

    left_width = frame_font.size(
        left_top
    )[0]

    right_width = frame_font.size(
        right_top
    )[0]

    total_width = (
        left_width
        + PANEL_GAP
        + right_width
    )

    left_x = (
        surface.get_width()
        - total_width
    ) // 2

    right_x = (
        left_x
        + left_width
        + PANEL_GAP
    )

    return (
        left_x,
        right_x
    )
#-----------------------------