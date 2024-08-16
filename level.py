import pygame as pyg

import constants
from cell import Cell
from circle import Circle
from constants import CellType
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
        self.temp_selected_cells: list[Cell] = list()

        self.points = 0

    def reset(self):
        self.temp_selected_cells = list()
        for cell in self.cells:
            cell.unselect()

        self.circles = list()
        self.temp_circle = None

        self.points = 0

    def set_temp_circle_position(self, x: int, y: int):
        if not any(cell.contains_point(x - self.x_offset, y - self.y_offset) for cell in self.cells):
            return

        self.temp_circle = Circle(x - self.x_offset, y - self.y_offset, 0)

    def validate_temp_circle(self):
        if self.temp_circle is None:
            return

        if self.temp_circle.radius < self.cell_size * 0.707:  # sqrt(2) / 2
            self.destroy_temp_circle()
            return

        points = 0
        multiplier = 1.0
        for cell in self.temp_selected_cells:
            cell.temp_selected = False
            cell.selected_count += 1

            points += cell.get_points()
            multiplier *= cell.cell_data.points_multiplier

        self.temp_selected_cells = []

        self.circles.append(self.temp_circle)
        self.temp_circle = None

        print(int(points * multiplier))
        self.points += int(points * multiplier)

    def destroy_temp_circle(self):
        if self.temp_circle is None:
            return

        for cell in self.temp_selected_cells:
            cell.temp_selected = False
        self.temp_selected_cells = []

        self.temp_circle = None

        # todo play sound

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

    def update(self):
        if self.temp_circle is None:
            return

        # todo voir la taille
        self.temp_circle.radius += 1

        for cell in self.cells:
            if self.temp_circle is None:
                break

            if not cell.is_full_selected() and not cell.temp_selected:
                if self.temp_circle.contains_rect(cell.rect):
                    self.__on_cell_in_temp_circle(cell)
                elif self.temp_circle.touch_rect(cell.rect):
                    self.__on_cell_touch_temp_circle(cell)

    def __on_cell_touch_temp_circle(self, cell: Cell):
        if cell.type == CellType.FORBIDDEN:
            self.destroy_temp_circle()

    def __on_cell_in_temp_circle(self, cell: Cell):
        if cell.cell_data.can_be_selected:
            cell.temp_selected = True
            self.temp_selected_cells.append(cell)

    def draw(self, surface: pyg.Surface, scale: Scale):
        for cell in self.cells:
            cell.draw(surface, self.x_offset, self.y_offset, scale)

        for circle in self.circles:
            circle.draw(surface, self.x_offset, self.y_offset, scale)

        if self.temp_circle is not None:
            self.temp_circle.draw(surface, self.x_offset, self.y_offset, scale)
