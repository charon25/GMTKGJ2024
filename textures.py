import pygame as pyg
from pygame.image import load
from pygame.transform import scale_by

from animation_manager import Animation, AnimationManager
from window import Scale

CELL_TEXTURES: list[list[Animation]] = []
MODIFIERS_TEXTURES: list[Animation] = []
CELL_ANIMATOR = AnimationManager()


def load_scale(filename: str, scale: Scale) -> pyg.Surface:
    if scale.scale == 1:
        return load(filename)
    return scale_by(load(filename), scale.scale)


def load_all(scale: Scale):
    _load_cell_animations(scale)
    _load_modifiers_animations(scale)


def _load_cell_animations(scale: Scale):
    global CELL_TEXTURES, CELL_ANIMATOR

    base_cell_animations = [
        Animation(
            [load_scale("resources/textures/base/0.png", scale), load_scale("resources/textures/base/1.png", scale)],
            [0.5, 0.5]
        ),
        Animation(
            [load_scale("resources/textures/base/selected_0.png", scale),
             load_scale("resources/textures/base/selected_1.png", scale)],
            [0.5, 0.5]
        )
    ]

    CELL_TEXTURES.append(base_cell_animations)
    CELL_ANIMATOR.add_animations(base_cell_animations)

    forbidden_cell_animations = [
        Animation(
            [load_scale("resources/textures/forbidden/0.png", scale),
             load_scale("resources/textures/forbidden/1.png", scale)],
            [0.5, 0.5]
        )
    ]

    CELL_TEXTURES.append(forbidden_cell_animations)
    CELL_ANIMATOR.add_animations(forbidden_cell_animations)


def _load_modifiers_animations(scale: Scale):
    global MODIFIERS_TEXTURES, CELL_ANIMATOR

    mult_2_anim = Animation(
        [load_scale("resources/textures/_modifiers/mult_2/0.png", scale)],
        [0.5]
    )
    MODIFIERS_TEXTURES.append(mult_2_anim)
    CELL_ANIMATOR.add_animation(mult_2_anim)

    circle_p1_anim = Animation(
        [load_scale("resources/textures/_modifiers/circle_p1/0.png", scale)],
        [0.5]
    )
    MODIFIERS_TEXTURES.append(circle_p1_anim)
    CELL_ANIMATOR.add_animation(circle_p1_anim)
