import math

import pygame as pyg

import constants
from cell import Cell
from circle import Circle
from constants import CellType
from window import Scale


class Level:
    def __init__(self, number: int, cell_size: int, max_circles_count: int, cells: list[Cell]):
        self.number = number
        self.cell_size = cell_size
        self.cells = cells
        for cell in self.cells:
            cell.generate(cell_size)

        self.x_offset, self.y_offset, self.width, self.height = self.__get_limits()

        self.circles: list[ValidatedCircle] = list()
        self.temp_circle: Circle | None = None
        self.temp_selected_cells: list[Cell] = list()
        self.circumscribed_circle: Circle = Circle(self.width // 2, self.height // 2, 0)

        self.max_circles_count = max_circles_count
        self.max_circles_count_upgrade = 0
        self.current_circles_count = 0

        self.points = 0

        self.screen_shake = 0

    def __get_limits(self) -> tuple[int, int, int, int]:
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
                constants.GAME_Y_OFFSET + (constants.HEIGHT - (max_y - min_y)) / 2,
                (max_x - min_x), (max_y - min_y))

    def reset(self):
        self.temp_selected_cells = list()
        for cell in self.cells:
            cell.unselect()

        self.circles = list()
        self.temp_circle = None
        self.circumscribed_circle = Circle(self.width // 2, self.height // 2, 0)

        self.max_circles_count_upgrade = 0
        self.current_circles_count = 0

        self.points = 0

    # region ===== CERCLE =====

    def click_on_level(self, x: int, y: int):
        x = x - self.x_offset
        y = y - self.y_offset

        for v_circle in self.circles:
            if v_circle.circle.contains_point(x, y):
                self.remove_circle(v_circle)
                return

        if self.current_circles_count >= self.max_circles_count + self.max_circles_count_upgrade:
            return

        if not any(cell.contains_point(x, y) for cell in self.cells):
            return

        self.temp_circle = Circle(x, y, 0)

    def validate_temp_circle(self):
        if self.temp_circle is None:
            return

        if self.temp_circle.radius < self.cell_size * 0.707:  # sqrt(2) / 2
            self.destroy_temp_circle()
            return

        points = 0
        multiplier = 1.0
        for cell in self.temp_selected_cells:
            cell.selected = True
            cell.temp_selected = False

            points += cell.get_points()
            multiplier *= cell.cell_data.points_multiplier

            self.max_circles_count_upgrade += cell.cell_data.bonus_circles

        earned_points = int(points * multiplier)

        self.circles.append(ValidatedCircle(self.temp_circle, self.temp_selected_cells, earned_points))

        max_dist = math.dist((self.width / 2, self.height / 2), (self.temp_circle.x, self.temp_circle.y)) + self.temp_circle.radius
        self.circumscribed_circle.radius = max(self.circumscribed_circle.radius, max_dist)
        self.temp_selected_cells = []
        self.temp_circle = None

        self.points += earned_points
        self.current_circles_count += 1

        self.screen_shake = earned_points

    def destroy_temp_circle(self):
        if self.temp_circle is None:
            return

        for cell in self.temp_selected_cells:
            cell.temp_selected = False
        self.temp_selected_cells = []

        self.temp_circle = None

        # todo play sound

    def remove_circle(self, v_circle: 'ValidatedCircle'):
        self.circles.remove(v_circle)

        for cell in v_circle.contained_cells:
            cell.selected = False
            cell.temp_selected = False

            self.max_circles_count_upgrade -= cell.cell_data.bonus_circles

        self.points -= v_circle.points
        self.current_circles_count -= 1

        # todo play sound

    # endregion

    # region ===== UPDATE =====

    def on_mouse_move(self, x: int, y: int):
        x = x - self.x_offset
        y = y - self.y_offset

        if not self.circumscribed_circle.contains_point(x, y):
            return

        for v_circle in self.circles:
            v_circle.circle.is_hovered = v_circle.circle.contains_point(x, y)

    def update(self, dt: float):
        if self.temp_circle is None:
            return

        # todo voir la taille
        self.temp_circle.radius += 1 * (dt * 60)

        for cell in self.cells:
            if self.temp_circle is None:
                break

            if not cell.selected and not cell.temp_selected:
                if self.temp_circle.contains_rect(cell.rect):
                    self.__on_cell_in_temp_circle(cell)
                elif self.temp_circle.touch_rect(cell.rect):
                    self.__on_cell_touch_temp_circle(cell)

        for v_circle in self.circles:
            if self.temp_circle is None:
                break

            if self.temp_circle.touch_circle(v_circle.circle):
                self.validate_temp_circle()
                break

    def __on_cell_touch_temp_circle(self, cell: Cell):
        if cell.type == CellType.FORBIDDEN:
            self.destroy_temp_circle()
        elif cell.type == CellType.BLOCKER:
            self.validate_temp_circle()

    def __on_cell_in_temp_circle(self, cell: Cell):
        if cell.cell_data.can_be_selected:
            cell.temp_selected = True
            self.temp_selected_cells.append(cell)

    def draw(self, surface: pyg.Surface, scale: Scale):
        for cell in self.cells:
            cell.draw(surface, self.x_offset, self.y_offset, scale)

        for v_circle in self.circles:
            v_circle.circle.draw(surface, self.x_offset, self.y_offset, scale)

        if self.temp_circle is not None:
            self.temp_circle.draw(surface, self.x_offset, self.y_offset, scale)

    # endregion


class ValidatedCircle:
    def __init__(self, circle: Circle, contained_cells: list[Cell], points: int):
        self.circle = circle
        self.contained_cells = contained_cells
        self.points = points
