from enum import Enum

import pygame as pyg

MUSICENDEVENT = pyg.constants.USEREVENT + 1

WIDTH = 1920
HEIGHT = 1080

GAME_Y_OFFSET = 0


class CellData:
    def __init__(self, main_texture: int, modifier_texture: int, can_be_selected: bool, points_multiplier: float):
        self.main_texture = main_texture  # Index into the CELL_TEXTURES animations list
        self.modifier_texture = modifier_texture  # Index into the MODIFIERS_TEXTURES animations list
        self.can_be_selected = can_be_selected
        self.points_multiplier = points_multiplier


CELL_DATA = [
    CellData(0, -1, True, 1.0),
    CellData(1, -1, False, 0.0),
    CellData(0, 0, True, 2.0)
]


class CellType(Enum):
    BASE = 0
    FORBIDDEN = 1
    MULT_2 = 2
