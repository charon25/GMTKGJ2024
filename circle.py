import pygame as pyg

from window import Scale


class Circle:
    def __init__(self, x: int, y: int, radius: float):
        self.x = x
        self.y = y
        self.radius = radius

    def draw(self, surface: pyg.Surface, x_offset: int, y_offset: int, scale: Scale):
        width = max(1, int(self.radius**0.5 / 2.5))
        pyg.draw.circle(surface, (0, 0, 0), scale.to_game_pos(self.x + x_offset, self.y + y_offset), self.radius * scale.scale, width=width)

    def contains_point(self, x: int, y: int):
        return (x - self.x) ** 2 + (y - self.y) ** 2 <= self.radius ** 2

    def contains_rect(self, rect: pyg.Rect):
        return (self.contains_point(rect.x, rect.y) and self.contains_point(rect.x + rect.w, rect.y)
                and self.contains_point(rect.x, rect.y + rect.h) and self.contains_point(rect.x + rect.w, rect.y + rect.h))

    def touch_rect(self, rect: pyg.Rect):
        return (self.contains_point(rect.x, rect.y) or self.contains_point(rect.x + rect.w, rect.y)
                or self.contains_point(rect.x, rect.y + rect.h) or self.contains_point(rect.x + rect.w, rect.y + rect.h)
                or rect.collidepoint(self.x, self.y))
