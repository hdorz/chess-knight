import pygame as pg

from .SpriteGroup import SpriteGroup


class DisplayInstance:
    """
    Declare a single instance of the Display class for the entire application.
    """

    obj = None

    @staticmethod
    def getInstance():
        if not DisplayInstance.obj:
            DisplayInstance.obj = Display()
        return DisplayInstance.obj


class Display:
    """
    Display class allows for screen updates at different places in the codebase.
    Main use case is to allow for screen updates to occur within a Turn.execute()
    method without needing to expose logic in the main game loop.
    """

    def __init__(self) -> None:
        self.screen = None
        self.backgroundSet = None
        self.background = None
        self.sprites: SpriteGroup = None

    def setup(self, screen, backgroundSet, background, sprites):
        self.screen = screen
        self.backgroundSet = backgroundSet
        self.background = background
        self.sprites = sprites

    def setSprites(self, sprites: SpriteGroup):
        self.sprites = sprites

    def getSprites(self):
        return self.sprites

    def setBackgroundSet(self, backgroundSet):
        self.backgroundSet = backgroundSet

    def setBackground(self, background):
        self.background = background

    def updateSprites(self):
        if self.sprites is not None:
            self.sprites.update()

    def clear(self):
        self.sprites.clear(self.screen, self.background)

    def updateDisplay(self):
        self.updateSprites()
        for backgroundPiece in self.backgroundSet:
            self.screen.blit(*backgroundPiece)
        if self.sprites is not None:
            self.sprites.draw(self.screen)
        pg.display.flip()
        # flip() the display to put your work on screen / update screen
