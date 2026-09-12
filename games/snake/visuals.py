#=============================#
# IMPORTS                     #
#=============================#
#-----------------------------
import pygame

from ascii.frames import DOUBLE
from ui.layout import FONT_NAME
from ui.layout import FOOTER_FONT_SIZE
from ui.layout import FOOTER_Y
from ui.layout import FRAME_FONT_SIZE
from ui.layout import LOGO_FONT_SIZE
from ui.layout import LOGO_Y
from ui.layout import MENU_FONT_SIZE
from ui.layout import NARROW_PANEL_COLUMNS
from ui.layout import PANEL_ROWS
from ui.layout import PANEL_Y
from ui.layout import TEXT_FONT_SIZE
from ui.layout import TITLE_FONT_SIZE
from ui.layout import WIDE_PANEL_COLUMNS
from ui.layout import get_panel_positions
from ui.rendering import draw_box
from ui.rendering import draw_pycade_logo
from ui.rendering import draw_text
from ui.themes import DEFAULT_THEME
from ui.themes import THEMES
#-----------------------------


#=============================#
# SNAKE MENU                  #
#=============================#
#-----------------------------
def draw_snake_menu(
    surface,
    menu_items,
    selected_index,
    theme_name=DEFAULT_THEME
):
    theme = THEMES[
        theme_name
    ]

    surface.fill(
        theme["background"]
    )

    elapsed_ms = pygame.time.get_ticks()

    left_x, right_x = get_panel_positions(
        surface,
        WIDE_PANEL_COLUMNS,
        NARROW_PANEL_COLUMNS
    )

    draw_pycade_logo(
        surface,
        surface.get_width() // 2,
        LOGO_Y,
        elapsed_ms,
        FONT_NAME,
        LOGO_FONT_SIZE
    )

    draw_box(
        surface,
        left_x,
        PANEL_Y,
        WIDE_PANEL_COLUMNS,
        PANEL_ROWS,
        theme["primary"],
        DOUBLE,
        FONT_NAME,
        FRAME_FONT_SIZE
    )

    draw_box(
        surface,
        right_x,
        PANEL_Y,
        NARROW_PANEL_COLUMNS,
        PANEL_ROWS,
        theme["primary"],
        DOUBLE,
        FONT_NAME,
        FRAME_FONT_SIZE
    )

    draw_text(
        surface,
        "SNAKE",
        (
            left_x + 17,
            PANEL_Y + 17
        ),
        theme["secondary"],
        FONT_NAME,
        TEXT_FONT_SIZE
    )

    draw_text(
        surface,
        "CLASSIC SNAKE",
        (
            left_x + 17,
            PANEL_Y + 50
        ),
        theme["accent"],
        FONT_NAME,
        TITLE_FONT_SIZE
    )

    draw_text(
        surface,
        "SNAKE MENU",
        (
            right_x + 17,
            PANEL_Y + 17
        ),
        theme["secondary"],
        FONT_NAME,
        TEXT_FONT_SIZE
    )

    start_y = (
        PANEL_Y + 50
    )

    for index, item in enumerate(
        menu_items
    ):
        selected = (
            index == selected_index
        )

        prefix = (
            "> "
            if selected
            else "  "
        )

        color = (
            theme["accent"]
            if selected
            else theme["primary"]
        )

        draw_text(
            surface,
            prefix + item,
            (
                right_x + 17,
                start_y + index * 27
            ),
            color,
            FONT_NAME,
            MENU_FONT_SIZE
        )

    footer_text = (
        "[UP/DOWN] NAVIGATE    "
        "[ENTER] SELECT    "
        "[ESC] BACK"
    )

    draw_text(
        surface,
        footer_text,
        (
            surface.get_width() // 2,
            FOOTER_Y
        ),
        theme["secondary"],
        FONT_NAME,
        FOOTER_FONT_SIZE,
        center=True
    )
#-----------------------------