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
        set_main_params(level_data, 16, 1, [2, 192])
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

    elif number == 6:
        set_main_params(level_data, 64, 1, 300)
        level_data.cells = [
            Cell(1, 0), Cell(7, 0),
            Cell(0, 1), Cell(1, 1, _type=CellType.CIRCLE_1), Cell(2, 1), Cell(4, 1, _type=CellType.FORBIDDEN),
            Cell(6, 1),
            Cell(7, 1, _type=CellType.MULT_5), Cell(8, 1),
            Cell(1, 2), Cell(7, 2),
        ]

    elif number == 7:
        set_main_params(level_data, 64, 1, [60, 70])
        level_data.cells = [
            Cell(2, 0), Cell(3, 0),
            Cell(0, 2), Cell(2, 2, 2, _type=CellType.FORBIDDEN), Cell(5, 2),
            Cell(0, 3), Cell(5, 3),
            Cell(2, 5), Cell(3, 5, _type=CellType.CIRCLE_2),
        ]

    elif number == 8:
        set_main_params(level_data, 64, 1, [1000, 1300, 1400])
        level_data.cells = [
            Cell(1, 0), Cell(2, 0), Cell(3, 0), Cell(4, 0), Cell(5, 0, _type=CellType.MULT_2),
            Cell(1, 1, _type=CellType.MULT_5), Cell(2, 1), Cell(3, 1), Cell(4, 1), Cell(5, 1),
            Cell(1, 2), Cell(2, 2), Cell(3, 2, 2, CellType.MULT_0), Cell(5, 2),
            Cell(1, 3), Cell(2, 3), Cell(5, 3),
            Cell(1, 4), Cell(2, 4), Cell(3, 4), Cell(4, 4), Cell(5, 4),
            Cell(0, 5, _type=CellType.BLOCKER),
        ]

    elif number == 9:
        set_main_params(level_data, 64, 2, [40, 50, 90])
        level_data.cells = [
            Cell(2, 0, _type=CellType.MULT_2),
            Cell(1, 1, _type=CellType.FORBIDDEN), Cell(2, 1, _type=CellType.FORBIDDEN),
            Cell(3, 1, _type=CellType.FORBIDDEN),
            Cell(2, 2),
            Cell(0, 3, _type=CellType.FORBIDDEN), Cell(2, 3, _type=CellType.PACIFIER),
            Cell(4, 3, _type=CellType.FORBIDDEN),
            Cell(2, 5, _type=CellType.FORBIDDEN),
        ]

    elif number == 10:
        set_main_params(level_data, 32, 1, [580, 600, 720])
        level_data.cells = [
            Cell(0, 0), Cell(1, 0), Cell(14, 0), Cell(15, 0),
            Cell(0, 1), Cell(1, 1), Cell(14, 1), Cell(15, 1),
            Cell(0, 2, 2, CellType.PACIFIER), Cell(14, 2, 2),
            Cell(0, 4, 2, CellType.MULT_2), Cell(14, 4, 2, CellType.MULT_5),
            Cell(0, 6, 2), Cell(14, 6, 2),
            Cell(0, 8), Cell(1, 8), Cell(14, 8), Cell(15, 8),
            Cell(0, 9), Cell(1, 9), Cell(14, 9), Cell(15, 9),
            Cell(2, 9), Cell(3, 9), Cell(4, 9), Cell(5, 9), Cell(6, 9), Cell(7, 9), Cell(8, 9), Cell(9, 9),
            Cell(10, 9), Cell(11, 9), Cell(12, 9), Cell(13, 9),
            Cell(2, 10, 2, _type=CellType.FORBIDDEN), Cell(12, 10, 2, _type=CellType.FORBIDDEN),
            Cell(2, 12, 2, _type=CellType.FORBIDDEN), Cell(12, 12, 2, _type=CellType.FORBIDDEN),
            Cell(2, 14, 2, _type=CellType.FORBIDDEN_CIRCLE_2), Cell(12, 14, 2, _type=CellType.FORBIDDEN),
            Cell(6, 12, 4, CellType.CIRCLE_2),
        ]

    elif number == 11:
        set_main_params(level_data, 64, 2, [450, 460, 520])
        level_data.cells = [
            Cell(1, 0, _type=CellType.FORBIDDEN), Cell(4, 0, _type=CellType.FORBIDDEN), Cell(5, 0, _type=CellType.FORBIDDEN), Cell(9, 0), Cell(10, 0), Cell(11, 0),
            Cell(0, 1, _type=CellType.FORBIDDEN), Cell(1, 1, _type=CellType.PACIFIER), Cell(2, 1, _type=CellType.FORBIDDEN), Cell(3, 1, _type=CellType.FORBIDDEN), Cell(4, 1, _type=CellType.FORBIDDEN), Cell(5, 1, _type=CellType.FORBIDDEN), Cell(7, 1, _type=CellType.BLOCKER), Cell(9, 1), Cell(10, 1, _type=CellType.MULT_5), Cell(11, 1),
            Cell(1, 2, _type=CellType.FORBIDDEN), Cell(4, 2, _type=CellType.FORBIDDEN), Cell(5, 2, _type=CellType.FORBIDDEN), Cell(9, 2), Cell(10, 2), Cell(11, 2),
        ]

    elif number == 12:
        set_main_params(level_data, 16, 2, [63, 72])
        level_data.cells = [
            Cell(10, 0, _type=CellType.FORBIDDEN), Cell(11, 0, _type=CellType.FORBIDDEN), Cell(12, 0, _type=CellType.FORBIDDEN),
            Cell(3, 1, 4, _type=CellType.FORBIDDEN), Cell(7, 1, 4, CellType.MULT_2), Cell(12, 1, 4, CellType.PACIFIER), Cell(16, 1, 4, _type=CellType.FORBIDDEN),
            Cell(0, 4, _type=CellType.FORBIDDEN), Cell(1, 4, _type=CellType.FORBIDDEN), Cell(2, 4, _type=CellType.FORBIDDEN),
            Cell(0, 5, _type=CellType.FORBIDDEN), Cell(5, 5, _type=CellType.FORBIDDEN), Cell(10, 5, _type=CellType.FORBIDDEN), Cell(11, 5, _type=CellType.FORBIDDEN), Cell(12, 5, _type=CellType.FORBIDDEN), Cell(19, 5, _type=CellType.FORBIDDEN),
            Cell(0, 6, _type=CellType.FORBIDDEN), Cell(5, 6, _type=CellType.FORBIDDEN), Cell(19, 6, _type=CellType.FORBIDDEN),
            Cell(0, 7, _type=CellType.FORBIDDEN), Cell(5, 7, _type=CellType.FORBIDDEN), Cell(6, 7, _type=CellType.FORBIDDEN), Cell(7, 7, _type=CellType.FORBIDDEN), Cell(19, 7, 4, CellType.CIRCLE_2),
            Cell(0, 8, _type=CellType.FORBIDDEN), Cell(7, 8, _type=CellType.FORBIDDEN),
            Cell(0, 9, 4, _type=CellType.FORBIDDEN), Cell(5, 9, _type=CellType.FORBIDDEN), Cell(7, 9, 4, _type=CellType.FORBIDDEN),
            Cell(5, 10, _type=CellType.FORBIDDEN),
            Cell(5, 11, _type=CellType.FORBIDDEN),
            Cell(5, 12, _type=CellType.FORBIDDEN),
        ]

    elif number == 13:
        set_main_params(level_data, 64, 7, [250, 24000, 24240])
        level_data.cells = [
            Cell(0, 0, _type=CellType.MULT_5), Cell(6, 0, _type=CellType.MULT_5), Cell(12, 0, _type=CellType.MULT_5),
            Cell(0, 1, 4), Cell(6, 1, 4), Cell(12, 1, 4),
            Cell(19, 3, _type=CellType.MULT_2), Cell(20, 3), Cell(21, 3), Cell(22, 3), Cell(23, 3), Cell(24, 3, _type=CellType.MULT_5),
            Cell(19, 4), Cell(20, 4, 4), Cell(24, 4),
            Cell(19, 5), Cell(24, 5),
            Cell(19, 6), Cell(24, 6),
            Cell(0, 7, 4), Cell(6, 7, 4), Cell(12, 7, 4), Cell(19, 7), Cell(24, 7),
            Cell(19, 8, _type=CellType.MULT_5), Cell(20, 8), Cell(21, 8), Cell(22, 8), Cell(23, 8), Cell(24, 8, _type=CellType.MULT_2),
            Cell(0, 11, _type=CellType.MULT_5), Cell(6, 11, _type=CellType.MULT_5), Cell(12, 11, _type=CellType.MULT_5),
        ]

    elif number == 14:
        set_main_params(level_data, 64, 1, 3_200_000)
        level_data.cells = [
            Cell(0, 0, _type=CellType.MULT_2), Cell(1, 0), Cell(2, 0), Cell(3, 0, _type=CellType.MULT_5), Cell(4, 0, _type=CellType.MULT_5), Cell(5, 0), Cell(6, 0), Cell(7, 0, _type=CellType.MULT_2),
            Cell(0, 1), Cell(1, 1), Cell(2, 1), Cell(3, 1), Cell(4, 1), Cell(5, 1), Cell(6, 1), Cell(7, 1),
            Cell(0, 2), Cell(1, 2), Cell(2, 2), Cell(3, 2), Cell(4, 2), Cell(5, 2), Cell(6, 2), Cell(7, 2),
            Cell(0, 3, _type=CellType.MULT_5), Cell(1, 3), Cell(2, 3), Cell(3, 3, _type=CellType.MULT_2), Cell(4, 3, _type=CellType.MULT_2), Cell(5, 3), Cell(6, 3), Cell(7, 3, _type=CellType.MULT_5),
        ]

    return level_data
