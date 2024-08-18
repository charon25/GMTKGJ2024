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

# Inputs
R_KEY = ord('r')
ENTER_KEY = ord('\r')
F12_KEY = 1073741893

LEFT_CLICK = 1
RIGHT_CLICK = 3

# Window
WIDTH = 1920
HEIGHT = 1080
GAME_RECT = pyg.Rect(0, 0, WIDTH, HEIGHT)

GAME_Y_OFFSET = 200

# Main menu
LOGO_SIZE = (1000, 400)
LOGO_POS = ((WIDTH - LOGO_SIZE[0]) / 2, 50)

PLAY_BTN_SIZE = (400, 400)
PLAY_BTN_POS = ((WIDTH - PLAY_BTN_SIZE[0]) / 2, 550)
PLAY_BTN_RECT = pyg.Rect(*PLAY_BTN_POS, *PLAY_BTN_SIZE)

# Options
OPTION_BTN_SIZE = 100
OPTION_BTN_X = WIDTH - OPTION_BTN_SIZE - 20
OPTION_TEXT_SIZE = 40
OPTION_TEXT_COLOR = (59, 59, 59)
OPTION_TEXT_BTN_GAP = 10

MUSIC_VOLUME_BTN_POS = (OPTION_BTN_X, 20)
MUSIC_VOLUME_BTN_RECT = pyg.Rect(*MUSIC_VOLUME_BTN_POS, OPTION_BTN_SIZE, OPTION_BTN_SIZE)
MUSIC_VOLUME_TEXT_RECT = pyg.Rect(MUSIC_VOLUME_BTN_POS[0] - OPTION_TEXT_BTN_GAP, MUSIC_VOLUME_BTN_POS[1], 0, OPTION_BTN_SIZE)

SFX_VOLUME_BTN_POS = (OPTION_BTN_X, MUSIC_VOLUME_BTN_POS[1] + 20 + OPTION_BTN_SIZE)
SFX_VOLUME_BTN_RECT = pyg.Rect(*SFX_VOLUME_BTN_POS, OPTION_BTN_SIZE, OPTION_BTN_SIZE)
SFX_VOLUME_TEXT_RECT = pyg.Rect(SFX_VOLUME_BTN_POS[0] - OPTION_TEXT_BTN_GAP, SFX_VOLUME_BTN_POS[1], 0, OPTION_BTN_SIZE)

HOLD_BTN_POS = (OPTION_BTN_X, SFX_VOLUME_BTN_POS[1] + 20 + OPTION_BTN_SIZE)
HOLD_BTN_RECT = pyg.Rect(*HOLD_BTN_POS, OPTION_BTN_SIZE, OPTION_BTN_SIZE)
HOLD_TEXT_RECT_1 = pyg.Rect(HOLD_BTN_POS[0] - OPTION_TEXT_BTN_GAP, HOLD_BTN_POS[1] + 10, 0, 40)
HOLD_TEXT_RECT_2 = pyg.Rect(HOLD_BTN_POS[0] - OPTION_TEXT_BTN_GAP, HOLD_BTN_POS[1] + 50, 0, 40)

# Levels
LEVEL_COUNT = 2

LEVEL_TITLE_RECT = pyg.Rect(0, 10, WIDTH, 120)

LEVEL_POINTS_COUNT_POS = (1000, 150)

RESTART_LEVEL_BTN_SIZE = 120
RESTART_LEVEL_BTN_POS = (20, 20)
RESTART_LEVEL_BTN_RECT = pyg.Rect(*RESTART_LEVEL_BTN_POS, RESTART_LEVEL_BTN_SIZE, RESTART_LEVEL_BTN_SIZE)

LEVEL_TUTORIAL_11_RECT = pyg.Rect(0, 965, WIDTH, 50)
LEVEL_TUTORIAL_12_RECT = pyg.Rect(0, 930, WIDTH, 50)
LEVEL_TUTORIAL_22_RECT = pyg.Rect(0, 1000, WIDTH, 50)

LEVEL_TUTORIALS: list[list[str]] = [
    ["Lorem ipsum dolor sit amet, consectetur adipiscing elit,", "sed do eiusmod tempor incididunt ut labore et dolore magna aliqua"],
    ["Excepteur sint occaecat cupidatat non proident, sunt in culpa"]
]

