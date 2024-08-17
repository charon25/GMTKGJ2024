from enum import Enum

import pygame as pyg

MUSICENDEVENT = pyg.constants.USEREVENT + 1

WIDTH = 1920
HEIGHT = 1080

GAME_Y_OFFSET = 0


class CellData:
    def __init__(self, can_be_selected: bool, points_multiplier: float):
        self.can_be_selected = can_be_selected
        self.points_multiplier = points_multiplier


CELL_DATA = [
    CellData(True, 1.0),
    CellData(False, 0.0),
    CellData(True, 2.0)
]


class CellType(Enum):
    BASE = 0
    FORBIDDEN = 1
    MULT_2 = 2
