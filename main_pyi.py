import pygame

import constants as co
from game import Game
from window import Window


def main():
    pygame.init()
    pygame.display.init()
    screen = Window.create(width=0, height=0, fullscreen=True, title='GMTK 2024', icon_path='resources/icon.ico')
    scale = Window.get_scale(co.WIDTH, co.HEIGHT, screen=screen)

    game = Game(screen, scale, is_browser=False)
    game.start()

    while not game.is_ended:
        game.loop()

    game.stop()


main()
