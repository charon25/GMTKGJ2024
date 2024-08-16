import asyncio

import pygame

import constants as co
from game import Game
from window import Window


async def main():
    pygame.init()
    pygame.display.init()
    screen = Window.create(width=0, height=0, fullscreen=True, title='GMTK 2024', icon_path='resources/icon.ico')
    scale = Window.get_scale(co.WIDTH, co.HEIGHT, screen=screen)

    game = Game(screen, scale, is_browser=True)
    game.start()

    while not game.is_ended:
        game.loop()
        await asyncio.sleep(0)

    game.stop()


asyncio.run(main())
