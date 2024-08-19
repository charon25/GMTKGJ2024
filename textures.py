import pygame as pyg
from pygame.image import load
from pygame.transform import scale_by

import constants
from animation_manager import Animation, AnimationManager
from images import Image
from window import Scale

CELL_TEXTURES: list[list[list[Animation]]] = list()
MODIFIERS_TEXTURES: list[list[Animation]] = list()
CELL_ANIMATOR = AnimationManager()

BACKGROUND = load("resources/textures/background.png")

LOGO = load("resources/textures/main_menu/logo.png")
PLAY_BUTTON = load("resources/textures/main_menu/play_btn.png")

VOLUMES: list[pyg.Surface] = [
    load("resources/textures/sounds/0.png"),
    load("resources/textures/sounds/1.png"),
    load("resources/textures/sounds/2.png"),
    load("resources/textures/sounds/3.png")
]

CHECKBOXES: list[pyg.Surface] = [
    load("resources/textures/checkbox_0.png"),
    load("resources/textures/checkbox_1.png")
]

END_OF_LEVEL_BACKGROUND = load("resources/textures/eol/end_of_level_bg.png")
END_OF_LEVEL_TITLE = load("resources/textures/eol/end_of_level_title.png")
MEDALS: list[pyg.Surface] = [
    load("resources/textures/eol/empty_medal.png"),
    load("resources/textures/eol/gold_medal.png"),
    load("resources/textures/eol/silver_medal.png"),
    load("resources/textures/eol/bronze_medal.png")
]
RESTART_LEVEL_BUTTON = load("resources/textures/eol/eol_restart_level_btn.png")
NEXT_LEVEL_BUTTON = load("resources/textures/eol/eol_next_level_btn.png")
RESTART_GAME_BUTTON = load("resources/textures/restart_btn.png")
REMOVE_CIRCLE = load("resources/textures/remove_circle.png")
GMTK_LOGO = load("resources/textures/gmtk-logo.png")
CIRCLE = load("resources/textures/circle.png")
PREVIOUS_LEVEL_BUTTON = load("resources/textures/prev_level_btn.png")
BG_CELL = load("resources/textures/cells/bg_cell.png")
CURSOR = load("resources/textures/cursor.png")


def load_scale(filename: str, scale: Scale) -> pyg.Surface:
    if scale.scale == 1:
        return load(filename)
    return scale_by(load(filename), scale.scale)


def scale_list(textures: list[pyg.Surface], scale: Scale) -> list[pyg.Surface]:
    return [scale_by(texture, scale.scale) for texture in textures]


def load_all(scale: Scale):
    _load_textures(scale)
    _load_cell_animations(scale)
    _load_modifiers_animations(scale)


def _load_textures(scale: Scale):
    global END_OF_LEVEL_BACKGROUND, END_OF_LEVEL_TITLE, MEDALS, NEXT_LEVEL_BUTTON, LOGO, PLAY_BUTTON, VOLUMES, CHECKBOXES
    global RESTART_GAME_BUTTON, RESTART_LEVEL_BUTTON, BACKGROUND, GMTK_LOGO, CIRCLE, PREVIOUS_LEVEL_BUTTON, BG_CELL

    if abs(1 - scale.scale) <= 0.03:
        return

    BACKGROUND = scale_by(BACKGROUND, scale.scale)
    LOGO = scale_by(LOGO, scale.scale)

    END_OF_LEVEL_BACKGROUND = scale_by(END_OF_LEVEL_BACKGROUND, scale.scale)
    END_OF_LEVEL_TITLE = scale_by(END_OF_LEVEL_TITLE, scale.scale)
    MEDALS = scale_list(MEDALS, scale)
    RESTART_LEVEL_BUTTON = scale_by(RESTART_LEVEL_BUTTON, scale.scale)
    NEXT_LEVEL_BUTTON = scale_by(NEXT_LEVEL_BUTTON, scale.scale)
    RESTART_GAME_BUTTON = scale_by(RESTART_GAME_BUTTON, scale.scale)

    PLAY_BUTTON = scale_by(PLAY_BUTTON, scale.scale)
    VOLUMES = scale_list(VOLUMES, scale)
    CHECKBOXES = scale_list(CHECKBOXES, scale)
    GMTK_LOGO = scale_by(GMTK_LOGO, scale.scale)
    CIRCLE = scale_by(CIRCLE, scale.scale)
    PREVIOUS_LEVEL_BUTTON = scale_by(PREVIOUS_LEVEL_BUTTON, scale.scale)
    BG_CELL = scale_by(BG_CELL, scale.scale)


def _get_animation(filename: str, width: int, height: int, total_duration: float, scale: Scale) -> Animation:
    textures = Image.slice_horizontally_then_vertically(filename, width, height)
    count = len(textures)
    return Animation(
        [scale_by(texture, scale.scale) for texture in textures],
        [total_duration / count] * count
    )


def _get_all_animations(filename: str, total_duration: float, scale: Scale) -> list[Animation]:
    return [
        _get_animation(f"{filename}/{size}.png", size, size, total_duration, scale)
        for size in constants.TEXTURE_SIZES
    ]


def _get_modifier_animation(filename: str, size: int, initial_duration: float, anim_duration: float, scale: Scale) -> Animation:
    textures = Image.slice_horizontally_then_vertically(f"{filename}/{size}.png", size, size)
    count = len(textures)
    return Animation(
        [scale_by(texture, scale.scale) for texture in textures],
        [initial_duration] + [anim_duration / (count - 1)] * (count - 1)
    )


def _load_cell_animations(scale: Scale):
    global CELL_TEXTURES, CELL_ANIMATOR

    base_cell_animations = [
        _get_all_animations("resources/textures/cells/base", 4, scale),
        _get_all_animations("resources/textures/cells/selected", 4, scale)
    ]
    CELL_TEXTURES.append(base_cell_animations)
    CELL_ANIMATOR.add_animationss(base_cell_animations)

    forbidden_cell_animations = [_get_all_animations("resources/textures/cells/forbidden", 1.3, scale)]
    CELL_TEXTURES.append(forbidden_cell_animations)
    CELL_ANIMATOR.add_animations(*forbidden_cell_animations)

    blocker_cell_animations = [_get_all_animations("resources/textures/cells/blocker", 1, scale)]
    CELL_TEXTURES.append(blocker_cell_animations)
    CELL_ANIMATOR.add_animations(*blocker_cell_animations)


def _load_modifiers_animations(scale: Scale):
    global MODIFIERS_TEXTURES, CELL_ANIMATOR

    for folder in ('mult_0', 'mult_2', 'mult_5', 'circle_1', 'circle_2'):
        animations = [
            _get_modifier_animation("resources/textures/cells/_modifiers/" + folder, 64, 6, 0.5, scale),
            _get_modifier_animation("resources/textures/cells/_modifiers/" + folder, 128, 6, 0.5, scale)
        ]
        MODIFIERS_TEXTURES.append(animations)
        CELL_ANIMATOR.add_animations(animations)

    animations = [_get_modifier_animation("resources/textures/cells/_modifiers/pacifier", 64, 6, 0.5, scale)]
    MODIFIERS_TEXTURES.append(animations)
    CELL_ANIMATOR.add_animations(animations)
