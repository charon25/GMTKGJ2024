import pygame as pyg


class Circle:
    def __init__(self, x: int, y: int, radius: float):
        self.x = x
        self.y = y
        self.radius = radius

    def draw(self, surface: pyg.Surface):
        width = max(1, int(self.radius**0.5 / 2.5))
        pyg.draw.circle(surface, (0, 0, 0), (self.x, self.y), self.radius, width=width)

    def contains_point(self, x: int, y: int):
        return (x - self.x) ** 2 + (y - self.y) ** 2 <= self.radius ** 2

    def contains_rect(self, rect: pyg.Rect):
        return (self.contains_point(rect.x, rect.y) and self.contains_point(rect.x + rect.w, rect.y)
                and self.contains_point(rect.x, rect.y + rect.h) and self.contains_point(rect.x + rect.w, rect.y + rect.h))
