import pygame as pyg

import constants
from cell import Cell
from circle import Circle
from window import Scale


class Level:
    def __init__(self, number: int, cell_size: int, cells: list[Cell]):
        self.number = number
        self.cell_size = cell_size
        self.cells = cells
        for cell in self.cells:
            cell.generate(cell_size)

        self.x_offset, self.y_offset = self.__get_limits()

        self.circles: list[Circle] = list()
        self.temp_circle: Circle | None = None

    def reset(self):
        self.circles = []
        self.temp_circle = None

    def set_temp_circle_position(self, x: int, y: int):
        if not any(cell.contains_point(x - self.x_offset, y - self.y_offset) for cell in self.cells):
            return

        self.temp_circle = Circle(x, y, 0)

    def widen_temp_circle(self):
        if self.temp_circle is None:
            return

        # todo : voir la taille
        self.temp_circle.radius += 1

    def validate_temp_circle(self):
        if self.temp_circle is None:
            return

        self.circles.append(self.temp_circle)
        self.temp_circle = None

    def __get_limits(self) -> tuple[int, int]:
        min_x: int = constants.WIDTH
        max_x: int = 0
        min_y: int = constants.HEIGHT
        max_y: int = 0
        for cell in self.cells:
            cell.generate(self.cell_size)
            min_x = min(min_x, cell.x * self.cell_size)
            max_x = max(max_x, (cell.x + cell.width) * self.cell_size)
            min_y = min(min_y, cell.y * self.cell_size)
            max_y = max(max_y, (cell.y + cell.height) * self.cell_size)

        return ((constants.WIDTH - (max_x - min_x)) / 2,
                constants.GAME_Y_OFFSET + (constants.HEIGHT - (max_y - min_y)) / 2)

    def draw(self, surface: pyg.Surface, scale: Scale):
        for cell in self.cells:
            cell.draw(surface, self.x_offset, self.y_offset, scale)

        for circle in self.circles:
            circle.draw(surface, scale)

        if self.temp_circle is not None:
            self.temp_circle.draw(surface, scale)
