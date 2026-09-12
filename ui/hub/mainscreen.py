#=============================#
# IMPORTS                     #
#=============================#
#-----------------------------
import pygame

from ascii.frames import DOUBLE
from engine.controls import get_menu_confirm
from engine.controls import get_menu_navigation
from ui.hub.previews.about_preview import draw_about_preview
from ui.hub.previews.exit_preview import draw_exit_preview
from ui.hub.previews.games_preview import draw_games_preview
from ui.hub.previews.options_preview import draw_options_preview
from ui.hub.previews.scores_preview import draw_scores_preview
from ui.layout import FONT_NAME
from ui.layout import FOOTER_FONT_SIZE
from ui.layout import FOOTER_Y
from ui.layout import FRAME_FONT_SIZE
from ui.layout import LEFT_PANEL_COLUMNS
from ui.layout import LOGO_FONT_SIZE
from ui.layout import LOGO_Y
from ui.layout import MENU_FONT_SIZE
from ui.layout import PANEL_ROWS
from ui.layout import PANEL_Y
from ui.layout import RIGHT_PANEL_COLUMNS
from ui.layout import TEXT_FONT_SIZE
from ui.layout import TITLE_FONT_SIZE
from ui.layout import get_panel_positions
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

        confirm = get_menu_confirm(
            events
        )

        if confirm:
            selected_item = MENU_ITEMS[
                self.selected_index
            ]

            return selected_item

        return None

    def draw(
        self,
        surface,
        animation_elapsed_ms
    ):
        surface.fill(
            self.theme["background"]
        )

        elapsed_ms = pygame.time.get_ticks()

        left_x, right_x = get_panel_positions(
            surface
        )

        draw_pycade_logo(
            surface,
            surface.get_width() // 2,
            LOGO_Y,
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
            right_x,
            animation_elapsed_ms
        )

        self.draw_footer(
            surface
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
        panel_x,
        animation_elapsed_ms
    ):
        selected_item = MENU_ITEMS[
            self.selected_index
        ]

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

        draw_preview = MENU_PREVIEWS[
            selected_item
        ]

        draw_preview(
            surface,
            panel_x,
            PANEL_Y,
            self.theme,
            FONT_NAME,
            TITLE_FONT_SIZE,
            TEXT_FONT_SIZE,
            animation_elapsed_ms
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
                FOOTER_Y
            ),
            self.theme["secondary"],
            FONT_NAME,
            FOOTER_FONT_SIZE,
            center=True
        )
#-----------------------------