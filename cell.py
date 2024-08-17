import pygame as pyg

import constants
from screen_shake import SHAKER
import textures
from cell_animation import CellAnimation, CellSelectAnimation
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

        self.points = 0

        self.animation: CellAnimation | None = None

    def __lt__(self, other: 'Cell'):
        return (self.y, self.x) < (other.y, other.x)

    def generate(self, cell_size: int, index: int):
        self.rect = pyg.Rect(self.x * cell_size, self.y * cell_size, self.width * cell_size, self.height * cell_size)
        self.index = index

    def select(self, order: int):
        self.selected = True
        self.temp_selected = False
        self.animation = CellSelectAnimation(order)

    def unselect(self, order: int = -1):
        self.selected = False
        self.temp_selected = False
        self.animation = None
        self.points = 0

    def __get_select_count(self):
        return self.selected + self.temp_selected

    def __get_main_texture(self) -> pyg.Surface:
        return textures.CELL_TEXTURES[self.cell_data.main_texture][self.__get_select_count()].get_current_sprite()

    def __get_modifier_texture(self) -> pyg.Surface:
        return textures.MODIFIERS_TEXTURES[self.cell_data.modifier_texture].get_current_sprite()

    def draw(self, surface: pyg.Surface, x_offset: int, y_offset: int, scale: Scale, dt: float):
        if self.animation is not None:
            self.animation.update(dt)

            anim_scale = self.animation.get_scale()
            if anim_scale != 1:
                x_offset += self.rect.w * (1 - anim_scale) / 2
                y_offset += self.rect.h * (1 - anim_scale) / 2

            if self.animation.is_finished:
                self.animation = None
                SHAKER.shake(1 + self.points + self.cell_data.points_multiplier)
                print(self.points)
                # todo ajouter son
        else:
            anim_scale = 1.0

        surface.blit(pyg.transform.scale(self.__get_main_texture(), (self.rect.w * anim_scale, self.rect.h * anim_scale)),
                     scale.to_screen_pos(self.rect.x + x_offset, self.rect.y + y_offset))

        if self.cell_data.modifier_texture >= 0:
            surface.blit(pyg.transform.scale(self.__get_modifier_texture(), (self.rect.w * anim_scale, self.rect.h * anim_scale)),
                         scale.to_screen_pos(self.rect.x + x_offset, self.rect.y + y_offset))

    def contains_point(self, x: int, y: int):
        return self.rect.collidepoint(x, y)

    def get_points(self):
        # todo
        return int(self.width * self.height * 1.25)
