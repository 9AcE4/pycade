#=============================#
# IMPORTS                     #
#=============================#
#-----------------------------
import pygame

from ascii.frames import THIN
from ui.rendering import draw_box
from ui.rendering import draw_text
#-----------------------------


#=============================#
# PREVIEW CONTENT             #
#=============================#
#-----------------------------
TITLE = "GAMES"
DESCRIPTION = "To game library"
#-----------------------------


#=============================#
# SNAKE DEMO CONFIG           #
#=============================#
#-----------------------------
# An even column count keeps the demo route closed.
DEMO_COLUMNS = 26
DEMO_ROWS = 5

DEMO_OFFSET_X = 19
DEMO_OFFSET_Y = 90

DEMO_STEP_MS = 180
DEMO_INITIAL_LENGTH = 6
DEMO_FIRST_FOOD_STEP = 12
DEMO_FOOD_INTERVAL = 18

DEMO_SNAKE_CHARACTER = "●"
DEMO_FOOD_CHARACTER = "○"
#-----------------------------


#=============================#
# SNAKE DEMO PATH             #
#=============================#
#-----------------------------
def build_demo_path():
    path = [
        (0, row)
        for row in range(DEMO_ROWS)
    ]

    for column in range(1, DEMO_COLUMNS):
        if column % 2 == 1:
            rows = range(DEMO_ROWS - 1, 0, -1)
        else:
            rows = range(1, DEMO_ROWS)

        path.extend(
            (column, row)
            for row in rows
        )

    path.extend(
        (column, 0)
        for column in range(DEMO_COLUMNS - 1, 0, -1)
    )

    return tuple(path)


DEMO_PATH = build_demo_path()

DEMO_FOOD_STEPS = tuple(
    range(
        DEMO_FIRST_FOOD_STEP,
        len(DEMO_PATH),
        DEMO_FOOD_INTERVAL
    )
)
#-----------------------------


#=============================#
# SNAKE DEMO FRAME            #
#=============================#
#-----------------------------
def get_demo_frame(elapsed_ms):
    head_index = (
        elapsed_ms // DEMO_STEP_MS
    ) % len(DEMO_PATH)

    food_eaten = sum(
        food_step <= head_index
        for food_step in DEMO_FOOD_STEPS
    )

    snake_length = (
        DEMO_INITIAL_LENGTH + food_eaten
    )

    snake_cells = tuple(
        DEMO_PATH[
            (head_index - offset) % len(DEMO_PATH)
        ]
        for offset in range(snake_length)
    )

    next_food_index = next(
        (
            food_step
            for food_step in DEMO_FOOD_STEPS
            if food_step > head_index
        ),
        DEMO_FOOD_STEPS[0]
    )

    return snake_cells, DEMO_PATH[next_food_index]
#-----------------------------


#=============================#
# DRAW SNAKE DEMO             #
#=============================#
#-----------------------------
def draw_snake_demo(
    surface,
    panel_x,
    panel_y,
    theme,
    font_name,
    font_size,
    elapsed_ms
):
    font = pygame.font.SysFont(
        font_name,
        font_size
    )

    character_width = font.size("M")[0]
    line_height = font.get_linesize()
    cell_width = character_width * 2

    demo_x = panel_x + DEMO_OFFSET_X
    demo_y = panel_y + DEMO_OFFSET_Y

    draw_box(
        surface,
        demo_x,
        demo_y,
        DEMO_COLUMNS * 2 + 2,
        DEMO_ROWS + 2,
        theme["secondary"],
        THIN,
        font_name,
        font_size
    )

    snake_cells, food_cell = get_demo_frame(
        elapsed_ms
    )

    head_surface = font.render(
        DEMO_SNAKE_CHARACTER,
        True,
        theme["accent"]
    )

    body_surface = font.render(
        DEMO_SNAKE_CHARACTER,
        True,
        theme["primary"]
    )

    food_surface = font.render(
        DEMO_FOOD_CHARACTER,
        True,
        theme["accent"]
    )

    field_x = demo_x + character_width
    field_y = demo_y + line_height

    for index, (column, row) in enumerate(snake_cells):
        segment_surface = (
            head_surface
            if index == 0
            else body_surface
        )

        surface.blit(
            segment_surface,
            (
                field_x
                + column * cell_width
                + (cell_width - segment_surface.get_width()) // 2,
                field_y + row * line_height
            )
        )

    food_column, food_row = food_cell

    surface.blit(
        food_surface,
        (
            field_x
            + food_column * cell_width
            + (cell_width - food_surface.get_width()) // 2,
            field_y + food_row * line_height
        )
    )
#-----------------------------


#=============================#
# DRAW PREVIEW                #
#=============================#
#-----------------------------
def draw_games_preview(
    surface,
    panel_x,
    panel_y,
    theme,
    font_name,
    title_font_size,
    text_font_size,
    animation_elapsed_ms
):
    draw_text(
        surface,
        TITLE,
        (
            panel_x + 19,
            panel_y + 17
        ),
        theme["accent"],
        font_name,
        title_font_size
    )

    draw_text(
        surface,
        DESCRIPTION,
        (
            panel_x + 19,
            panel_y + 61
        ),
        theme["primary"],
        font_name,
        text_font_size
    )

    draw_snake_demo(
        surface,
        panel_x,
        panel_y,
        theme,
        font_name,
        text_font_size,
        animation_elapsed_ms
    )
#-----------------------------
