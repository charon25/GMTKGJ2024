import math


class CellAnimation:
    def __init__(self, total: int, order: int, phases: list[int]):
        factor = max(1.5, 15 - 3 * total)
        self.frame = -factor * order
        self.phases = phases
        self.phase = 0

        self.is_finished = False

    def get_scale(self) -> float:
        pass

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
