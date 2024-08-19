import pygame as pyg

import constants
import textures
import constants as co
from window import Scale


class Circle:
    def __init__(self, x: int, y: int, radius: float):
        self.x = x
        self.y = y
        self.radius = radius
        self.is_hovered = False

    def __repr__(self):
        return f'({self.x:0f} ; {self.y:.0f}) r={self.radius:.1f}'

    def draw(self, surface: pyg.Surface, x_offset: int, y_offset: int, scale: Scale):
        width = max(1, int(self.radius ** 0.5 / 2.5))
        color = constants.DARK_COLOR if not self.is_hovered else constants.RED_COLOR
        pyg.draw.circle(surface, color, scale.to_screen_pos(self.x + x_offset, self.y + y_offset),
                        self.radius * scale.scale, width=width)
        if self.is_hovered:
            surface.blit(textures.REMOVE_CIRCLE, (self.x - co.REMOVE_CIRCLE_TEXTURE_SIZE / 2 + x_offset,
                                                  self.y - co.REMOVE_CIRCLE_TEXTURE_SIZE / 2 + y_offset))

    def contains_point(self, x: int, y: int):
        return (x - self.x) ** 2 + (y - self.y) ** 2 <= self.radius ** 2

    def contains_rect(self, rect: pyg.Rect):
        left, top, right, bottom = rect.left + co.CELL_OFFSET, rect.top + co.CELL_OFFSET, rect.right - co.CELL_OFFSET, rect.bottom - co.CELL_OFFSET
        return (self.contains_point(left, top) and self.contains_point(right, top)
                and self.contains_point(left, bottom) and self.contains_point(right, bottom))

    def touch_rect(self, rect: pyg.Rect):
        left, top, right, bottom = rect.left + co.CELL_OFFSET, rect.top + co.CELL_OFFSET, rect.right - co.CELL_OFFSET, rect.bottom - co.CELL_OFFSET
        return (self.contains_point(left, top) or self.contains_point(right, top)
                or self.contains_point(left, bottom) or self.contains_point(right, bottom))

    def touch_circle(self, other: 'Circle'):
        return (self.x - other.x) ** 2 + (self.y - other.y) ** 2 <= (self.radius + other.radius) ** 2
