import pygame as pyg
from pygame.image import load
from pygame.transform import scale_by

from window import Scale

BASE_CELL_TX: pyg.Surface = None
SELECTED_BASE_CELL_TX: pyg.Surface = None
FORBIDDEN_CELL_TX: pyg.Surface = None


def load_scale(name: str, scale: Scale) -> pyg.Surface:
    if scale.scale == 1:
        return load(name)
    return scale_by(load(name), scale.scale)


def load_all(scale: Scale):
    global BASE_CELL_TX, SELECTED_BASE_CELL_TX, FORBIDDEN_CELL_TX
    BASE_CELL_TX = load_scale('resources/base_cell.png', scale)
    SELECTED_BASE_CELL_TX = load_scale('resources/base_cell_selected.png', scale)
    FORBIDDEN_CELL_TX = load_scale('resources/forbidden_cell.png', scale)
