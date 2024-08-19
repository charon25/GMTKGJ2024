import pygame.mixer as mixer

from sound_manager import SoundManager

BUTTON_CLICK = "buttonClick"
CELL_SELECT = "cellSelect"


def add_sound(filepath: str, sound_name: str):
    SoundManager.instance().add_sound(filepath, sound_name)


def load_sounds():
    add_sound("resources/audio/sounds/btn_1.ogg", BUTTON_CLICK)
    add_sound("resources/audio/sounds/btn_2.ogg", BUTTON_CLICK)
    add_sound("resources/audio/sounds/cell_select_1.wav", CELL_SELECT)

