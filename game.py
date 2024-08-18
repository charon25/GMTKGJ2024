import math

import pygame as pyg

import constants as co
import textures
import utils
from circle import Circle
from constants import GameState
from event_manager import EventManager
from level import Level, LevelManager
from options import Options
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

        self.options: Options = Options()

        self.is_ended = False

        self.current_level: Level = None

        self.up_down: tuple[float, float] = (0.0, 0.0)
        self.in_out: tuple[float, float] = (0.0, 0.0)

        # Temp
        self.events.set_mouse_button_down_callback(self.click)
        self.events.set_mouse_button_up_callback(self.unclick)
        self.events.set_mouse_motion_callback(self.mouse_move)
        self.events.set_key_down_callback(self.key_down)
        self.circle = Circle(0, 0, 0)

    def key_down(self, data: dict):
        if self.state == GameState.PLAYING_LEVEL:
            if data['key'] == co.R_KEY:
                self.restart_level()
        elif self.state == GameState.END_OF_LEVEL:
            if data['key'] == co.R_KEY:
                self.restart_level()
            elif data['key'] == co.ENTER_KEY:
                self.start_next_level()
        elif self.state == GameState.MAIN_MENU:
            if data['key'] == co.ENTER_KEY:
                self.start_next_level()

        if data['key'] == co.F12_KEY:
            pyg.image.save(self.screen, 'screenshot.png', 'png')

    def click(self, data: dict):
        x, y = self.scale.to_game_pos(*data['pos'])
        button = data['button']
        if button == co.LEFT_CLICK:
            self.left_click(x, y)
        elif button == co.RIGHT_CLICK:
            self.right_click(x, y)

    def left_click(self, x: float, y: float):
        if self.state == GameState.PLAYING_LEVEL:
            if co.RESTART_LEVEL_BTN_RECT.collidepoint(x, y):
                self.restart_level()
            else:
                if self.options.hold_to_grow or self.current_level.temp_circle is None:
                    self.current_level.click_on_level(int(x), int(y))
                else:
                    self.current_level.validate_temp_circle()
                    self.current_level.on_mouse_move(int(x), int(y))

        elif self.state == GameState.END_OF_LEVEL:
            if co.EOL_RESTART_LEVEL_BTN_RECT.collidepoint(x, y):
                self.restart_level()
            elif co.NEXT_LEVEL_BTN_RECT.collidepoint(x, y):
                self.start_next_level()

        elif self.state == GameState.MAIN_MENU:
            if co.PLAY_BTN_RECT.collidepoint(x, y):
                LevelManager.reset()
                self.start_next_level()

        elif self.state == GameState.END_OF_GAME:
            if co.EOG_RESTART_BTN_RECT.collidepoint(x, y):
                self.open_main_menu()

        elif self.state == GameState.BROWSER_WAIT_FOR_CLICK:
            self.open_main_menu()

        if self.state != GameState.BROWSER_WAIT_FOR_CLICK and self.state != GameState.END_OF_GAME:
            if co.MUSIC_VOLUME_BTN_RECT.collidepoint(x, y):
                self.options.cycle_music_volume()
            elif co.SFX_VOLUME_BTN_RECT.collidepoint(x, y):
                self.options.cycle_sfx_volume()
            elif co.HOLD_BTN_RECT.collidepoint(x, y):
                self.options.hold_to_grow = not self.options.hold_to_grow

    def right_click(self, x: float, y: float):
        if self.state == GameState.PLAYING_LEVEL:
            self.current_level.destroy_temp_circle()

    def unclick(self, data: dict):
        if self.state == GameState.PLAYING_LEVEL and self.options.hold_to_grow:
            self.current_level.validate_temp_circle()
            x, y = self.scale.to_game_pos(*data['pos'])
            self.current_level.on_mouse_move(int(x), int(y))

    def mouse_move(self, data: dict):
        if self.state == GameState.PLAYING_LEVEL:
            x, y = self.scale.to_game_pos(*data['pos'])
            self.current_level.on_mouse_move(int(x), int(y))

    def start(self):
        textures.load_all(self.scale)

        if self.is_browser:
            self.state = GameState.BROWSER_WAIT_FOR_CLICK
        else:
            self.open_main_menu()

    def stop(self):
        self.is_ended = True
        Window.close()

    def open_main_menu(self):
        self.state = GameState.MAIN_MENU

    def restart_level(self):
        LevelManager.instance().reload_current_level()
        self.current_level = LevelManager.instance().current_level
        self.state = GameState.PLAYING_LEVEL

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

        self.up_down = (self.up_down[0] + self.dt / 1000, 4 * math.sin(2.5 * self.up_down[0]))
        self.in_out = (self.in_out[0] + self.dt / 1000, 1 + 0.03 * math.sin(2.5 * self.in_out[0]))

        textures.CELL_ANIMATOR.play_all(self.dt / 1000)
        self.draw()

    def draw(self):
        game_surface = pyg.Surface((co.WIDTH, co.HEIGHT), pyg.SRCALPHA)
        if self.state != GameState.END_OF_LEVEL and self.state != GameState.BROWSER_WAIT_FOR_CLICK:
            game_surface.blit(textures.BACKGROUND, self.scale.to_screen_pos(0, 0))

        if self.state == GameState.PLAYING_LEVEL:
            self.draw_game(game_surface)

        elif self.state == GameState.END_OF_LEVEL:
            self.draw_end_of_level(game_surface)

        elif self.state == GameState.MAIN_MENU:
            self.draw_main_menu(game_surface)

        elif self.state == GameState.END_OF_GAME:
            self.draw_end_of_game(game_surface)

        elif self.state == GameState.BROWSER_WAIT_FOR_CLICK:
            game_surface.fill((0, 0, 0))
            utils.draw_text_center(game_surface, "Click anywhere to start the game", 128,
                                   self.scale.to_screen_rect(pyg.Rect(0, 0, co.WIDTH, co.HEIGHT)), (255, 255, 255))

        utils.draw_text(game_surface, f'{self.clock.get_fps():.0f} fps', 16, self.scale.to_screen_pos(1880, 1065),
                        (0, 0, 0))

        if self.state != GameState.BROWSER_WAIT_FOR_CLICK and self.state != GameState.END_OF_GAME:
            utils.draw_text_next_to_img(game_surface, textures.VOLUMES[self.options.music_volume],
                                        co.MUSIC_VOLUME_BTN_POS, co.OPTION_TEXT_BTN_GAP, 'Music', co.OPTION_TEXT_SIZE,
                                        co.OPTION_TEXT_COLOR)
            utils.draw_text_next_to_img(game_surface, textures.VOLUMES[self.options.sfx_volume],
                                        co.SFX_VOLUME_BTN_POS, co.OPTION_TEXT_BTN_GAP, 'SFX', co.OPTION_TEXT_SIZE,
                                        co.OPTION_TEXT_COLOR)

            utils.draw_text_center_right(game_surface, 'Hold click', co.OPTION_TEXT_SIZE,
                                         self.scale.to_screen_rect(co.HOLD_TEXT_RECT_1), co.OPTION_TEXT_COLOR)
            utils.draw_text_center_right(game_surface, 'to grow', co.OPTION_TEXT_SIZE,
                                         self.scale.to_screen_rect(co.HOLD_TEXT_RECT_2), co.OPTION_TEXT_COLOR)
            game_surface.blit(textures.CHECKBOXES[self.options.hold_to_grow], co.HOLD_BTN_POS)

        self.screen.blit(game_surface, SHAKER.get_next())

    def draw_game(self, game_surface):
        self.current_level.draw(game_surface, self.scale, self.dt / 1000, self.up_down[1])

        utils.blit_scaled(game_surface, textures.RESTART_LEVEL_BUTTON, co.RESTART_LEVEL_BTN_POS[0],
                          co.RESTART_LEVEL_BTN_POS[1],
                          self.in_out[1])

    def draw_end_of_level(self, game_surface: pyg.Surface):
        game_surface.blit(textures.END_OF_LEVEL_BACKGROUND, self.scale.to_screen_pos(0, 0))
        game_surface.blit(textures.END_OF_LEVEL_TITLE, (co.EOL_TITLE_POS[0], co.EOL_TITLE_POS[1] + self.up_down[1]))

        utils.draw_text_next_to_img(game_surface,
                                    textures.CELL_TEXTURES[0][1][co.TEXTURE_INDEX_FROM_SIZE[64]].get_current_sprite(),
                                    self.scale.to_screen_pos(*co.POINTS_TEXT_POS), 15,
                                    f'{self.current_level.points:.0f}',
                                    co.POINTS_TEXT_SIZE[1], co.EOL_TEXT_COLOR)

        medal_count = len(self.current_level.required_points) - 1
        medals = self.current_level.get_medals()

        for k, (pos, medal) in enumerate(zip(co.MEDAL_POS[medal_count], medals)):
            game_surface.blit(textures.MEDALS[medal], self.scale.to_screen_pos(pos[0], pos[1] + self.up_down[1]))

            utils.draw_text_and_img_centered(game_surface, textures.CELL_TEXTURES[0][medal > 0][
                co.TEXTURE_INDEX_FROM_SIZE[32]].get_current_sprite(), f'{self.current_level.required_points[k]:.0f}',
                                             co.MEDAL_TEXT_FONT_SIZE, self.scale.to_screen_rect(
                    pyg.Rect(pos[0], co.MEDAL_TEXT_Y, co.MEDAL_WIDTH, co.MEDAL_TEXT_FONT_SIZE)), 8,
                                             co.EOL_TEXT_COLOR, bold=medal > 0)

        utils.blit_scaled(game_surface, textures.RESTART_LEVEL_BUTTON, co.EOL_RESTART_LEVEL_BTN_POS[0],
                          co.EOL_RESTART_LEVEL_BTN_POS[1],
                          self.in_out[1])
        utils.blit_scaled(game_surface, textures.NEXT_LEVEL_BUTTON, co.NEXT_LEVEL_BTN_POS[0], co.NEXT_LEVEL_BTN_POS[1],
                          self.in_out[1])

    def draw_main_menu(self, game_surface: pyg.Surface):
        game_surface.blit(textures.LOGO, (co.LOGO_POS[0], co.LOGO_POS[1] + self.up_down[1]))
        utils.blit_scaled(game_surface, textures.PLAY_BUTTON, co.PLAY_BTN_POS[0], co.PLAY_BTN_POS[1], self.in_out[1])

    def draw_end_of_game(self, game_surface: pyg.Surface):
        game_surface.blit(textures.LOGO, (co.LOGO_POS[0], co.LOGO_POS[1] + self.up_down[1]))
        utils.draw_text_center(game_surface, 'CONGRATULATIONS', 150, co.EOG_TEXT1_RECT, co.OPTION_TEXT_COLOR, bold=True)
        utils.draw_text_center(game_surface, 'You beat the game!', 100, co.EOG_TEXT2_RECT, co.OPTION_TEXT_COLOR)
        utils.draw_text_center(game_surface, 'Thanks for playing, please rate and comment :)', 45, co.EOG_TEXT3_RECT,
                               co.OPTION_TEXT_COLOR)

        game_surface.blit(textures.MEDALS[1], self.scale.to_screen_pos(co.EOG_GOLD_MEDAL_POS[0],
                                                                       co.EOG_GOLD_MEDAL_POS[1] + self.up_down[1]))
        utils.draw_text(game_surface,
                        f'{sum(LevelManager.instance().gold_medals.values())} / {len(LevelManager.instance().gold_medals)}',
                        co.EOG_GOLD_MEDAL_TEXT_SIZE, co.EOG_GOLD_MEDAL_TEXT_POS, co.OPTION_TEXT_COLOR)
        utils.blit_scaled(game_surface, textures.RESTART_GAME_BUTTON, co.EOG_RESTART_BTN_POS[0],
                          co.EOG_RESTART_BTN_POS[1], self.in_out[1])

    def loop(self):
        self.frame += 1
        self.dt = self.clock.tick(self.target_fps)
        self.events.listen()

        self.loop_game()

        pyg.display.update()
