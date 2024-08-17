import pygame as pyg

import constants as co
import textures
import utils
from circle import Circle
from constants import GameState
from event_manager import EventManager
from level import Level, LevelManager
from screen_shake import SHAKER
from window import Scale, Window


class Game:
    def __init__(self, screen: pyg.Surface, scale: Scale, is_browser: bool):
        self.state: GameState = GameState.NONE
        self.screen = screen
        self.scale = scale
        self.is_browser = is_browser

        self.target_fps = 60
        self.clock = pyg.time.Clock()

        self.events = EventManager()
        self.events.set_quit_callback(self.stop)

        self.frame: int = 0
        self.dt: int = 0

        self.is_ended = False

        self.current_level: Level = None

        # Temp
        self.events.set_mouse_button_down_callback(self.click)
        self.events.set_mouse_button_up_callback(self.unclick)
        self.events.set_mouse_motion_callback(self.mouse_move)
        self.events.set_key_down_callback(self.screenshot)
        self.circle = Circle(0, 0, 0)

    def screenshot(self, data: dict):
        if data['key'] == 1073741893:
            pyg.image.save(self.screen, 'screenshot.png', 'png')

    def click(self, data: dict):
        if self.state == GameState.PLAYING_LEVEL:
            x, y = self.scale.to_game_pos(*data['pos'])
            self.current_level.click_on_level(int(x), int(y))
        elif self.state == GameState.END_OF_LEVEL:
            # todo temp
            self.start_next_level()
        elif self.state == GameState.BROWSER_WAIT_FOR_CLICK:
            # todo temp
            self.start_next_level()

    def unclick(self, data: dict):
        if self.state == GameState.PLAYING_LEVEL:
            self.current_level.validate_temp_circle()

    def mouse_move(self, data: dict):
        if self.state == GameState.PLAYING_LEVEL:
            x, y = self.scale.to_game_pos(*data['pos'])
            self.current_level.on_mouse_move(int(x), int(y))

    def start(self):
        textures.load_all(self.scale)

        if self.is_browser:
            self.state = GameState.BROWSER_WAIT_FOR_CLICK
        else:
            # todo temp
            self.start_next_level()

    def stop(self):
        self.is_ended = True
        Window.close()

    def start_next_level(self):
        if LevelManager.instance().are_all_level_complete():
            self.state = GameState.END_OF_GAME
        else:
            LevelManager.instance().load_next_level()
            self.current_level = LevelManager.instance().current_level
            self.state = GameState.PLAYING_LEVEL

    def loop_game(self):
        if self.state == GameState.PLAYING_LEVEL:
            if not LevelManager.instance().current_level_ended:
                self.current_level.update(self.dt / 1000)
            else:
                self.state = GameState.END_OF_LEVEL

        elif self.state == GameState.END_OF_LEVEL:
            pass

        textures.CELL_ANIMATOR.play_all(self.dt / 1000)
        self.draw_game()

    def draw_game(self):
        game_surface = pyg.Surface((co.WIDTH, co.HEIGHT), pyg.SRCALPHA)
        game_surface.fill((200, 200, 200, 255))

        utils.draw_text(game_surface, f'{self.clock.get_fps():.0f} fps', 30, self.scale.to_screen_pos(10, 10),
                        (0, 0, 0))

        if self.state == GameState.PLAYING_LEVEL:
            self.current_level.draw(game_surface, self.scale, self.dt / 1000)

            utils.draw_text(game_surface, f'{self.current_level.points} points', 30, self.scale.to_screen_pos(900, 200),
                            (200, 0, 0))
        elif self.state == GameState.END_OF_LEVEL:
            self.draw_end_of_level(game_surface)

        self.screen.blit(game_surface, SHAKER.get_next())

    def draw_end_of_level(self, game_surface: pyg.Surface):
        game_surface.blit(textures.END_OF_LEVEL_BACKGROUND, self.scale.to_screen_pos(co.EOL_BG_X, 0))
        game_surface.blit(textures.END_OF_LEVEL_TITLE, self.scale.to_screen_pos(*co.EOL_TITLE_POS))

        medal_count = len(self.current_level.required_points) - 1
        medals = self.current_level.get_medals()

        for pos, medal in zip(co.MEDAL_POS[medal_count], medals):
            game_surface.blit(textures.MEDALS[medal], pos)


    def loop(self):
        self.frame += 1
        self.dt = self.clock.tick(self.target_fps)
        self.events.listen()

        self.loop_game()

        pyg.display.update()
