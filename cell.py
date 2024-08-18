from typing import Callable

import pygame as pyg

import constants
import textures
import utils
from cell_animation import CellAnimation, CellSelectAnimation
from constants import CellType, CellData
from screen_shake import SHAKER
from window import Scale


class Cell:
    def __init__(self, x: int, y: int, size: int = 1, _type: CellType = CellType.BASE):
        self.x = x
        self.y = y
        self.size = size
        self.type = _type
        self.cell_data: CellData = constants.CELL_DATA[self.type.value]
        self.rect: pyg.Rect = None
        self.index: int = -1
        self.on_select: Callable[['Cell'], None] = lambda cell: None
        self.real_size = 99999
        self.texture_size = 99999

        self.selected: bool = False
        self.temp_selected: bool = False

        self.points: float = 0.0

        self.animation: CellAnimation | None = None
        self.displayed: bool = True
        self.vector = (0.0, 0.0)
        self.velocity = (0.0, 0.0)
        self.temp_rect: pyg.Rect = None
        self.previous_sign = 0

        self.flying_text: FlyingText | None = None

    def __lt__(self, other: 'Cell'):
        return (self.y, self.x) < (other.y, other.x)

    def generate(self, cell_size: int, index: int, on_select: Callable[['Cell'], None]):
        self.rect = pyg.Rect(self.x * cell_size, self.y * cell_size, self.size * cell_size, self.size * cell_size)
        self.real_size = self.size * cell_size
        self.texture_size = constants.TEXTURE_INDEX_FROM_SIZE[self.real_size]
        self.index = index
        self.on_select = on_select

    def set_temp_rect(self, cell_size: int, x: int, y: int):
        self.temp_rect = pyg.Rect(x, y, self.size * cell_size, self.size * cell_size)

    def is_in_place(self) -> bool:
        x = self.temp_rect.centerx - self.rect.centerx
        y = self.temp_rect.centery - self.rect.centery
        if abs(x) < 0.0001 and abs(y) < 0.0001:
            return True

        dot = self.vector[0] * (x + self.velocity[0]) + self.vector[1] * (y + self.velocity[1])
        sign = 1 if dot >= 0 else -1
        in_place = (sign == -self.previous_sign)
        self.previous_sign = sign
        return in_place

    def is_outside_screen(self, x_offset: int, y_offset: int):
        return (self.temp_rect.right + x_offset < 0 or self.temp_rect.left + x_offset > constants.WIDTH
                or self.temp_rect.bottom + y_offset < 0 or self.temp_rect.top + y_offset > constants.HEIGHT)

    def select(self, total_selected: int, order: int):
        self.selected = True
        self.temp_selected = False
        self.animation = CellSelectAnimation(total_selected, order)

    def unselect(self, order: int = -1):
        self.selected = False
        self.temp_selected = False
        self.animation = None
        self.points = 0.0

    def __get_select_count(self):
        return self.selected + self.temp_selected

    def __get_main_texture(self) -> pyg.Surface:
        return textures.CELL_TEXTURES[self.cell_data.main_texture][self.__get_select_count()][
            self.texture_size].get_current_sprite()

    def __get_modifier_texture(self) -> pyg.Surface:
        # -1 is because there aren't modifiers for sizes 16 and 32
        return textures.MODIFIERS_TEXTURES[self.cell_data.modifier_texture][self.texture_size - 2].get_current_sprite()

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
                if self.points > 0:
                    SHAKER.shake(int(1 + self.points))
                self.on_select(self)
                self.flying_text = FlyingText(int(self.points), self.rect)
                # todo ajouter son
        else:
            anim_scale = 1.0

        total_scale = scale.scale * anim_scale
        surface.blit(pyg.transform.scale(self.__get_main_texture(), (rect.w * total_scale, rect.h * total_scale)),
                     scale.to_screen_pos(rect.x + x_offset, rect.y + y_offset))

        if self.cell_data.modifier_texture >= 0 and self.real_size in constants.VALID_MULTIPLIER_SIZES:
            surface.blit(pyg.transform.scale(self.__get_modifier_texture(), (
                rect.w * total_scale, rect.h * total_scale)),
                         scale.to_screen_pos(rect.x + x_offset, rect.y + y_offset))

        if self.flying_text is not None:
            self.flying_text.draw(surface, x_offset, y_offset, scale, dt)

            if self.flying_text.lifetime <= 0:
                self.flying_text = None

    def contains_point(self, x: int, y: int):
        return self.rect.collidepoint(x, y)

    def get_points(self):
        return constants.POINTS_FROM_SIZE[self.real_size]


class FlyingText:
    def __init__(self, value: int, cell_rect: pyg.Rect):
        self.text: str = f'+{value:.0f}'
        self.x: float = cell_rect.centerx
        self.y: float = cell_rect.top
        self.lifetime: float = 1

    def draw(self, screen: pyg.Surface, x_offset: int, y_offset: int, scale: Scale, dt: float):
        self.lifetime -= dt
        self.y -= 10 * dt

        font = utils.get_font(24)
        text = font.render(self.text, False, constants.DARK_COLOR)
        text_white = font.render(self.text, False, constants.LIGHT_COLOR)
        x = self.x - text.get_width() / 2 + x_offset
        y = self.y - text.get_width() / 2 + y_offset
        for dx in (-2, 0, 2):
            for dy in (-2, 0, 2):
                screen.blit(text_white, scale.to_screen_pos(x + dx, y + dy))

        screen.blit(text, scale.to_screen_pos(x, y))
