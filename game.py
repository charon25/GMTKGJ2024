import pygame as pyg

import constants as co
import textures
from cell import Cell
from circle import Circle
from event_manager import EventManager
from level import Level
from window import Scale, Window


class Game:
    def __init__(self, screen: pyg.Surface, scale: Scale, is_browser: bool):
        self.screen = screen
        self.scale = scale
        self.is_browser = is_browser

        self.clock = pyg.time.Clock()

        self.events = EventManager()
        self.events.set_quit_callback(self.stop)

        self.dt: int = 0

        self.is_ended = False

        # Temp
        self.events.set_mouse_button_down_callback(self.click)
        self.events.set_mouse_button_up_callback(self.unclick)
        self.circle = Circle(0, 0, 0)
        self.current_level = Level(1, 32, [Cell(x, 0, 1, 1) for x in range(5)] + [Cell(0, 1, 2, 1)])

    def click(self, data: dict):
        x, y = data['pos']
        self.current_level.set_temp_circle_position(x, y)

    def unclick(self, data: dict):
        self.current_level.validate_temp_circle()

    def start(self):
        textures.load_all(self.scale)

    def stop(self):
        self.is_ended = True
        Window.close()

    def loop_game(self):
        self.current_level.widen_temp_circle()

        self.draw_game()

    def draw_game(self):
        game_surface = pyg.Surface((co.WIDTH, co.HEIGHT), pyg.SRCALPHA)
        game_surface.fill((100, 100, 100))

        self.current_level.draw(game_surface, self.scale)

        self.screen.blit(game_surface, (0, 0))

    def loop(self):
        self.dt = self.clock.tick(60)
        self.events.listen()

        self.loop_game()

        pyg.display.update()
