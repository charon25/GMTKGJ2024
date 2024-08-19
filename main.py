import asyncio

import pygame

import constants as co
from game import Game
from window import Window


async def main():
    pygame.init()
    pygame.display.init()
    screen = Window.create(width=960, height=540, fullscreen=False, title='GMTK 2024', icon_path='resources/icon.ico')
    scale = Window.get_scale(co.WIDTH, co.HEIGHT, screen=screen)

    game = Game(screen, scale, is_browser=True)
    game.start()

    while not game.is_ended:
        game.loop()
        await asyncio.sleep(0)

    game.stop()


asyncio.run(main())
