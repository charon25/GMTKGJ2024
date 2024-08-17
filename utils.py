import pygame as pyg

import constants as co

FONT_CACHE: dict[int, pyg.font.Font] = dict()


def get_font(size, bold=False, italic=False, underline=False):
    if size in FONT_CACHE:
        font: pyg.font.Font = FONT_CACHE[size]
    else:
        try:
            font = pyg.font.Font(co.FONT_PATH, size)
        except:
            font = pyg.font.SysFont("arial", size)
        FONT_CACHE[size] = font

    font.set_bold(bold)
    font.set_italic(italic)
    font.set_underline(underline)
    return font


def draw_text(screen: pyg.Surface, text: str, size: int, pos: tuple[float, float], color: pyg.Color, bold=False,
              italic=False, underline=False):
    font: pyg.font.Font = get_font(size, bold=bold, italic=italic, underline=underline)
    img = font.render(text, False, color)
    screen.blit(img, pos)
