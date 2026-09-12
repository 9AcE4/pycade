#=============================#
# IMPORTS                     #
#=============================#
#-----------------------------
import pygame

from ascii.logos import PYCADE_LOGO
from ui.themes import PYCADE_GRADIENT
from ui.themes import PYCADE_GRADIENT_SPEED
#-----------------------------


#=============================#
# TEXT RENDERING              #
#=============================#
#-----------------------------
def draw_text(
    surface,
    text,
    position,
    color,
    font_name,
    font_size,
    center=False
):
    font = pygame.font.SysFont(
        font_name,
        font_size
    )

    text_surface = font.render(
        text,
        True,
        color
    )

    text_rect = text_surface.get_rect()

    if center:
        text_rect.center = position
    else:
        text_rect.topleft = position

    surface.blit(
        text_surface,
        text_rect
    )
#-----------------------------


#=============================#
# ASCII BOX RENDERING         #
#=============================#
#-----------------------------
def draw_box(
    surface,
    x,
    y,
    columns,
    rows,
    color,
    frame,
    font_name,
    font_size
):
    font = pygame.font.SysFont(
        font_name,
        font_size
    )

    line_height = font.get_linesize()

    top = (
        frame["top_left"]
        + frame["horizontal"] * (columns - 2)
        + frame["top_right"]
    )

    middle = (
        frame["vertical"]
        + " " * (columns - 2)
        + frame["vertical"]
    )

    bottom = (
        frame["bottom_left"]
        + frame["horizontal"] * (columns - 2)
        + frame["bottom_right"]
    )

    lines = [
        top,
        *(
            middle
            for _ in range(rows - 2)
        ),
        bottom,
    ]

    for row, line in enumerate(lines):
        line_surface = font.render(
            line,
            True,
            color
        )

        surface.blit(
            line_surface,
            (
                x,
                y + row * line_height
            )
        )
#-----------------------------


#=============================#
# PYCADE LOGO RENDERING       #
#=============================#
#-----------------------------
def draw_pycade_logo(
    surface,
    center_x,
    top_y,
    elapsed_ms,
    font_name,
    font_size,
    alpha=255
):
    logo_lines = (
        PYCADE_LOGO
        .strip("\n")
        .splitlines()
    )

    font = pygame.font.SysFont(
        font_name,
        font_size
    )

    char_width = font.size("M")[0]
    line_height = font.get_linesize()

    max_line_length = max(
        len(line)
        for line in logo_lines
    )

    logo_width = (
        max_line_length
        * char_width
    )

    start_x = (
        center_x
        - logo_width // 2
    )

    for row, line in enumerate(logo_lines):
        y = (
            top_y
            + row * line_height
        )

        for column, character in enumerate(line):
            if character == " ":
                continue

            x = (
                start_x
                + column * char_width
            )

            gradient_position = (
                column
                / max(
                    1,
                    max_line_length
                )
            )

            color = get_gradient_color(
                gradient_position,
                elapsed_ms
            )

            character_surface = font.render(
                character,
                True,
                color
            )

            character_surface.set_alpha(
                alpha
            )

            surface.blit(
                character_surface,
                (x, y)
            )
#-----------------------------


#=============================#
# GRADIENT                    #
#=============================#
#-----------------------------
def get_gradient_color(
    position,
    elapsed_ms
):
    phase = (
        position
        + elapsed_ms * PYCADE_GRADIENT_SPEED
    ) % 1.0

    color_count = len(
        PYCADE_GRADIENT
    )

    scaled_position = (
        phase
        * color_count
    )

    index_a = (
        int(scaled_position)
        % color_count
    )

    index_b = (
        index_a + 1
    ) % color_count

    blend = (
        scaled_position
        - int(scaled_position)
    )

    color_a = PYCADE_GRADIENT[index_a]
    color_b = PYCADE_GRADIENT[index_b]

    return (
        int(
            color_a[0]
            + (
                color_b[0]
                - color_a[0]
            ) * blend
        ),
        int(
            color_a[1]
            + (
                color_b[1]
                - color_a[1]
            ) * blend
        ),
        int(
            color_a[2]
            + (
                color_b[2]
                - color_a[2]
            ) * blend
        ),
    )
#-----------------------------