REMOVE_CIRCLE_TEXTURE_SIZE = 16

# End of level
EOL_BG_WIDTH = 700
EOL_BG_X = (WIDTH - EOL_BG_WIDTH) / 2
EOL_TITLE_WIDTH = 644
EOL_TITLE_HEIGHT = 285
EOL_TITLE_POS = (EOL_BG_X + (EOL_BG_WIDTH - 644) / 2, 100)

POINTS_TEXT_POS = (EOL_BG_X + 200, 420)
POINTS_TEXT_SIZE = (300, 65)

MEDAL_WIDTH = 130
MEDAL_HEIGHT = 200
MEDAL_GAP = 50
MEDAL_X = (EOL_BG_WIDTH - 3 * MEDAL_WIDTH - 2 * MEDAL_GAP) / 2
MEDAL_X_2 = (EOL_BG_WIDTH - 2 * MEDAL_WIDTH - MEDAL_GAP) / 2
MEDAL_Y = 530
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

MEDAL_TEXT_FONT_SIZE = 40
MEDAL_TEXT_Y = MEDAL_Y + MEDAL_HEIGHT + 20

EOL_RESTART_LEVEL_BTN_POS = (EOL_BG_X + MEDAL_X, MEDAL_TEXT_Y + MEDAL_TEXT_FONT_SIZE + 100)
EOL_RESTART_LEVEL_BTN_SIZE = 120
EOL_RESTART_LEVEL_BTN_RECT = pyg.Rect(*EOL_RESTART_LEVEL_BTN_POS, EOL_RESTART_LEVEL_BTN_SIZE, EOL_RESTART_LEVEL_BTN_SIZE)

NEXT_LEVEL_BTN_POS = (EOL_BG_X + MEDAL_X + 40 + EOL_RESTART_LEVEL_BTN_SIZE, MEDAL_TEXT_Y + MEDAL_TEXT_FONT_SIZE + 100)
NEXT_LEVEL_BTN_SIZE = (330, 120)
NEXT_LEVEL_BTN_RECT = pyg.Rect(*NEXT_LEVEL_BTN_POS, *NEXT_LEVEL_BTN_SIZE)

# End of game
EOG_TEXT1_RECT = pyg.Rect((WIDTH - 1000) / 2, LOGO_POS[1] + LOGO_SIZE[1], 1000, 100)
EOG_TEXT2_RECT = pyg.Rect((WIDTH - 750) / 2, EOG_TEXT1_RECT[1] + 100, 750, 140)
EOG_TEXT3_RECT = pyg.Rect((WIDTH - 750) / 2, EOG_TEXT2_RECT[1] + 100, 750, 160)

EOG_GOLD_MEDAL_POS = (530, 812)
EOG_GOLD_MEDAL_TEXT_SIZE = 60
EOG_GOLD_MEDAL_TEXT_POS = (EOG_GOLD_MEDAL_POS[0] + MEDAL_WIDTH + 10, EOG_GOLD_MEDAL_POS[1] + (MEDAL_HEIGHT - EOG_GOLD_MEDAL_TEXT_SIZE) / 2)

EOG_RESTART_BTN_SIZE = 200
EOG_RESTART_BTN_POS = (WIDTH - EOG_GOLD_MEDAL_POS[0] - EOG_RESTART_BTN_SIZE, EOG_GOLD_MEDAL_POS[1])
EOG_RESTART_BTN_RECT = pyg.Rect(*EOG_RESTART_BTN_POS, EOG_RESTART_BTN_SIZE, EOG_RESTART_BTN_SIZE)

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


TEXTURE_INDEX_FROM_SIZE: dict[int, int] = {
    16: 0,
    32: 1,
    64: 2,
    128: 3,
    256: 4
}
TEXTURE_SIZES = sorted(TEXTURE_INDEX_FROM_SIZE.keys())

POINTS_FROM_SIZE: dict[int, int] = {
    16: 2,
    32: 5,
    64: 10,
    128: 20,
    256: 40
}


# Screen shake
SCREEN_SHAKE_COUNT = 5
SCREEN_SHAKE_MAX_INTENSITY = 20
FREQUENCY = 2 * math.pi / SCREEN_SHAKE_COUNT

# Font
FONT_PATH = "resources/font/ldcBlackRound.ttf"
FONT_Y_OFFSET = 1 / 16
