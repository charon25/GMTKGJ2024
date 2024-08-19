import pygame.mixer as mixer

from sound_manager import SoundManager

BUTTON_CLICK = "buttonClick"
CELL_SELECT = "cellSelect"
REMOVE_CIRCLE = "removeCircle"
VALIDATE_CIRCLE_BLOCKER = "validateCircleBlocker"
VALIDATE_CIRCLE_CLICK = "validateCircleClick"
GROWING_CIRCLE = "growingCircle"


def add_sound(filepath: str, sound_name: str):
    SoundManager.instance().add_sound(filepath, sound_name)


def load_sounds():
    add_sound("resources/audio/sounds/btn_1.ogg", BUTTON_CLICK)
    add_sound("resources/audio/sounds/btn_2.ogg", BUTTON_CLICK)

    add_sound("resources/audio/sounds/cell_select_1.wav", CELL_SELECT)

    add_sound("resources/audio/sounds/remove_circle_1.ogg", REMOVE_CIRCLE)
    add_sound("resources/audio/sounds/remove_circle_2.ogg", REMOVE_CIRCLE)
    add_sound("resources/audio/sounds/remove_circle_3.ogg", REMOVE_CIRCLE)

    add_sound("resources/audio/sounds/validate_circle_blocker_1.ogg", VALIDATE_CIRCLE_BLOCKER)
    add_sound("resources/audio/sounds/validate_circle_blocker_2.ogg", VALIDATE_CIRCLE_BLOCKER)

    add_sound("resources/audio/sounds/growing_circle.wav", GROWING_CIRCLE)
