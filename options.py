class Options:
    def __init__(self):
        self.music_volume: int = 2
        self.sfx_volume: int = 2

    def cycle_music_volume(self):
        if self.music_volume < 3:
            self.music_volume += 1
        else:
            self.music_volume = 0

    def cycle_sfx_volume(self):
        if self.sfx_volume < 3:
            self.sfx_volume += 1
        else:
            self.sfx_volume = 0
