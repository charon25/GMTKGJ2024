import math
import random

import pygame as pyg

import constants as co
from cell import Cell
from circle import Circle
from constants import CellType
from window import Scale


class LevelManager:
    INSTANCE = None

    def __init__(self):
        self.number = -1
        self.current_level: Level = None
        self.in_loading_anim = False
        self.current_level_ended = False
        self.all_level_complete = False

        self.gold_medals: dict[int, bool] = dict()

    @classmethod
    def instance(cls) -> 'LevelManager':
        if cls.INSTANCE is None:
            cls.INSTANCE = LevelManager()
        return cls.INSTANCE

    @classmethod
    def reset(cls):
        cls.INSTANCE = LevelManager()

    def load_next_level(self):
        self.load_level(self.number + 1)

    def reload_current_level(self):
        # if self.current_level.is_finished():
        #     self.total_gold_medals -= 1
        #     self.obtained_gold_medals -= self.current_level.got_gold_medal()
        self.load_level(self.number)

    def __get_level(self):
        if self.number == 0:
            return Level(1, 32, 3, [1, 3, 100], [Cell(x, 0, 1, 1) for x in range(8)]
                         + [Cell(0, 1, 2, 1)] + [Cell(0, 4, 1, 1, co.CellType.FORBIDDEN)]
                         + [Cell(5, 2, 1, 1, co.CellType.CIRCLE_P1)]
                         + [Cell(0, -4, 1, 1, co.CellType.BLOCKER)]
                         + [Cell(3, 1, 1, 1, co.CellType.MULT_2)])
        else:
            return Level(1, 32, 3, [4],
                                       [Cell(1, 0), Cell(0, 1), Cell(2, 1), Cell(1, 2)])

    def load_level(self, number: int):
        self.number = number
        self.current_level = self.__get_level()

        self.current_level_ended = False
        self.current_level.start_loading_animation()
        self.in_loading_anim = True

    def on_level_loaded(self):
        self.in_loading_anim = False

    def on_level_unloaded(self):
        self.current_level_ended = True
        self.gold_medals[self.number] = self.current_level.got_gold_medal()

    def are_all_level_complete(self):
        return self.number == co.LEVEL_COUNT - 1 and self.current_level_ended


