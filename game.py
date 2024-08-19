import math

import pygame as pyg

import constants as co
import sounds
import textures
import utils
from bg_animation import BackgroundAnimation
from constants import GameState
from event_manager import EventManager
from level import Level, LevelManager
from options import Options
from screen_shake import SHAKER
from sound_manager import SoundManager
from window import Scale, Window


class Game:
    def __init__(self, screen: pyg.Surface, scale: Scale, is_browser: bool):
        self.state: GameState = GameState.NONE
        self.screen = screen
        self.scale = scale
        utils.SCALE = scale.scale
        self.bg_animation = BackgroundAnimation(self.scale)
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

        self.events.set_mouse_button_down_callback(self.click)
        self.events.set_mouse_button_up_callback(self.unclick)
        self.events.set_mouse_motion_callback(self.mouse_move)
        self.events.set_key_down_callback(self.key_down)

    def key_down(self, data: dict):
        if self.state == GameState.PLAYING_LEVEL:
            if data['key'] == co.R_KEY:
                self.restart_level()
            if data['key'] == co.N_KEY and self.current_level.animation == 0:
                self.start_next_level()
        elif self.state == GameState.END_OF_LEVEL:
            if data['key'] == co.R_KEY:
                self.restart_level()
            elif data['key'] == co.ENTER_KEY:
                self.start_next_level()
        elif self.state == GameState.MAIN_MENU:
            if data['key'] == co.ENTER_KEY:
                self.start_next_level()
        # TODO : remove quand publie
        if data['key'] == co.F12_KEY:
            pyg.image.save(self.screen, 'level_solutions/screenshot.png', 'png')

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
            elif co.PREVIOUS_LEVEL_BTN_RECT.collidepoint(x, y):
                self.start_previous_level()
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
        pyg.mouse.set_visible(False)
        textures.load_all(self.scale)
        SoundManager.instance().options = self.options
        sounds.load_sounds()

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
        if self.current_level.animation == 1:
            return

        LevelManager.instance().reload_current_level()
        self.current_level = LevelManager.instance().current_level
        self.state = GameState.PLAYING_LEVEL

    def start_next_level(self):
        if LevelManager.instance().on_last_level():
            self.state = GameState.END_OF_GAME
        else:
            LevelManager.instance().load_next_level()
            self.current_level = LevelManager.instance().current_level
            self.state = GameState.PLAYING_LEVEL

    def start_previous_level(self):
        if self.current_level.animation != 0:
            return

        if LevelManager.instance().number == 0:
            self.state = GameState.MAIN_MENU
        else:
            LevelManager.instance().load_previous_level()
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
        if self.state != GameState.BROWSER_WAIT_FOR_CLICK:
            game_surface.blit(
                textures.BACKGROUND if self.state != GameState.END_OF_LEVEL else textures.END_OF_LEVEL_BACKGROUND,
                self.scale.to_screen_pos(0, 0))

            if self.state == GameState.PLAYING_LEVEL:
                excl_rect = self.current_level.rect
            elif self.state == GameState.END_OF_LEVEL:
                excl_rect = co.EOL_BG_RECT
            else:
                excl_rect = None
            self.bg_animation.draw(game_surface, excl_rect, self.dt / 1000)

            utils.draw_text(game_surface, "By charon25", 42, self.scale.to_screen_pos(*co.CREDIT_TEXT_POS), co.MEDIUM_COLOR)

        if self.state == GameState.PLAYING_LEVEL:
            self.draw_game(game_surface)

        elif self.state == GameState.END_OF_LEVEL:
            self.draw_end_of_level(game_surface)

        elif self.state == GameState.MAIN_MENU:
            self.draw_main_menu(game_surface)

        elif self.state == GameState.END_OF_GAME:
            self.draw_end_of_game(game_surface)

        elif self.state == GameState.BROWSER_WAIT_FOR_CLICK:
            game_surface.fill(co.DARK_COLOR)
            utils.draw_text_center(game_surface, "Click anywhere to start the game", 100,
                                   self.scale.to_screen_rect(pyg.Rect(0, 0, co.WIDTH, co.HEIGHT)), (255, 255, 255))

        utils.draw_text(game_surface, f'{self.clock.get_fps():.0f} fps', 16, self.scale.to_screen_pos(1870, 1060),
                        co.DARK_COLOR)

        if self.state != GameState.BROWSER_WAIT_FOR_CLICK and self.state != GameState.END_OF_GAME:
            utils.draw_text_next_to_img(game_surface, textures.VOLUMES[self.options.music_volume],
                                        self.scale.to_screen_pos(*co.MUSIC_VOLUME_BTN_POS),
                                        co.OPTION_TEXT_BTN_GAP * self.scale.scale, 'Music', co.OPTION_TEXT_SIZE,
                                        co.MEDIUM_COLOR)
            utils.draw_text_next_to_img(game_surface, textures.VOLUMES[self.options.sfx_volume],
                                        self.scale.to_screen_pos(*co.SFX_VOLUME_BTN_POS),
                                        co.OPTION_TEXT_BTN_GAP * self.scale.scale, 'SFX', co.OPTION_TEXT_SIZE,
                                        co.MEDIUM_COLOR)

            utils.draw_text_center_right(game_surface, 'Hold click', co.OPTION_TEXT_SIZE,
                                         self.scale.to_screen_rect(co.HOLD_TEXT_RECT_1), co.MEDIUM_COLOR)
            utils.draw_text_center_right(game_surface, 'to grow', co.OPTION_TEXT_SIZE,
                                         self.scale.to_screen_rect(co.HOLD_TEXT_RECT_2), co.MEDIUM_COLOR)
            game_surface.blit(textures.CHECKBOXES[self.options.hold_to_grow],
                              self.scale.to_screen_pos(*co.HOLD_BTN_POS))

        if self.scale.x_offset > 0:
            pyg.draw.rect(game_surface, co.BLACK, pyg.Rect(0, 0, self.scale.x_offset, co.HEIGHT * self.scale.scale))
            pyg.draw.rect(game_surface, co.BLACK,
                          pyg.Rect(self.scale.x_offset + co.WIDTH * self.scale.scale, 0, self.scale.x_offset,
                                   co.HEIGHT * self.scale.scale))
        elif self.scale.y_offset > 0:
            pyg.draw.rect(game_surface, co.BLACK, pyg.Rect(0, 0, co.WIDTH * self.scale.scale, self.scale.y_offset))
            pyg.draw.rect(game_surface, co.BLACK,
                          pyg.Rect(0, self.scale.y_offset + co.HEIGHT * self.scale.scale, co.WIDTH * self.scale.scale,
                                   self.scale.y_offset))

        mouse_x, mouse_y = self.scale.to_game_pos(*pyg.mouse.get_pos())
        game_surface.blit(textures.CURSOR, self.scale.to_screen_pos(mouse_x - co.CURSOR_OFFSET / self.scale.scale,
                                                                    mouse_y - co.CURSOR_OFFSET / self.scale.scale))

        self.screen.blit(game_surface, SHAKER.get_next())

    def draw_game(self, game_surface):
        self.current_level.draw(game_surface, self.scale, self.dt / 1000, self.up_down[1])

        utils.blit_scaled(game_surface, textures.RESTART_LEVEL_BUTTON,
                          *self.scale.to_screen_pos(co.RESTART_LEVEL_BTN_POS[0],
                                                    co.RESTART_LEVEL_BTN_POS[1]),
                          self.in_out[1])

        utils.blit_scaled(game_surface, textures.PREVIOUS_LEVEL_BUTTON,
                          *self.scale.to_screen_pos(co.PREVIOUS_LEVEL_BTN_POS[0],
                                                    co.PREVIOUS_LEVEL_BTN_POS[1]),
                          self.in_out[1])

    def draw_end_of_level(self, game_surface: pyg.Surface):
        game_surface.blit(textures.END_OF_LEVEL_TITLE,
                          self.scale.to_screen_pos(co.EOL_TITLE_POS[0], co.EOL_TITLE_POS[1] + self.up_down[1]))

        utils.draw_text_and_img_centered(game_surface,
                                         textures.CELL_TEXTURES[0][1][
                                             co.TEXTURE_INDEX_FROM_SIZE[64]].get_current_sprite(),
                                         f'{self.current_level.points:.0f}',
                                         co.POINTS_TEXT_SIZE[1], self.scale.to_screen_rect(co.POINTS_TEXT_RECT), 15,
                                         co.DARK_COLOR)

        medal_count = len(self.current_level.required_points) - 1
        medals = self.current_level.get_medals()

        for k, (pos, medal) in enumerate(zip(co.MEDAL_POS[medal_count], medals)):
            game_surface.blit(textures.MEDALS[medal], self.scale.to_screen_pos(pos[0], pos[1] + self.up_down[1]))

            utils.draw_text_and_img_centered(game_surface, textures.CELL_TEXTURES[0][medal > 0][
                co.TEXTURE_INDEX_FROM_SIZE[32]].get_current_sprite(), f'{self.current_level.required_points[k]:.0f}',
                                             co.MEDAL_TEXT_FONT_SIZE, self.scale.to_screen_rect(
                    pyg.Rect(pos[0], co.MEDAL_TEXT_Y, co.MEDAL_WIDTH, co.MEDAL_TEXT_FONT_SIZE)), 8,
                                             co.DARK_COLOR, bold=medal > 0)

        utils.blit_scaled(game_surface, textures.RESTART_LEVEL_BUTTON,
                          *self.scale.to_screen_pos(co.EOL_RESTART_LEVEL_BTN_POS[0],
                                                    co.EOL_RESTART_LEVEL_BTN_POS[1]),
                          self.in_out[1])
        utils.blit_scaled(game_surface, textures.NEXT_LEVEL_BUTTON,
                          *self.scale.to_screen_pos(co.NEXT_LEVEL_BTN_POS[0], co.NEXT_LEVEL_BTN_POS[1]),
                          self.in_out[1])

    def draw_main_menu(self, game_surface: pyg.Surface):
        game_surface.blit(textures.LOGO, self.scale.to_screen_pos(co.LOGO_POS[0], co.LOGO_POS[1] + self.up_down[1]))
        utils.blit_scaled(game_surface, textures.PLAY_BUTTON,
                          *self.scale.to_screen_pos(co.PLAY_BTN_POS[0], co.PLAY_BTN_POS[1]), self.in_out[1])
        game_surface.blit(textures.GMTK_LOGO, self.scale.to_screen_pos(20, 20))
        if self.is_browser:
            game_surface.blit(textures.BROWSER_TEXT, self.scale.to_screen_pos(*co.BROWSER_TEXT_POS))

    def draw_end_of_game(self, game_surface: pyg.Surface):
        game_surface.blit(textures.LOGO, self.scale.to_screen_pos(co.LOGO_POS[0], co.LOGO_POS[1] + self.up_down[1]))
        utils.draw_text_center(game_surface, 'CONGRATULATIONS', 150, self.scale.to_screen_rect(co.EOG_TEXT1_RECT),
                               co.MEDIUM_COLOR, bold=True)
        utils.draw_text_center(game_surface, 'You beat the game!', 100, self.scale.to_screen_rect(co.EOG_TEXT2_RECT),
                               co.MEDIUM_COLOR)
        utils.draw_text_center(game_surface, 'Thanks for playing, please rate and comment :)', 45,
                               self.scale.to_screen_rect(co.EOG_TEXT3_RECT),
                               co.MEDIUM_COLOR)

        game_surface.blit(textures.MEDALS[1], self.scale.to_screen_pos(co.EOG_GOLD_MEDAL_POS[0],
                                                                       co.EOG_GOLD_MEDAL_POS[1] + self.up_down[1]))
        utils.draw_text(game_surface,
                        f'{sum(LevelManager.instance().gold_medals.values())} / {len(LevelManager.instance().gold_medals)}',
                        co.EOG_GOLD_MEDAL_TEXT_SIZE, self.scale.to_screen_pos(*co.EOG_GOLD_MEDAL_TEXT_POS),
                        co.MEDIUM_COLOR)
        utils.blit_scaled(game_surface, textures.RESTART_GAME_BUTTON,
                          *self.scale.to_screen_pos(co.EOG_RESTART_BTN_POS[0],
                                                    co.EOG_RESTART_BTN_POS[1]), self.in_out[1])

    def loop(self):
        self.frame += 1
        self.dt = self.clock.tick(self.target_fps)
        self.events.listen()

        self.loop_game()

        pyg.display.update()
