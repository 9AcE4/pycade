#=============================#
# IMPORTS                     #
#=============================#
#-----------------------------
import pygame

from ascii.frames import DOUBLE
from engine.controls import get_menu_navigation
from ui.hub.previews.about_preview import draw_about_preview
from ui.hub.previews.exit_preview import draw_exit_preview
from ui.hub.previews.games_preview import draw_games_preview
from ui.hub.previews.options_preview import draw_options_preview
from ui.hub.previews.scores_preview import draw_scores_preview
from ui.rendering import draw_box
from ui.rendering import draw_pycade_logo
from ui.rendering import draw_text
from ui.themes import DEFAULT_THEME
from ui.themes import THEMES
#-----------------------------


#=============================#
# MAIN SCREEN CONFIG          #
#=============================#
#-----------------------------
FONT_NAME = "consolas"

LOGO_FONT_SIZE = 8
FRAME_FONT_SIZE = 11
MENU_FONT_SIZE = 14
TITLE_FONT_SIZE = 14
TEXT_FONT_SIZE = 11
FOOTER_FONT_SIZE = 9

PANEL_Y = 108
PANEL_ROWS = 16

LEFT_PANEL_COLUMNS = 28
RIGHT_PANEL_COLUMNS = 60

PANEL_GAP = 12

MENU_ITEMS = [
    "GAMES",
    "SCORES",
    "OPTIONS",
    "ABOUT",
    "EXIT",
]

MENU_PREVIEWS = {
    "GAMES": draw_games_preview,
    "SCORES": draw_scores_preview,
    "OPTIONS": draw_options_preview,
    "ABOUT": draw_about_preview,
    "EXIT": draw_exit_preview,
}
#-----------------------------


#=============================#
# MAIN SCREEN                 #
#=============================#
#-----------------------------
class MainScreen:
    def __init__(self, theme_name=DEFAULT_THEME):
        self.theme = THEMES[theme_name]
        self.selected_index = 0

    def update(self, events):
        navigation = get_menu_navigation(
            events
        )

        self.selected_index = (
            self.selected_index + navigation
        ) % len(MENU_ITEMS)

    def draw(self, surface):
        surface.fill(
            self.theme["background"]
        )

        elapsed_ms = pygame.time.get_ticks()

        left_x, right_x = self.get_panel_positions(
            surface
        )

        draw_pycade_logo(
            surface,
            surface.get_width() // 2,
            21,
            elapsed_ms,
            FONT_NAME,
            LOGO_FONT_SIZE
        )

        self.draw_navigation_panel(
            surface,
            left_x
        )

        self.draw_content_panel(
            surface,
            right_x
        )

        self.draw_footer(
            surface
        )
#-----------------------------


#=============================#
# PANEL LAYOUT                #
#=============================#
#-----------------------------
    def get_panel_positions(self, surface):
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


#=============================#
# NAVIGATION PANEL            #
#=============================#
#-----------------------------
    def draw_navigation_panel(
        self,
        surface,
        panel_x
    ):
        draw_box(
            surface,
            panel_x,
            PANEL_Y,
            LEFT_PANEL_COLUMNS,
            PANEL_ROWS,
            self.theme["primary"],
            DOUBLE,
            FONT_NAME,
            FRAME_FONT_SIZE
        )

        draw_text(
            surface,
            "NAVIGATION",
            (
                panel_x + 17,
                PANEL_Y + 17
            ),
            self.theme["secondary"],
            FONT_NAME,
            TEXT_FONT_SIZE
        )

        start_y = (
            PANEL_Y + 50
        )

        for index, item in enumerate(MENU_ITEMS):
            selected = (
                index == self.selected_index
            )

            prefix = (
                "> "
                if selected
                else "  "
            )

            color = (
                self.theme["accent"]
                if selected
                else self.theme["primary"]
            )

            draw_text(
                surface,
                prefix + item,
                (
                    panel_x + 17,
                    start_y + index * 27
                ),
                color,
                FONT_NAME,
                MENU_FONT_SIZE
            )
#-----------------------------


#=============================#
# CONTENT PANEL               #
#=============================#
#-----------------------------
    def draw_content_panel(
        self,
        surface,
        panel_x
    ):
        selected_item = MENU_ITEMS[self.selected_index]

        draw_box(
            surface,
            panel_x,
            PANEL_Y,
            RIGHT_PANEL_COLUMNS,
            PANEL_ROWS,
            self.theme["primary"],
            DOUBLE,
            FONT_NAME,
            FRAME_FONT_SIZE
        )

        draw_preview = MENU_PREVIEWS[selected_item]

        draw_preview(
            surface,
            panel_x,
            PANEL_Y,
            self.theme,
            FONT_NAME,
            TITLE_FONT_SIZE,
            TEXT_FONT_SIZE
        )
#-----------------------------


#=============================#
# FOOTER                      #
#=============================#
#-----------------------------
    def draw_footer(self, surface):
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
                338
            ),
            self.theme["secondary"],
            FONT_NAME,
            FOOTER_FONT_SIZE,
            center=True
        )
#-----------------------------
