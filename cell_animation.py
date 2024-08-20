import math

import constants
import sounds
from sound_manager import SoundManager


class CellAnimation:
    NO_DISPLACEMENT = (0, 0)

    def __init__(self, total: int, order: int, phases: list[int]):
        factor = 15 if total < 10 else max(1.5, 15 - total / 2)
        self.frame = -factor * order
        self.phases = phases
        self.phase = 0

        self.is_finished = False

    def get_scale(self) -> float:
        return 1.0

    def get_displacement(self) -> tuple[float, float]:
        return CellAnimation.NO_DISPLACEMENT

    def get_type(self) -> int:
        return 0

    def update(self, dt: float) -> None:
        if self.is_finished:
            return

        self.frame += dt * 60
        if self.frame >= self.phases[self.phase]:
            self.phase += 1
            self.is_finished = (self.phase >= len(self.phases))


class CellSelectAnimation(CellAnimation):
    def __init__(self, total: int, order: int):
        super().__init__(total, order, [0, 15, 22])

    def get_scale(self) -> float:
        if self.phase == 0:
            return 1.0
        elif self.phase == 1:
            return 0.7007 * math.exp(-0.4 * self.frame) + 0.29929
        elif self.phase == 2:
            return 0.1 * self.frame - 1.2
        return 1.0

    def get_type(self) -> int:
        return constants.CELL_SELECT_ANIMATION


class CellTempSelectAnimation(CellAnimation):
    def __init__(self):
        super().__init__(1, 0, [0, 20])

    def get_scale(self) -> float:
        if self.phase == 0:
            return 1.0
        elif self.phase == 1:
            return 1 + math.exp(-((self.frame - 10) / 10) ** 2) / 10
        return 1.0

    def get_type(self) -> int:
        return constants.CELL_TEMP_SELECT_ANIMATION


class CellTouchAnimation(CellAnimation):
    def __init__(self, dir_x: float, dir_y: float, intensity: int):
        super().__init__(1, 0, [0, 14])
        self.dir_x = dir_x
        self.dir_y = dir_y
        self.intensity = min(constants.CELL_TOUCH_ANIMATION_MAX_INTENSITY, max(constants.CELL_TOUCH_ANIMATION_MIN_INTENSITY, intensity))

    def get_displacement(self) -> tuple[float, float]:
        if self.phase == 0:
            return CellAnimation.NO_DISPLACEMENT
        elif self.phase == 1 or self.phase == 2:
            factor = self.intensity * math.exp(-((self.frame - 7) / 3.5) ** 2)
            return factor * self.dir_x, factor * self.dir_y
        return CellAnimation.NO_DISPLACEMENT

    def get_type(self) -> int:
        return constants.CELL_TOUCH_ANIMATION
