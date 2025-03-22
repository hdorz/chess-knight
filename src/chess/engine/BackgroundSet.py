from abc import ABC, abstractmethod

from .CurrentPlayerSurface import (
    CurrentPlayerSurfaceInstance,
    PlayerOnePointsInstance,
    PlayerTwoPointsInstance,
)
from .Notification import NotificationInstance
from .utilities import load_image


class BackgroundSet(ABC):
    """
    BackgroundSet class handles the surfaces required to display. As a general
    rule, BackgroundSet() objects should only be instantiated after pygame.init()
    """

    def __init__(self, background):
        if type(self) is BackgroundSet:
            raise Exception("BackgroundSet class is an abstract class")
        self.background = background
        self.backgroundSet = []

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def getBackground(self):
        pass

    @abstractmethod
    def getSet(self):
        pass


class GameBackground(BackgroundSet):
    """
    GameBackground displays the surfaces needed to be shown during
    normal gameplay.
    """

    def __init__(self, background):
        super().__init__(background=background)
        self.notification = NotificationInstance.getInstance()
        self.playerOneSurface = PlayerOnePointsInstance.getInstance()
        self.playerTwoSurface = PlayerTwoPointsInstance.getInstance()
        self.currentPlayerSurface = CurrentPlayerSurfaceInstance.getInstance()

        self.update()

    def update(self):
        notificationText, notificationBackground = self.notification.render()
        playerOneBackgroundSurface, playerOneTextSurface = (
            self.playerOneSurface.render()
        )
        playerTwoBackgroundSurface, playerTwoTextSurface = (
            self.playerTwoSurface.render()
        )
        currentPlayerBackgroundSurface, currentPlayerTextSurface = (
            self.currentPlayerSurface.render()
        )
        self.backgroundSet = [
            (self.background, (0, 0)),
            notificationBackground,
            notificationText,
            playerOneBackgroundSurface,
            playerOneTextSurface,
            playerTwoBackgroundSurface,
            playerTwoTextSurface,
            currentPlayerBackgroundSurface,
            currentPlayerTextSurface,
        ]

    def getBackground(self):
        return self.background

    def getSet(self):
        self.update()
        return self.backgroundSet


class StartingBackground(BackgroundSet):
    """
    StartingBackground displays the surfaces for start menu.
    """

    def __init__(self, background):
        super().__init__(background=background)
        self.header = None
        self.setHeader()
        self.update()

    def setHeader(self):
        self.header, _ = load_image(
            "menu/KnightChess.png",
            colorkey=-1,
            scale=1,
        )
        self.header = self.header.convert()

    def update(self):
        self.backgroundSet = [
            (self.background, (0, 0)),
            (self.header, (100, 100)),
        ]

    def getBackground(self):
        return self.background

    def getSet(self):
        self.update()
        return self.backgroundSet


class SelectModeBackground(BackgroundSet):
    """
    StartingBackground displays the surfaces for start menu.
    """

    def __init__(self, background):
        super().__init__(background=background)
        self.header = None
        self.setHeader()
        self.update()

    def setHeader(self):
        self.header, _ = load_image(
            "menu/WhichMode.png",
            colorkey=-1,
            scale=0.7,
        )
        self.header = self.header.convert()

    def update(self):
        self.backgroundSet = [
            (self.background, (0, 0)),
            (self.header, (300, 100)),
        ]

    def getBackground(self):
        return self.background

    def getSet(self):
        self.update()
        return self.backgroundSet
