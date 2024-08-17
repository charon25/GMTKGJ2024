import math
from enum import IntEnum

import pygame as pyg


class GameState(IntEnum):
    NONE = -9999
    BROWSER_WAIT_FOR_CLICK = -10
    PLAYING_LEVEL = 0
    END_OF_LEVEL = 10
    MAIN_MENU = 20
    END_OF_GAME = 30


MUSICENDEVENT = pyg.constants.USEREVENT + 1

# Window
WIDTH = 1920
HEIGHT = 1080
GAME_RECT = pyg.Rect(0, 0, WIDTH, HEIGHT)

GAME_Y_OFFSET = 0

# Levels
LEVEL_COUNT = 2

# End of level
EOL_BG_WIDTH = 700
EOL_BG_X = (WIDTH - EOL_BG_WIDTH) / 2
EOL_TITLE_WIDTH = 644
EOL_TITLE_POS = (EOL_BG_X + (EOL_BG_WIDTH - 644) / 2, 100)

MEDAL_WIDTH = 130
MEDAL_GAP = 50
MEDAL_X = (EOL_BG_WIDTH - 3 * MEDAL_WIDTH - 2 * MEDAL_GAP) / 2
MEDAL_X_2 = (EOL_BG_WIDTH - 2 * MEDAL_WIDTH - MEDAL_GAP) / 2
MEDAL_Y = 450
MEDAL_POS = [
    [
        (EOL_BG_X + MEDAL_X + MEDAL_WIDTH + MEDAL_GAP, MEDAL_Y)
    ],
    [
        (EOL_BG_X + MEDAL_X_2, MEDAL_Y),
        (EOL_BG_X + MEDAL_X_2 + MEDAL_WIDTH + MEDAL_GAP, MEDAL_Y)
    ],
    [
        (EOL_BG_X + MEDAL_X, MEDAL_Y),
        (EOL_BG_X + MEDAL_X + MEDAL_WIDTH + MEDAL_GAP, MEDAL_Y),
        (EOL_BG_X + MEDAL_X + 2 * (MEDAL_WIDTH + MEDAL_GAP), MEDAL_Y)
    ]
]


# Cells
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

# Font
FONT_PATH = "resources/font/betterpixels.ttf"
