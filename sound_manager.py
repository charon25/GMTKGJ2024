import random

import pygame.mixer as mixer

import constants
from options import Options


class SoundManager:
    INSTANCE = None

    def __init__(self):
        self.sounds: dict[str, list[mixer.Sound]] = dict()
        self.musics: dict[str, str] = dict()
        mixer.init()
        mixer.music.set_endevent(constants.MUSICENDEVENT)
        self.options: Options = Options()

    @classmethod
    def instance(cls) -> 'SoundManager':
        if cls.INSTANCE is None:
            cls.INSTANCE = SoundManager()
        return cls.INSTANCE

    def add_sound(self, sound_path: str, sound_name: str) -> None:
        sound = mixer.Sound(sound_path)

        if sound_name not in self.sounds:
            self.sounds[sound_name] = []
        self.sounds[sound_name].append(sound)

    def play_random_sound(self, sound_name: str, volume: float = 1.0) -> None:
        sound_candidates = self.sounds.get(sound_name, None)

        if sound_candidates is None:
            return

        sound_to_play: mixer.Sound = random.choice(sound_candidates)
        base_volume = self.options.get_sfx_volume()
        if base_volume > 0:
            sound_to_play.set_volume(base_volume * volume)
            sound_to_play.play()

    def add_music(self, music_path: str, music_name: str) -> None:
        self.musics[music_name] = music_path

    def __play_music(self, music_path: str, loop: bool):
        mixer.music.load(music_path)
        mixer.music.play(loops=-int(loop))

    def play_random_music(self, loop: bool = False):
        if len(self.musics) == 0:
            raise ValueError("No music previously added.")

        music_to_play = random.choice(list(self.musics.values()))
        self.__play_music(music_to_play, loop=loop)

    def play_music(self, music_name: str, loop: bool = False):
        if music_name not in self.musics:
            raise IndexError(f"Music '{music_name}' does not exist.")

        self.__play_music(self.musics[music_name], loop=loop)
