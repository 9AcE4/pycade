#=============================#
# IMPORTS                     #
#=============================#
#-----------------------------
import textwrap

import pygame

from ascii.frames import DOUBLE
from engine.controls import get_menu_back
from engine.controls import get_menu_confirm
from engine.controls import get_menu_navigation
from games.catalog import load_game_catalog
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
# GAME SELECTION CONFIG       #
#=============================#
#-----------------------------
ACTION_BACK = "BACK"
ACTION_SELECT = "SELECT"

GAME_ITEM_SPACING = 27
VISIBLE_GAME_COUNT = 5

DESCRIPTION_COLUMNS = (
    RIGHT_PANEL_COLUMNS - 8
)

MAX_DESCRIPTION_LINES = 5
DESCRIPTION_LINE_SPACING = 17
#-----------------------------


#=============================#
# GAME SELECTION SCREEN       #
#=============================#
#-----------------------------
class GameSelectionScreen:
    def __init__(self, theme_name=DEFAULT_THEME):
        self.theme = THEMES[theme_name]

        self.games = load_game_catalog()

        self.selected_index = 0
        self.first_visible_index = 0

    def update(self, events):
        if get_menu_back(
            events
        ):
            return ACTION_BACK

        if self.games:
            navigation = get_menu_navigation(
                events
            )

            self.selected_index = (
                self.selected_index + navigation
            ) % len(self.games)

            self.update_scroll_position()

            if get_menu_confirm(
                events
            ):
                return ACTION_SELECT

        return None

    def get_selected_game(self):
        if not self.games:
            return None

        return self.games[
            self.selected_index
        ]

    def update_scroll_position(self):
        if self.selected_index < self.first_visible_index:
            self.first_visible_index = (
                self.selected_index
            )

        visible_end = (
            self.first_visible_index
            + VISIBLE_GAME_COUNT
        )

        if self.selected_index >= visible_end:
            self.first_visible_index = (
                self.selected_index
                - VISIBLE_GAME_COUNT
                + 1
            )

    def draw(self, surface):
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

        self.draw_game_list_panel(
            surface,
            left_x
        )

        self.draw_game_info_panel(
            surface,
            right_x
        )

        self.draw_footer(
            surface
        )
#-----------------------------


#=============================#
# GAME LIST PANEL             #
#=============================#
#-----------------------------
    def draw_game_list_panel(
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
            "GAME LIBRARY",
            (
                panel_x + 17,
                PANEL_Y + 17
            ),
            self.theme["secondary"],
            FONT_NAME,
            TEXT_FONT_SIZE
        )

        if not self.games:
            draw_text(
                surface,
                "NO GAMES FOUND",
                (
                    panel_x + 17,
                    PANEL_Y + 50
                ),
                self.theme["primary"],
                FONT_NAME,
                TEXT_FONT_SIZE
            )

            return

        start_y = (
            PANEL_Y + 50
        )

        visible_games = self.games[
            self.first_visible_index:
            self.first_visible_index
            + VISIBLE_GAME_COUNT
        ]

        for visible_index, game in enumerate(
            visible_games
        ):
            game_index = (
                self.first_visible_index
                + visible_index
            )

            selected = (
                game_index
                == self.selected_index
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
                prefix + game.title,
                (
                    panel_x + 17,
                    start_y
                    + visible_index
                    * GAME_ITEM_SPACING
                ),
                color,
                FONT_NAME,
                MENU_FONT_SIZE
            )
#-----------------------------


#=============================#
# GAME INFO PANEL             #
#=============================#
#-----------------------------
    def draw_game_info_panel(
        self,
        surface,
        panel_x
    ):
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

        draw_text(
            surface,
            "GAME INFO",
            (
                panel_x + 17,
                PANEL_Y + 17
            ),
            self.theme["secondary"],
            FONT_NAME,
            TEXT_FONT_SIZE
        )

        selected_game = self.get_selected_game()

        if selected_game is None:
            draw_text(
                surface,
                "NO GAME SELECTED",
                (
                    panel_x + 17,
                    PANEL_Y + 50
                ),
                self.theme["primary"],
                FONT_NAME,
                TEXT_FONT_SIZE
            )

            return

        draw_text(
            surface,
            selected_game.title,
            (
                panel_x + 17,
                PANEL_Y + 50
            ),
            self.theme["accent"],
            FONT_NAME,
            TITLE_FONT_SIZE
        )

        draw_text(
            surface,
            "DESCRIPTION",
            (
                panel_x + 17,
                PANEL_Y + 82
            ),
            self.theme["secondary"],
            FONT_NAME,
            TEXT_FONT_SIZE
        )

        description_lines = self.get_description_lines(
            selected_game.description
        )

        description_y = (
            PANEL_Y + 105
        )

        for line_index, line in enumerate(
            description_lines
        ):
            draw_text(
                surface,
                line,
                (
                    panel_x + 17,
                    description_y
                    + line_index
                    * DESCRIPTION_LINE_SPACING
                ),
                self.theme["primary"],
                FONT_NAME,
                TEXT_FONT_SIZE
            )
#-----------------------------


#=============================#
# DESCRIPTION WRAPPING        #
#=============================#
#-----------------------------
    def get_description_lines(
        self,
        description
    ):
        lines = textwrap.wrap(
            description,
            width=DESCRIPTION_COLUMNS,
            break_long_words=False,
            break_on_hyphens=False
        )

        if len(lines) <= MAX_DESCRIPTION_LINES:
            return lines

        visible_lines = lines[
            :MAX_DESCRIPTION_LINES
        ]

        last_line = visible_lines[-1]

        if len(last_line) >= 3:
            last_line = (
                last_line[:-3]
                + "..."
            )
        else:
            last_line += "..."

        visible_lines[-1] = last_line

        return visible_lines
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