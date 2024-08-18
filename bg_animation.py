import math
import random

import textures
from window import Scale
import pygame as pyg
import constants as co


class BackgroundAnimation:
    def __init__(self, scale: Scale):
        self.cells: list[BackgroundCell] = list()
        self.scale = scale

    def draw(self, screen: pyg.Surface, excl_rect: pyg.Rect | None, dt: float):
        if len(self.cells) < 35:
            x = co.BG_CELL_SIZE * random.randrange(co.WIDTH // co.BG_CELL_SIZE)
            y = co.BG_CELL_SIZE * random.randrange(co.WIDTH // co.BG_CELL_SIZE) + co.BG_CELL_OFFSET_Y
            if excl_rect is None or not excl_rect.colliderect(pyg.Rect(x, y, co.BG_CELL_SIZE, co.BG_CELL_SIZE)):
                self.cells.append(BackgroundCell(x, y, self.scale))

        for i in range(len(self.cells) - 1, -1, -1):
            cell = self.cells[i]
            if cell.lifetime <= 0:
                self.cells.pop(i)
            else:
                cell.draw(screen, dt)


class BackgroundCell:
    def __init__(self, x: int, y: int, scale: Scale):
        self.x = x
        self.y = y
        self.alpha: int = 0
        self.scale = scale
        self.texture = textures.BG_CELL.copy()
        self.initial_lifetime = random.random() * (
                co.BG_CELL_MAX_LIFETIME - co.BG_CELL_MIN_LIFETIME) + co.BG_CELL_MIN_LIFETIME
        self.lifetime: float = self.initial_lifetime

    def draw(self, screen: pyg.Surface, dt: float):
        self.lifetime -= dt
        self.alpha = int(co.BG_CELL_MAX_ALPHA * math.sin(self.lifetime * math.pi / self.initial_lifetime))

        self.texture.set_alpha(self.alpha)

        if self.alpha < 5:
            return

        screen.blit(self.texture, self.scale.to_screen_pos(self.x, self.y))
