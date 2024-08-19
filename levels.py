from cell import Cell
from constants import CellType


class LevelData:
    def __init__(self):
        self.number = -1
        self.cell_size = -1
        self.max_circle_count = -1
        self.required_points: list[int] = list()
        self.cells: list[Cell] = list()


def set_main_params(level_data: LevelData, cell_size: int, max_circle_count: int, required_points: int | list[int]):
    level_data.cell_size = cell_size
    level_data.max_circle_count = max_circle_count
    level_data.required_points = required_points if isinstance(required_points, list) else [required_points]


def get_level(number: int) -> LevelData:
    level_data = LevelData()
    level_data.number = number
    if number == 0:  # Niveau 1
        set_main_params(level_data, 64, 1, 10)
        level_data.cells = [
            Cell(0, 0)
        ]

    elif number == 1:
        set_main_params(level_data, 64, 1, 50)
        level_data.cells = [
            Cell(1, 0),
            Cell(0, 1), Cell(1, 1), Cell(2, 1),
            Cell(1, 2),
        ]

    elif number == 2:
        set_main_params(level_data, 64, 2, 20)
        level_data.cells = [
            Cell(0, 0), Cell(2, 0, _type=CellType.FORBIDDEN), Cell(4, 0),
        ]

    elif number == 3:
        set_main_params(level_data, 64, 2, 20)
        level_data.cells = [
            Cell(0, 0),
            Cell(0, 2, _type=CellType.BLOCKER),
            Cell(0, 4),
        ]

    elif number == 4:
        set_main_params(level_data, 16, 1, 192)
        level_data.cells = [
            Cell(0, 0, 16),
            Cell(16, 0, 8), Cell(16, 8, 8),
            Cell(24, 0, 4), Cell(24, 4, 4), Cell(24, 8, 4), Cell(24, 12, 4),
            Cell(28, 0, 2), Cell(28, 2, 2), Cell(28, 4, 2), Cell(28, 6, 2),
            Cell(28, 8, 2), Cell(28, 10, 2), Cell(28, 12, 2), Cell(28, 14, 2),
            Cell(30, 0), Cell(30, 1), Cell(30, 2), Cell(30, 3),
            Cell(30, 4), Cell(30, 5), Cell(30, 6), Cell(30, 7),
            Cell(30, 8), Cell(30, 9), Cell(30, 10), Cell(30, 11),
            Cell(30, 12), Cell(30, 13), Cell(30, 14), Cell(30, 15)
        ]
        pass

    elif number == 5:
        set_main_params(level_data, 64, 1, [60, 80])
        level_data.cells = [
            Cell(0, 0), Cell(1, 0), Cell(5, 0),
            Cell(0, 1), Cell(1, 1), Cell(3, 1, _type=CellType.FORBIDDEN), Cell(5, 1, _type=CellType.MULT_2), Cell(6, 1),
            Cell(0, 2), Cell(1, 2), Cell(5, 2),
        ]

    return level_data
