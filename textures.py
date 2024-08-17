import pygame as pyg
from pygame.image import load
from pygame.transform import scale_by

from animation_manager import Animation, AnimationManager
from window import Scale

CELL_TEXTURES: list[list[Animation]] = list()
MODIFIERS_TEXTURES: list[Animation] = list()
CELL_ANIMATOR = AnimationManager()

END_OF_LEVEL_BACKGROUND = load("resources/textures/eol/end_of_level_bg.png")
END_OF_LEVEL_TITLE = load("resources/textures/eol/end_of_level_title.png")
MEDALS: list[pyg.Surface] = [
    load("resources/textures/eol/empty_medal.png"),
    load("resources/textures/eol/gold_medal.png"),
    load("resources/textures/eol/silver_medal.png"),
    load("resources/textures/eol/bronze_medal.png")
]


def load_scale(filename: str, scale: Scale) -> pyg.Surface:
    if scale.scale == 1:
        return load(filename)
    return scale_by(load(filename), scale.scale)


def load_all(scale: Scale):
    _load_textures(scale)
    _load_cell_animations(scale)
    _load_modifiers_animations(scale)


def _load_textures(scale: Scale):
    global END_OF_LEVEL_BACKGROUND, END_OF_LEVEL_TITLE, MEDALS

    if abs(1 - scale.scale) <= 0.03:
        return

    END_OF_LEVEL_BACKGROUND = scale_by(END_OF_LEVEL_BACKGROUND, scale.scale)
    END_OF_LEVEL_TITLE = scale_by(END_OF_LEVEL_TITLE, scale.scale)
    for i, texture in enumerate(MEDALS):
        MEDALS[i] = scale_by(texture, scale.scale)


def _load_cell_animations(scale: Scale):
    global CELL_TEXTURES, CELL_ANIMATOR

    base_cell_animations = [
        Animation(
            [load_scale("resources/textures/cells/base/0.png", scale),
             load_scale("resources/textures/cells/base/1.png", scale)],
            [0.5, 0.5]
        ),
        Animation(
            [load_scale("resources/textures/cells/base/selected_0.png", scale),
             load_scale("resources/textures/cells/base/selected_1.png", scale)],
            [0.5, 0.5]
        )
    ]

    CELL_TEXTURES.append(base_cell_animations)
    CELL_ANIMATOR.add_animations(base_cell_animations)

    forbidden_cell_animations = [
        Animation(
            [load_scale("resources/textures/cells/forbidden/0.png", scale),
             load_scale("resources/textures/cells/forbidden/1.png", scale)],
            [0.5, 0.5]
        )
    ]

    CELL_TEXTURES.append(forbidden_cell_animations)
    CELL_ANIMATOR.add_animations(forbidden_cell_animations)

    blocker_cell_animations = [
        Animation(
            [load_scale("resources/textures/cells/blocker/0.png", scale)],
            [0.5]
        )
    ]

    CELL_TEXTURES.append(blocker_cell_animations)
    CELL_ANIMATOR.add_animations(blocker_cell_animations)


def _load_modifiers_animations(scale: Scale):
    global MODIFIERS_TEXTURES, CELL_ANIMATOR

    mult_2_anim = Animation(
        [load_scale("resources/textures/cells/_modifiers/mult_2/0.png", scale)],
        [0.5]
    )
    MODIFIERS_TEXTURES.append(mult_2_anim)
    CELL_ANIMATOR.add_animation(mult_2_anim)

    circle_p1_anim = Animation(
        [load_scale("resources/textures/cells/_modifiers/circle_p1/0.png", scale)],
        [0.5]
    )
    MODIFIERS_TEXTURES.append(circle_p1_anim)
    CELL_ANIMATOR.add_animation(circle_p1_anim)
