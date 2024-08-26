import pygame

import constants as co
from game import Game
from window import Window


def main():
    pygame.init()
    pygame.display.init()
    screen = Window.create(width=1920, height=1080, fullscreen=True, title='Squale', icon_path='resources/icon.ico')
    scale = Window.get_scale(co.WIDTH, co.HEIGHT, screen=screen)

    game = Game(screen, scale, is_browser=False)
    game.start()

    while not game.is_ended:
        game.loop()

    Window.close()


main()
