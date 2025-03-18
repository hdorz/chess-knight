import pygame as pg


class SpriteGroup(pg.sprite.RenderPlain):
    """
    SpriteGroup class holds a list of sprites to organise sprites when changing
    between different sets of sprites.
    """

    def __init__(self, sprites: list) -> None:
        super().__init__(*sprites)

    def addSprites(self, sprites: list):
        super().add(*sprites)
