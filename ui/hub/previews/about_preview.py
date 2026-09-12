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
TITLE = "ABOUT"
DESCRIPTION = "About PyCade"
#-----------------------------


#=============================#
# DRAW PREVIEW                #
#=============================#
#-----------------------------
def draw_about_preview(
    surface,
    panel_x,
    panel_y,
    theme,
    font_name,
    title_font_size,
    text_font_size
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
#-----------------------------
