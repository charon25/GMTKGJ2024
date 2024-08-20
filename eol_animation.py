import sounds
from level import Level
import constants as co
from sound_manager import SoundManager


class EOLAnimation:
    def __init__(self, level: Level, dt: float):
        self.target_points = level.points
        self.current_points: float = 0.0
        self.delta: float = self.target_points * dt / co.EOL_ANIMATION_DURATION
        self.required_points = level.required_points
        self.target_medals = level.get_medals()
        self.current_medals = [0] * len(self.target_medals)

    def update(self):
        self.current_points += self.delta
        for i, pts in enumerate(self.required_points):
            if self.current_points >= pts and self.current_medals[i] != self.target_medals[i]:
                self.current_medals[i] = self.target_medals[i]
                SoundManager.instance().play_sound(sounds.EOL_EARN_MEDAL)

    def is_finished(self):
        return self.current_points >= self.target_points
