import pygame as pyg

import textures
from constants import CellType
from window import Scale


class Cell:
    def __init__(self, x: int, y: int, width: int = 1, height: int = 1, _type: CellType = CellType.BASE):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.type = _type
        self.rect: pyg.Rect = None

        self.selected: bool = False
        self.temp_selected: bool = False

    def generate(self, cell_size: int):
        self.rect = pyg.Rect(self.x * cell_size, self.y * cell_size, self.width * cell_size, self.height * cell_size)

    def __get_texture(self) -> pyg.Surface:
        if self.type == CellType.BASE:
            return textures.BASE_CELL_TX if not self.selected and not self.temp_selected else textures.SELECTED_BASE_CELL_TX
        if self.type == CellType.FORBIDDEN:
            return textures.FORBIDDEN_CELL_TX

    def draw(self, surface: pyg.Surface, x_offset: int, y_offset: int, scale: Scale):
        surface.blit(pyg.transform.scale(self.__get_texture(), (self.rect.w, self.rect.h)),
                     scale.to_screen_pos(self.rect.x + x_offset, self.rect.y + y_offset))

    def contains_point(self, x: int, y: int):
        return self.rect.collidepoint(x, y)
