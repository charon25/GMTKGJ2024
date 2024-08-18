import pygame


class Image:
    @staticmethod
    def slice_by_columns(sprite_sheet: pygame.Surface, width: int) -> list[pygame.Surface]:
        height = sprite_sheet.get_height()

        sprites = list()
        for i in range(sprite_sheet.get_width() // width):
            sprite = pygame.Surface((width, height), pygame.SRCALPHA)
            sprite.blit(
                source=sprite_sheet,
                dest=(0, 0),
                area=(i * width, 0, width, height)
            )
            sprites.append(sprite)

        return sprites

    @staticmethod
    def slice_by_rows(sprite_sheet: pygame.Surface, height: int) -> list[pygame.Surface]:
        width = sprite_sheet.get_width()

        sprites = list()
        for i in range(sprite_sheet.get_height() // height):
            sprite = pygame.Surface((width, height), pygame.SRCALPHA)
            sprite.blit(
                source=sprite_sheet,
                dest=(0, 0),
                area=(0, i * height, width, height)
            )
            sprites.append(sprite)

        return sprites

    @staticmethod
    def slice_vertically_then_horizontally(filename: str, width: int, height: int) -> list[pygame.Surface]:
        sprite_sheet = pygame.image.load(filename)
        sprites_rows = Image.slice_by_columns(sprite_sheet, height)

        sprites = list()
        for row in sprites_rows:
            sprites.extend(Image.slice_by_rows(row, width))

        return sprites

    @staticmethod
    def slice_horizontally_then_vertically(filename: str, width: int, height: int) -> list[pygame.Surface]:
        sprite_sheet = pygame.image.load(filename)
        sprites_rows = Image.slice_by_rows(sprite_sheet, height)

        sprites = list()
        for row in sprites_rows:
            sprites.extend(Image.slice_by_columns(row, width))
        pygame.image.save(sprites[0], "test.png")

        return sprites
