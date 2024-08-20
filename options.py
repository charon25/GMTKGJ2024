import pygame.mixer

import sounds
import constants as co


class Options:
    def __init__(self):
        self.music_volume: int = 2
        self.sfx_volume: int = 2
        self.hold_to_grow: bool = True
        self.update_music_volume()

    def cycle_music_volume(self):
        if self.music_volume < co.MAX_VOLUME:
            self.music_volume += 1
        else:
            self.music_volume = 0
        self.update_music_volume()

    def cycle_music_volume_rev(self):
        if self.music_volume > 0:
            self.music_volume -= 1
        else:
            self.music_volume = co.MAX_VOLUME
        self.update_music_volume()

    def update_music_volume(self):
        pygame.mixer.music.set_volume(sounds.MAX_MUSIC_VOLUME * self.music_volume / co.MAX_VOLUME)

    def cycle_sfx_volume(self):
        if self.sfx_volume < co.MAX_VOLUME:
            self.sfx_volume += 1
        else:
            self.sfx_volume = 0

    def cycle_sfx_volume_rev(self):
        if self.sfx_volume > 0:
            self.sfx_volume -= 1
        else:
            self.sfx_volume = co.MAX_VOLUME

    def get_sfx_volume(self):
        return self.sfx_volume / co.MAX_VOLUME
