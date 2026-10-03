#=============================#
# IMPORTS                     #
#=============================#
#-----------------------------
from ui.rendering import draw_text
#-----------------------------


#=============================#
# PREVIEW CONTENT             #
#=============================#
#-----------------------------
TITLE = "OPTIONS"
DESCRIPTION = "Customize PyCade"
#-----------------------------


#=============================#
# DRAW PREVIEW                #
#=============================#
#-----------------------------
def draw_options_preview(
    surface,
    panel_x,
    panel_y,
    theme,
    font_path,
    title_font_size,
    text_font_size,
    _animation_elapsed_ms
):
    draw_text(
        surface,
        TITLE,
        (
            panel_x + 19,
            panel_y + 17
        ),
        theme["accent"],
        font_path,
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
        font_path,
        text_font_size
    )
#-----------------------------
