import pygame as pyg

import constants as co
from circle import Circle
from event_manager import EventManager
from window import Scale, Window


class Game:
    def __init__(self, screen: pyg.Surface, scale: Scale, is_browser: bool):
        self.screen = screen
        self.scale = scale
        self.is_browser = is_browser

        self.clock = pyg.time.Clock()

        self.events = EventManager()
        self.events.set_quit_callback(self.stop)

        self.events.set_mouse_button_down_callback(self.click)
        self.events.set_mouse_button_up_callback(self.unclick)
        self.circle = Circle(0, 0, 0)

        self.dt: int = 0

        self.is_ended = False

    def click(self, data: dict):
        x, y = data['pos']
        self.circle = Circle(x, y, 1)

    def unclick(self, data: dict):
        self.circle.radius = 0

    def start(self):
        pass

    def stop(self):
        self.is_ended = True
        Window.close()

    def draw_game(self):
        game_surface = pyg.Surface((co.WIDTH, co.HEIGHT), pyg.SRCALPHA)
        game_surface.fill((100, 100, 100))

        size = 60
        n_x = co.WIDTH // size
        n_y = co.HEIGHT // size
        for x in range(n_x):
            for y in range(n_y):
                rect = pyg.Rect(x * size, y * size, size, size)
                color = (255, 0, 0) if not self.circle.contains_rect(rect) else (0, 0, 255)
                pyg.draw.rect(game_surface, color, rect)

        if self.circle.radius > 0:
            self.circle.draw(game_surface)

        self.screen.blit(game_surface, (0, 0))

    def loop_game(self):
        if self.circle.radius > 0:
            self.circle.radius += 1
        self.draw_game()

    def loop(self):
        self.dt = self.clock.tick(60)
        print(self.clock.get_fps())
        self.events.listen()

        self.loop_game()

        pyg.display.update()
