import pygame as pyg
from pygame.image import load
from pygame.transform import scale_by

from animation_manager import Animation, AnimationManager
from window import Scale

CELL_TEXTURES: list[list[Animation]] = []
CELL_ANIMATOR = AnimationManager()


def load_scale(filename: str, scale: Scale) -> pyg.Surface:
    if scale.scale == 1:
        return load(filename)
    return scale_by(load(filename), scale.scale)


def load_all(scale: Scale):
    global CELL_TEXTURES, CELL_ANIMATOR
    base_cell_animations = [
        Animation(
            [load_scale("resources/cells/base/0.png", scale), load_scale("resources/cells/base/1.png", scale)],
            [0.5, 0.5]
        ),
        Animation(
            [load_scale("resources/cells/base/selected_0.png", scale),
             load_scale("resources/cells/base/selected_1.png", scale)],
            [0.5, 0.5]
        )
    ]

    CELL_TEXTURES.append(base_cell_animations)
    CELL_ANIMATOR.add_animations(base_cell_animations)

    forbidden_cell_animations = [
        Animation(
            [load_scale("resources/cells/forbidden/0.png", scale), load_scale("resources/cells/forbidden/1.png", scale)],
            [0.5, 0.5]
        )
    ]

    CELL_TEXTURES.append(forbidden_cell_animations)
    CELL_ANIMATOR.add_animations(forbidden_cell_animations)
