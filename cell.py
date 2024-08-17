from typing import Callable

import pygame as pyg

import constants
import textures
from cell_animation import CellAnimation, CellSelectAnimation
from constants import CellType, CellData
from screen_shake import SHAKER
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
        self.on_select: Callable[['Cell'], None] = lambda cell: None

        self.selected: bool = False
        self.temp_selected: bool = False

        self.points: float = 0.0

        self.animation: CellAnimation | None = None
        self.displayed: bool = True
        self.vector = (0.0, 0.0)
        self.velocity = (0.0, 0.0)
        self.temp_rect: pyg.Rect = None

    def __lt__(self, other: 'Cell'):
        return (self.y, self.x) < (other.y, other.x)

    def generate(self, cell_size: int, index: int, on_select: Callable[['Cell'], None]):
        self.rect = pyg.Rect(self.x * cell_size, self.y * cell_size, self.width * cell_size, self.height * cell_size)
        self.index = index
        self.on_select = on_select

    def set_temp_rect(self, cell_size: int, x: int, y: int):
        self.temp_rect = pyg.Rect(x, y, self.width * cell_size, self.height * cell_size)

    def is_in_place(self) -> bool:
        return (self.temp_rect.centerx - self.rect.centerx) ** 2 + (
                    self.temp_rect.centery - self.rect.centery) ** 2 < 5000

    def is_outside_screen(self, x_offset: int, y_offset: int):
        return (self.temp_rect.right + x_offset < 0 or self.temp_rect.left + x_offset > constants.WIDTH
                or self.temp_rect.bottom + y_offset < 0 or self.temp_rect.top + y_offset > constants.HEIGHT)

    def select(self, order: int):
        self.selected = True
        self.temp_selected = False
        self.animation = CellSelectAnimation(order)

    def unselect(self, order: int = -1):
        self.selected = False
        self.temp_selected = False
        self.animation = None
        self.points = 0.0

    def __get_select_count(self):
        return self.selected + self.temp_selected

    def __get_main_texture(self) -> pyg.Surface:
        return textures.CELL_TEXTURES[self.cell_data.main_texture][self.__get_select_count()].get_current_sprite()

    def __get_modifier_texture(self) -> pyg.Surface:
        return textures.MODIFIERS_TEXTURES[self.cell_data.modifier_texture].get_current_sprite()

    def draw(self, surface: pyg.Surface, x_offset: int, y_offset: int, scale: Scale, dt: float):
        if not self.displayed:
            return

        rect = self.rect if self.temp_rect is None else self.temp_rect

        if self.animation is not None:
            self.animation.update(dt)

            anim_scale = self.animation.get_scale()
            if anim_scale != 1:
                x_offset += rect.w * (1 - anim_scale) / 2
                y_offset += rect.h * (1 - anim_scale) / 2

            if self.animation.is_finished:
                self.animation = None
                SHAKER.shake(int(1 + self.points + self.cell_data.points_multiplier))
                self.on_select(self)
                # todo ajouter son
        else:
            anim_scale = 1.0

        total_scale = scale.scale * anim_scale
        surface.blit(pyg.transform.scale(self.__get_main_texture(), (rect.w * total_scale, rect.h * total_scale)),
                     scale.to_screen_pos(rect.x + x_offset, rect.y + y_offset))

        if self.cell_data.modifier_texture >= 0:
            surface.blit(pyg.transform.scale(self.__get_modifier_texture(), (
                rect.w * total_scale, rect.h * total_scale)),
                         scale.to_screen_pos(rect.x + x_offset, rect.y + y_offset))

    def contains_point(self, x: int, y: int):
        return self.rect.collidepoint(x, y)

    def get_points(self):
        # todo
        return int(self.width * self.height * 1.25)
