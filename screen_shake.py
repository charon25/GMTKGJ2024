import math
import random

import constants as co


class ScreenShake:
    def __init__(self):
        self.frame = 0
        self.values: list[tuple[int, int]] = list()

    def shake(self, intensity: int):
        self.frame = 0
        self.values = list()

        intensity = min(co.SCREEN_SHAKE_MAX_INTENSITY, intensity)
        angle = random.random() * math.pi / 2 + math.pi / 4
        if random.random() < 0.5:
            angle = -angle

        dir_x, dir_y = math.cos(angle), math.sin(angle)
        for n in range(co.SCREEN_SHAKE_COUNT + 1):
            value = math.sin(n * co.FREQUENCY) * intensity
            self.values.append((value * dir_x, value * dir_y))

    def get_next(self) -> tuple[int, int]:
        if self.frame < len(self.values):
            value = self.values[self.frame]
            self.frame += 1
            return value

        return 0, 0


SHAKER = ScreenShake()
