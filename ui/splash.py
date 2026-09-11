#=============================#
# IMPORTS                     #
#=============================#
#-----------------------------
import pygame

from ascii.logos import PYCADE_LOGO
from ui.themes import DEFAULT_THEME
from ui.themes import PYCADE_GRADIENT
from ui.themes import PYCADE_GRADIENT_SPEED
from ui.themes import THEMES
#-----------------------------


#=============================#
# SPLASH 1 - MEPY             #
#=============================#
#-----------------------------
INTRO_TITLE = "MePy"
INTRO_SUBTITLE = "presents"

INTRO_TITLE_SIZE = 24
INTRO_SUBTITLE_SIZE = 16

INTRO_FADE_IN = 1800
INTRO_HOLD = 3200
INTRO_FADE_OUT = 1800

INTRO_DURATION = (
    INTRO_FADE_IN
    + INTRO_HOLD
    + INTRO_FADE_OUT
)


def draw_splash_1(surface, elapsed_ms, theme):
    alpha = get_splash_1_alpha(elapsed_ms)

    title_font = pygame.font.SysFont(
        "consolas",
        INTRO_TITLE_SIZE
    )

    subtitle_font = pygame.font.SysFont(
        "consolas",
        INTRO_SUBTITLE_SIZE
    )

    title_surface = title_font.render(
        INTRO_TITLE,
        True,
        theme["primary"]
    )

    subtitle_surface = subtitle_font.render(
        INTRO_SUBTITLE,
        True,
        theme["secondary"]
    )

    title_surface.set_alpha(alpha)
    subtitle_surface.set_alpha(alpha)

    center_x = surface.get_width() // 2
    center_y = surface.get_height() // 2

    title_rect = title_surface.get_rect(
        center=(center_x, center_y - 12)
    )

    subtitle_rect = subtitle_surface.get_rect(
        center=(center_x, center_y + 14)
    )

    surface.blit(
        title_surface,
        title_rect
    )

    surface.blit(
        subtitle_surface,
        subtitle_rect
    )


def get_splash_1_alpha(elapsed_ms):
    if elapsed_ms < INTRO_FADE_IN:
        progress = elapsed_ms / INTRO_FADE_IN

        return int(
            255 * progress
        )

    hold_end = (
        INTRO_FADE_IN
        + INTRO_HOLD
    )

    if elapsed_ms < hold_end:
        return 255

    fade_out_elapsed = (
        elapsed_ms
        - hold_end
    )

    progress = (
        fade_out_elapsed
        / INTRO_FADE_OUT
    )

    return max(
        0,
        int(
            255 * (1 - progress)
        )
    )
#-----------------------------


#=============================#
# SPLASH 2 - PYCADE           #
#=============================#
#-----------------------------
LOGO_FONT_NAME = "consolas"
LOGO_FONT_SIZE = 11

LOGO_FADE_IN = 1800

PRESS_ENTER_TEXT = "press enter"
PRESS_ENTER_SIZE = 14
PRESS_ENTER_MIN_TIME = 2000
PRESS_ENTER_OFFSET_Y = 70

EXIT_FADE_OUT = 1200


def draw_splash_2(
    surface,
    elapsed_ms,
    exit_alpha
):
    logo_alpha = get_logo_alpha(
        elapsed_ms
    )

    final_alpha = min(
        logo_alpha,
        exit_alpha
    )

    logo_lines = (
        PYCADE_LOGO
        .strip("\n")
        .splitlines()
    )

    font = pygame.font.SysFont(
        LOGO_FONT_NAME,
        LOGO_FONT_SIZE
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

    logo_height = (
        len(logo_lines)
        * line_height
    )

    start_x = (
        surface.get_width()
        - logo_width
    ) // 2

    start_y = (
        surface.get_height()
        - logo_height
    ) // 2

    for row, line in enumerate(logo_lines):
        y = (
            start_y
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
                final_alpha
            )

            surface.blit(
                character_surface,
                (x, y)
            )


def draw_press_enter(
    surface,
    theme,
    alpha
):
    font = pygame.font.SysFont(
        "consolas",
        PRESS_ENTER_SIZE
    )

    text_surface = font.render(
        PRESS_ENTER_TEXT,
        True,
        theme["primary"]
    )

    text_surface.set_alpha(alpha)

    text_rect = text_surface.get_rect(
        center=(
            surface.get_width() // 2,
            (
                surface.get_height() // 2
                + PRESS_ENTER_OFFSET_Y
            )
        )
    )

    surface.blit(
        text_surface,
        text_rect
    )


def get_logo_alpha(elapsed_ms):
    progress = min(
        1.0,
        elapsed_ms / LOGO_FADE_IN
    )

    return int(
        255 * progress
    )


def get_gradient_color(position, elapsed_ms):
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

    red = int(
        color_a[0]
        + (
            color_b[0]
            - color_a[0]
        ) * blend
    )

    green = int(
        color_a[1]
        + (
            color_b[1]
            - color_a[1]
        ) * blend
    )

    blue = int(
        color_a[2]
        + (
            color_b[2]
            - color_a[2]
        ) * blend
    )

    return (
        red,
        green,
        blue
    )
#-----------------------------


#=============================#
# SPLASH FLOW                 #
#=============================#
#-----------------------------
class Splash:
    def __init__(self, theme_name=DEFAULT_THEME):
        self.theme = THEMES[theme_name]

        self.start_time = pygame.time.get_ticks()

        self.ready = False
        self.finished = False

        self.exit_requested = False
        self.exit_start_time = None

    def set_ready(self):
        self.ready = True

    def update(self):
        if self.finished:
            return

        current_time = pygame.time.get_ticks()

        elapsed_ms = (
            current_time
            - self.start_time
        )

        if elapsed_ms < INTRO_DURATION:
            return

        splash_2_elapsed = (
            elapsed_ms
            - INTRO_DURATION
        )

        press_enter_visible = (
            self.ready
            and splash_2_elapsed
            >= PRESS_ENTER_MIN_TIME
        )

        if (
            press_enter_visible
            and not self.exit_requested
            and pygame.key.get_pressed()[pygame.K_RETURN]
        ):
            self.exit_requested = True
            self.exit_start_time = current_time

        if self.exit_requested:
            exit_elapsed = (
                current_time
                - self.exit_start_time
            )

            if exit_elapsed >= EXIT_FADE_OUT:
                self.finished = True

    def draw(self, surface):
        surface.fill(
            self.theme["background"]
        )

        if self.finished:
            return

        current_time = pygame.time.get_ticks()

        elapsed_ms = (
            current_time
            - self.start_time
        )

        if elapsed_ms < INTRO_DURATION:
            draw_splash_1(
                surface,
                elapsed_ms,
                self.theme
            )

            return

        splash_2_elapsed = (
            elapsed_ms
            - INTRO_DURATION
        )

        exit_alpha = self.get_exit_alpha(
            current_time
        )

        draw_splash_2(
            surface,
            splash_2_elapsed,
            exit_alpha
        )

        if (
            self.ready
            and splash_2_elapsed
            >= PRESS_ENTER_MIN_TIME
        ):
            draw_press_enter(
                surface,
                self.theme,
                exit_alpha
            )

    def get_exit_alpha(self, current_time):
        if not self.exit_requested:
            return 255

        exit_elapsed = (
            current_time
            - self.exit_start_time
        )

        progress = min(
            1.0,
            exit_elapsed / EXIT_FADE_OUT
        )

        return int(
            255 * (1 - progress)
        )

    def is_finished(self):
        return self.finished
#-----------------------------
