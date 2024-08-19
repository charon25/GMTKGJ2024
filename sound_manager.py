import random

import pygame.mixer as mixer

import constants
from options import Options


class SoundManager:
    INSTANCE = None

    def __init__(self):
        self.sounds: dict[str, mixer.Sound] = dict()
        self.musics: dict[str, str] = dict()
        mixer.init()
        self.options: Options = Options()

    @classmethod
    def instance(cls) -> 'SoundManager':
        if cls.INSTANCE is None:
            cls.INSTANCE = SoundManager()
        return cls.INSTANCE

    def add_sound(self, sound_path: str, sound_name: str) -> None:
        sound = mixer.Sound(sound_path)
        self.sounds[sound_name] = sound

    def play_sound(self, sound_name: str, volume: float = 1.0) -> None:
        sound = self.sounds.get(sound_name, None)
        if sound is None:
            return

        base_volume = self.options.get_sfx_volume()
        if base_volume > 0:
            sound.set_volume(base_volume * volume)
            sound.play()

    def stop_sound(self, sound_name):
        sound = self.sounds.get(sound_name, None)
        if sound is None:
            return

        sound.stop()

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
