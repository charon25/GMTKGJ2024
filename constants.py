import math
from enum import IntEnum

import pygame as pyg


class GameState(IntEnum):
    NONE = -9999
    BROWSER_WAIT_FOR_CLICK = -10
    PLAYING_LEVEL = 0
    END_OF_LEVEL = 10
    MAIN_MENU = 20


MUSICENDEVENT = pyg.constants.USEREVENT + 1

WIDTH = 1920
HEIGHT = 1080
GAME_RECT = pyg.Rect(0, 0, WIDTH, HEIGHT)

GAME_Y_OFFSET = 0


class CellData:
    def __init__(self, main_texture: int, modifier_texture: int, can_be_selected: bool = True,
                 points_multiplier: float = 1.0, bonus_circles: int = 0):
        self.main_texture = main_texture  # Index into the CELL_TEXTURES animations list
        self.modifier_texture = modifier_texture  # Index into the MODIFIERS_TEXTURES animations list
        self.can_be_selected = can_be_selected
        self.points_multiplier = points_multiplier if can_be_selected else 0.0
        self.bonus_circles = bonus_circles


# Needs to be in same order as enum below
CELL_DATA = [
    CellData(0, -1),
    CellData(1, -1, can_be_selected=False),
    CellData(0, 0, points_multiplier=2.0),
    CellData(0, 1, bonus_circles=1),
    CellData(2, 0, can_be_selected=False)
]


class CellType(IntEnum):
    BASE = 0
    FORBIDDEN = 1
    MULT_2 = 2
    CIRCLE_P1 = 3
    BLOCKER = 4


# Screen shake
SCREEN_SHAKE_COUNT = 5
SCREEN_SHAKE_MAX_INTENSITY = 20
FREQUENCY = 2 * math.pi / SCREEN_SHAKE_COUNT
