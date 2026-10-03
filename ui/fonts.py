"""Load the bundled UI font independently of installed system fonts."""

from pathlib import Path

import pygame


FONT_PATH = (
    Path(__file__).resolve().parent.parent
    / "assets" / "fonts" / "LiberationMono-Regular.ttf"
)


def load_font(font_path, font_size):
    """Load a font file; missing or invalid assets raise a visible error."""
    return pygame.font.Font(str(font_path), font_size)
