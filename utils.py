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


def draw_text(screen: pyg.Surface, text: str, size: int, pos: tuple[float, float], color: tuple[int, int, int], bold=False,
              italic=False, underline=False):
    font: pyg.font.Font = get_font(size, bold=bold, italic=italic, underline=underline)
    img = font.render(text, False, color)
    screen.blit(img, pos)


def draw_text_center(screen: pyg.Surface, text: str, size: int, rect: pyg.Rect, color: tuple[int, int, int], bold=False,
                     italic=False, underline=False):
    font: pyg.font.Font = get_font(size, bold=bold, italic=italic, underline=underline)
    img = font.render(text, False, color)
    screen.blit(img, (rect.centerx - img.get_width() / 2, rect.centery - img.get_height() / 2))


def blit_scaled(screen: pyg.Surface, img: pyg.Surface, x: int, y: int, scale: float):
    scaled_img = pyg.transform.scale_by(img, scale)
    dx = (scaled_img.get_width() - img.get_width()) / 2
    dy = (scaled_img.get_height() - img.get_height()) / 2
    screen.blit(scaled_img, (x - dx, y - dy))
