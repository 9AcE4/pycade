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

NARROW_PANEL_COLUMNS = 28
WIDE_PANEL_COLUMNS = 60

LEFT_PANEL_COLUMNS = NARROW_PANEL_COLUMNS
RIGHT_PANEL_COLUMNS = WIDE_PANEL_COLUMNS

PANEL_GAP = 12

FOOTER_Y = 338
#-----------------------------


#=============================#
# PANEL WIDTH                 #
#=============================#
#-----------------------------
def get_panel_width(columns):
    frame_font = pygame.font.SysFont(
        FONT_NAME,
        FRAME_FONT_SIZE
    )

    top_line = (
        DOUBLE["top_left"]
        + DOUBLE["horizontal"] * (columns - 2)
        + DOUBLE["top_right"]
    )

    return frame_font.size(
        top_line
    )[0]
#-----------------------------


#=============================#
# PANEL POSITIONS             #
#=============================#
#-----------------------------
def get_panel_positions(
    surface,
    left_columns=LEFT_PANEL_COLUMNS,
    right_columns=RIGHT_PANEL_COLUMNS
):
    left_width = get_panel_width(
        left_columns
    )

    right_width = get_panel_width(
        right_columns
    )

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