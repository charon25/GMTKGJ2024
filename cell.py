import pygame as pyg

import constants
import textures
from constants import CellType, CellData
from window import Scale


class Cell:
    def __init__(self, x: int, y: int, width: int = 1, height: int = 1, _type: CellType = CellType.BASE):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.type = _type
        self.cell_data: CellData = constants.CELL_DATA[self.type.value]
        self.rect: pyg.Rect = None
        self.index: int = -1

        self.selected: bool = False
        self.temp_selected: bool = False

    def __lt__(self, other: 'Cell'):
        return (self.y, self.x) < (other.y, other.x)

    def generate(self, cell_size: int, index: int):
        self.rect = pyg.Rect(self.x * cell_size, self.y * cell_size, self.width * cell_size, self.height * cell_size)
        self.index = index

    def select(self):
        self.selected = True
        self.temp_selected = False

    def unselect(self):
        self.selected = False
        self.temp_selected = False

    def __get_select_count(self):
        return self.selected + self.temp_selected

    def __get_main_texture(self) -> pyg.Surface:
        return textures.CELL_TEXTURES[self.cell_data.main_texture][self.__get_select_count()].get_current_sprite()

    def __get_modifier_texture(self) -> pyg.Surface:
        return textures.MODIFIERS_TEXTURES[self.cell_data.modifier_texture].get_current_sprite()

    def draw(self, surface: pyg.Surface, x_offset: int, y_offset: int, scale: Scale):
        surface.blit(pyg.transform.scale(self.__get_main_texture(), (self.rect.w, self.rect.h)),
                     scale.to_screen_pos(self.rect.x + x_offset, self.rect.y + y_offset))

        if self.cell_data.modifier_texture >= 0:
            surface.blit(pyg.transform.scale(self.__get_modifier_texture(), (self.rect.w, self.rect.h)),
                         scale.to_screen_pos(self.rect.x + x_offset, self.rect.y + y_offset))

    def contains_point(self, x: int, y: int):
        return self.rect.collidepoint(x, y)

    def get_points(self):
        # todo
        return int(self.width * self.height * 1.25)
