import pygame as pyg

import constants as co

FONT_CACHE: dict[int, pyg.font.Font] = dict()
SCALE: float = 1.0


def get_font(size, bold=False, italic=False, underline=False):
    size = int(round(size * SCALE, 0))
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


def draw_text(screen: pyg.Surface, text: str, size: int, pos: tuple[float, float], color: tuple[int, int, int],
              bold=False,
              italic=False, underline=False):
    font: pyg.font.Font = get_font(size, bold=bold, italic=italic, underline=underline)
    img = font.render(text, False, color)
    screen.blit(img, pos)


def draw_text_center(screen: pyg.Surface, text: str, size: int, rect: pyg.Rect, color: tuple[int, int, int],
                     up_down: float = 0.0, bold=False,
                     italic=False, underline=False):
    font: pyg.font.Font = get_font(size, bold=bold, italic=italic, underline=underline)
    img = font.render(text, False, color)
    screen.blit(img, (rect.centerx - img.get_width() / 2, rect.centery - img.get_height() / 2 + up_down))


def draw_text_center_right(screen: pyg.Surface, text: str, size: int, rect: pyg.Rect,
                           color: tuple[int, int, int], bold=False, italic=False, underline=False):
    font: pyg.font.Font = get_font(size, bold=bold, italic=italic, underline=underline)
    img = font.render(text, False, color)
    screen.blit(img, (rect.right - img.get_width(), rect.centery - img.get_height() / 2 + size * co.FONT_Y_OFFSET))


def draw_text_next_to_img(screen: pyg.Surface, img: pyg.Surface, img_pos: tuple[float, float], gap: int, text: str,
                          size: int, color: tuple[int, int, int], scale: float = 1.0, bold=False,
                          italic=False, underline=False):
    if scale == 1.0:
        screen.blit(img, img_pos)
    else:
        blit_scaled(screen, img, img_pos[0], img_pos[1], scale)
    draw_text_center_right(screen, text, size, pyg.Rect(img_pos[0] - gap, img_pos[1], 0, img.get_height()), color,
                           bold=bold, italic=italic, underline=underline)


def draw_text_and_img_centered(screen: pyg.Surface, img: pyg.Surface, text: str,
                               size: int, rect: pyg.Rect, gap: int, color: tuple[int, int, int],
                               bold=False, italic=False, underline=False):
    font: pyg.font.Font = get_font(size, bold=bold, italic=italic, underline=underline)
    text_surf = font.render(text, False, color)
    dw = (rect.width - (img.get_width() + gap + text_surf.get_width())) / 2
    screen.blit(text_surf,
                (rect.left + dw, rect.top + (rect.height - text_surf.get_height()) / 2 + co.FONT_Y_OFFSET * size))
    screen.blit(img, (rect.left + dw + text_surf.get_width() + gap, rect.top + (rect.height - img.get_width()) / 2))


def blit_scaled(screen: pyg.Surface, img: pyg.Surface, x: float, y: float, scale: float):
    scaled_img = pyg.transform.scale_by(img, scale)
    dx = (scaled_img.get_width() - img.get_width()) / 2
    dy = (scaled_img.get_height() - img.get_height()) / 2
    screen.blit(scaled_img, (x - dx, y - dy))
