import pygame as pyg

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
        color = (0, 0, 0) if not self.is_hovered else (255, 0, 0)
        pyg.draw.circle(surface, color, scale.to_screen_pos(self.x + x_offset, self.y + y_offset),
                        self.radius * scale.scale, width=width)
        if self.is_hovered:
            surface.blit(textures.REMOVE_CIRCLE, (self.x - co.REMOVE_CIRCLE_TEXTURE_SIZE / 2 + x_offset,
                                                  self.y - co.REMOVE_CIRCLE_TEXTURE_SIZE / 2 + y_offset))

    def contains_point(self, x: int, y: int):
        return (x - self.x) ** 2 + (y - self.y) ** 2 <= self.radius ** 2

    def contains_rect(self, rect: pyg.Rect):
        return (self.contains_point(rect.x, rect.y) and self.contains_point(rect.x + rect.w, rect.y)
                and self.contains_point(rect.x, rect.y + rect.h) and self.contains_point(rect.x + rect.w,
                                                                                         rect.y + rect.h))

    def touch_rect(self, rect: pyg.Rect):
        return (self.contains_point(rect.x, rect.y) or self.contains_point(rect.x + rect.w, rect.y)
                or self.contains_point(rect.x, rect.y + rect.h) or self.contains_point(rect.x + rect.w, rect.y + rect.h)
                or rect.collidepoint(self.x, self.y))

    def touch_circle(self, other: 'Circle'):
        return (self.x - other.x) ** 2 + (self.y - other.y) ** 2 <= (self.radius + other.radius) ** 2
