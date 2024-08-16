import pygame as pyg
from pygame.surface import Surface

from event_manager import EventManager
from window import Scale, Window


class Game:
    def __init__(self, screen: Surface, scale: Scale, is_browser: bool):
        self.screen = screen
        self.scale = scale
        self.is_browser = is_browser

        self.clock = pyg.time.Clock()

        self.events = EventManager()
        self.events.set_quit_callback(self.stop)

        self.dt: int = 0

        self.is_ended = False

    def start(self):
        pass

    def stop(self):
        self.is_ended = True
        Window.close()

    def loop(self):
        self.dt = self.clock.tick(60)
        self.events.listen()

        pyg.display.update()
