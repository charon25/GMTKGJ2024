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

        self.target_fps = 60 if not is_browser else 30
        self.clock = pyg.time.Clock()

        self.events = EventManager()
        self.events.set_quit_callback(self.stop)

        self.frame: int = 0
        self.dt: int = 0

        self.is_ended = False

        # Temp
        self.events.set_mouse_button_down_callback(self.click)
        self.events.set_mouse_button_up_callback(self.unclick)
        self.circle = Circle(0, 0, 0)
        self.current_level = Level(1, 32, [Cell(x, 0, 1, 1) for x in range(5)]
                                   + [Cell(0, 1, 2, 1)] + [Cell(0, 4, 1, 1, co.CellType.FORBIDDEN)]
                                   + [Cell(3, 1, 1, 1, co.CellType.MULT_2)])

    def click(self, data: dict):
        x, y = self.scale.to_game_pos(*data['pos'])
        self.current_level.click_on_level(int(x), int(y))

    def unclick(self, data: dict):
        self.current_level.validate_temp_circle()

    def start(self):
        textures.load_all(self.scale)

    def stop(self):
        self.is_ended = True
        Window.close()

    def loop_game(self):
        self.current_level.update(self.dt / 1000)

        textures.CELL_ANIMATOR.play_all(self.dt / 1000)
        self.draw_game()

    def draw_game(self):
        game_surface = pyg.Surface((co.WIDTH, co.HEIGHT), pyg.SRCALPHA)
        game_surface.fill((100, 100, 100))

        self.current_level.draw(game_surface, self.scale)

        font = pyg.font.Font(None, 30)
        text = font.render(f'{self.clock.get_fps():.0f} fps', False, (0, 0, 0))
        game_surface.blit(text, self.scale.to_screen_pos(10, 10))

        text = font.render(f'{self.current_level.points} points', False, (200, 200, 0))
        game_surface.blit(text, self.scale.to_screen_pos(900, 200))

        self.screen.blit(game_surface, (0, 0))

    def loop(self):
        self.frame += 1
        self.dt = self.clock.tick(self.target_fps)
        self.events.listen()

        self.loop_game()

        pyg.display.update()

        if self.frame % 60 == 0:
            print(f"fps={self.clock.get_fps()}")