class Level:
    def __init__(self, number: int, cell_size: int, max_circles_count: int,
                 required_points: list[int],
                 cells: list[Cell]):
        self.number = number
        self.cell_size = cell_size
        self.cells = sorted(cells)

        self.x_offset, self.y_offset, self.width, self.height = 0, 0, 0, 0
        self.__compute_terrain()

        self.circles: list[ValidatedCircle] = list()
        self.temp_circle: Circle | None = None
        self.temp_selected_cells: list[Cell] = list()
        self.temp_multiplier: float = 1.0
        self.circumscribed_circle: Circle = Circle(self.width // 2, self.height // 2, 0)

        self.max_circles_count = max_circles_count
        self.max_circles_count_upgrade = 0
        self.current_circles_count = 0

        self.required_points = sorted(required_points)
        self.points: float = 0.0
        self.cells_in_animation = 0

        self.animation = 0  # 0 : pas d'anim, 1 : loading, -1 : unloading

    def __compute_terrain(self):
        min_x: int = co.WIDTH
        max_x: int = 0
        min_y: int = co.HEIGHT
        max_y: int = 0
        x_center, y_center = 0, 0
        for k, cell in enumerate(self.cells):
            cell.generate(self.cell_size, k, self.on_cell_selected)
            min_x = min(min_x, cell.rect.left)
            max_x = max(max_x, cell.rect.right)
            min_y = min(min_y, cell.rect.top)
            max_y = max(max_y, cell.rect.bottom)
            x_center += cell.rect.centerx
            y_center += cell.rect.centery

        self.x_offset = (co.WIDTH - (max_x - min_x)) / 2 - min_x
        self.y_offset = co.GAME_Y_OFFSET + (co.HEIGHT - (max_y - min_y)) / 2 - min_y
        self.width = max_x - min_x
        self.height = max_y - min_y

        x_center = x_center / len(self.cells)
        y_center = y_center / len(self.cells)

        for cell in self.cells:
            mag = math.dist(cell.rect.center, (x_center, y_center))
            cell.vector = ((cell.rect.centerx - x_center) / mag, (cell.rect.centery - y_center) / mag)

    def reset(self):
        self.temp_selected_cells = list()
        for cell in self.cells:
            cell.unselect()

        self.circles = list()
        self.temp_circle = None
        self.temp_multiplier = 1.0
        self.circumscribed_circle = Circle(self.width // 2, self.height // 2, 0)

        self.max_circles_count_upgrade = 0
        self.current_circles_count = 0

        self.points = 0.0

        self.cells_in_animation = 0

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
        self.temp_multiplier = 1.0

    def validate_temp_circle(self):
        if self.temp_circle is None:
            return

        if self.temp_circle.radius < self.cell_size * 0.707:  # sqrt(2) / 2
            self.destroy_temp_circle()
            return

        self.temp_selected_cells = sorted(self.temp_selected_cells)

        self.cells_in_animation = len(self.temp_selected_cells)

        points = 0
        for k, cell in enumerate(self.temp_selected_cells):
            cell.select(k)
            cell.points += cell.get_points() * self.temp_multiplier

            points += cell.get_points()

        self.circles.append(ValidatedCircle(self.temp_circle, self.temp_selected_cells, points * self.temp_multiplier))

        max_dist = math.dist((self.width / 2, self.height / 2),
                             (self.temp_circle.x, self.temp_circle.y)) + self.temp_circle.radius
        self.circumscribed_circle.radius = max(self.circumscribed_circle.radius, max_dist)
        self.temp_selected_cells = []
        self.temp_circle = None
        self.temp_multiplier = 1.0

        self.current_circles_count += 1

    def destroy_temp_circle(self):
        if self.temp_circle is None:
            return

        for cell in self.temp_selected_cells:
            cell.temp_selected = False
        self.temp_selected_cells = []

        self.temp_circle = None
        self.temp_multiplier = 1.0

        # todo play sound

    def remove_circle(self, v_circle: 'ValidatedCircle'):
        self.circles.remove(v_circle)

        for k, cell in enumerate(v_circle.contained_cells):
            if cell.animation is None:
                self.points -= cell.points
            cell.unselect(k)

            self.max_circles_count_upgrade -= cell.cell_data.bonus_circles

        self.current_circles_count -= 1

        # todo play sound

    # endregion

    # region ===== UPDATE =====

    def on_cell_selected(self, cell: Cell):
        self.points += cell.points
        self.max_circles_count_upgrade += cell.cell_data.bonus_circles
        self.cells_in_animation -= 1

    def on_mouse_move(self, x: int, y: int):
        x = x - self.x_offset
        y = y - self.y_offset

        if not self.circumscribed_circle.contains_point(x, y):
            return

        for v_circle in self.circles:
            v_circle.circle.is_hovered = v_circle.circle.contains_point(x, y)

    def update(self, dt: float):
        if self.is_finished():
            self.start_unloading_animation()

        self.update_temp_circle(dt)

    def update_temp_circle(self, dt: float):
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
            self.temp_multiplier *= cell.cell_data.points_multiplier

    def is_finished(self):
        return self.animation == 0 and self.cells_in_animation == 0 and self.points >= self.required_points[0]

    def draw(self, surface: pyg.Surface, scale: Scale, dt: float):
        if self.animation == 0:
            self.draw_level(surface, scale, dt)
        elif self.animation == 1:
            self.draw_loading_animation(surface, scale, dt)
        elif self.animation == -1:
            self.draw_unloading_animation(surface, scale, dt)

    def draw_level(self, surface: pyg.Surface, scale: Scale, dt: float):
        for cell in self.cells:
            cell.draw(surface, self.x_offset, self.y_offset, scale, dt)

        for v_circle in self.circles:
            v_circle.circle.draw(surface, self.x_offset, self.y_offset, scale)

        if self.temp_circle is not None:
            self.temp_circle.draw(surface, self.x_offset, self.y_offset, scale)

    # endregion

    # region ===== ANIMATIONS =====

    def start_loading_animation(self):
        for cell in self.cells:
            dir_x, dir_y = (cell.vector[0] + random.random() / 10, cell.vector[1] + random.random() / 10)
            x = cell.rect.x + dir_x * (co.WIDTH / 2 + 150)
            y = cell.rect.y + dir_y * (co.WIDTH / 2 + 150)
            cell.set_temp_rect(self.cell_size, x, y)
            speed = random.random() * 10 + 40
            cell.velocity = (-speed * dir_x, -speed * dir_y)
        self.animation = 1

    def draw_loading_animation(self, surface: pyg.Surface, scale: Scale, dt: float):
        placed_cells_count = 0
        for cell in self.cells:
            if cell.temp_rect is None:
                continue

            cell.draw(surface, self.x_offset, self.y_offset, scale, dt)
            if cell.is_in_place():
                cell.temp_rect = cell.rect
                placed_cells_count += 1
            else:
                cell.temp_rect.x += cell.velocity[0] * dt * 60
                cell.temp_rect.y += cell.velocity[1] * dt * 60

        if placed_cells_count == len(self.cells):
            LevelManager.instance().on_level_loaded()
            self.animation = 0

    def start_unloading_animation(self):
        for cell in self.cells:
            dir_x, dir_y = (cell.vector[0] + random.random() / 10, cell.vector[1] + random.random() / 10)
            cell.set_temp_rect(self.cell_size, cell.rect.x, cell.rect.y)
            speed = random.random() * 10 + 40
            cell.velocity = (speed * dir_x, speed * dir_y)
        self.animation = -1

    def draw_unloading_animation(self, surface: pyg.Surface, scale: Scale, dt: float):
        removed_cells_count = 0
        for cell in self.cells:
            if cell.temp_rect is None:
                continue

            cell.draw(surface, self.x_offset, self.y_offset, scale, dt)
            if cell.is_outside_screen(self.x_offset, self.y_offset):
                cell.displayed = False
                removed_cells_count += 1
            else:
                cell.temp_rect.x += cell.velocity[0] * dt * 60
                cell.temp_rect.y += cell.velocity[1] * dt * 60

        if removed_cells_count == len(self.cells):
            LevelManager.instance().on_level_unloaded()

    # endregion

    # region ===== OTHER =====

    def get_medals(self) -> list[int]:
        if len(self.required_points) == 1:
            return [1]
        if len(self.required_points) == 2:
            return [2, 1 if self.points >= self.required_points[1] else 0]
        if len(self.required_points) == 3:
            return [3, 2 if self.points >= self.required_points[1] else 0, 1 if self.points >= self.required_points[2] else 0]

    def got_gold_medal(self):
        return self.points >= self.required_points[-1]

    # endregion


class ValidatedCircle:
    def __init__(self, circle: Circle, contained_cells: list[Cell], points: float):
        self.circle = circle
        self.contained_cells = contained_cells
        self.points = points
