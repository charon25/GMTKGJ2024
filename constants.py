from enum import Enum

import pygame as pyg

MUSICENDEVENT = pyg.constants.USEREVENT + 1

WIDTH = 1920
HEIGHT = 1080

GAME_Y_OFFSET = 0


class CellData:
    def __init__(self, can_be_selected: bool, max_select_count: int, points_multiplier: float):
        self.can_be_selected = can_be_selected
        self.max_select_count = max_select_count
        self.points_multiplier = points_multiplier


CELL_DATA = [
    CellData(True, 1, 1.0),
    CellData(False, 1, 0.0)
]


class CellType(Enum):
    BASE = 0
    FORBIDDEN = 1
