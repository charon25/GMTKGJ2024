from enum import Enum

import pygame as pyg

MUSICENDEVENT = pyg.constants.USEREVENT + 1

WIDTH = 1920
HEIGHT = 1080

GAME_Y_OFFSET = 0

class CellType(Enum):
    BASE = 0
    FORBIDDEN = 1
