from .constants import PLAYER_1, PLAYER_2, blackFontColour, windowSize
from .utilities import load_image, resource_path

currentPlayerBackgroundScale = (windowSize[1] + 150) / 1280


class CurrentPlayerSurface:
    """
    CurrentPlayerSurface class displays current player's turn.
    """

    def __init__(self, coord: tuple) -> None:
        self.playerSurface = None
        self.backGroundSurface = None
        self.textSurface = None
        self.font_size = 30
        self.font = None
        self.message = "turn"
        self.coord = coord

        self._setBackgroundSurface()

    def setup(self, font):
        """
        Should be run after pygame.init()
        """
        self._setFont(font)

    def getPlayerName(self):
        return self.playerName

    def incrementPoints(self, points: int):
        self.points += points

    def _setFont(self, font):
        """
        Pass in pygame.font.Font function. Call this after pygame.init()
        """
        self.font = font(
            resource_path("chess/data/font/BerlinSansFB.TTF"), self.font_size
        )

    def _setTextSurface(self):
        """
        Set text surface based on font. Call this after pygame.init()
        """
        self.textSurface = self.font.render(self.message, False, blackFontColour)

    def _setBackgroundSurface(self):
        """
        Set background for player display.
        """
        self.backgroundSurface, _ = load_image(
            "notifications/player_display_bg.png",
            scale=currentPlayerBackgroundScale,
        )

    def _textCoord(self):
        return (
            self.coord[0] + 20,
            self.coord[1] + 25,
        )

    def setCurrentPlayer(self, playerName: str):
        self.message = f"{playerName}'s turn"

    def render(self):
        self._setTextSurface()

        return (
            (self.backgroundSurface, self.coord),
            (self.textSurface, self._textCoord()),
        )


class CurrentPlayerSurfaceInstance:
    """
    Declare a single instance of the CurrentPlayerSurface class for
    the entire application. Uses Singleton design pattern.
    """

    obj = None

    @staticmethod
    def getInstance() -> CurrentPlayerSurface:
        if not CurrentPlayerSurfaceInstance.obj:
            CurrentPlayerSurfaceInstance.obj = CurrentPlayerSurface(
                coord=(0, 200),
            )
        return CurrentPlayerSurfaceInstance.obj


class PlayerPointsSurface:
    """
    PlayerPointsSurface class displays a player's turn.
    """

    def __init__(self, playerName: str, coord: tuple) -> None:
        self.playerSurface = None
        self.backGroundSurface = None
        self.textSurface = None
        self.font_size = 30
        self.font = None
        self.message = "turn"
        self.coord = coord

        self.playerName = playerName
        self.points = 0

        self._setBackgroundSurface()

    def setup(self, font):
        """
        Should be run after pygame.init()
        """
        self._setFont(font)

    def getPlayerName(self):
        return self.playerName

    def incrementPoints(self, points: int):
        self.points += points

    def _setFont(self, font):
        """
        Pass in pygame.font.Font function. Call this after pygame.init()
        """
        self.font = font(
            resource_path("chess/data/font/BerlinSansFB.TTF"), self.font_size
        )

    def _setTextSurface(self):
        """
        Set text surface based on font. Call this after pygame.init()
        """
        self.textSurface = self.font.render(self.message, False, blackFontColour)

    def _setBackgroundSurface(self):
        """
        Set background for player display.
        """
        self.backgroundSurface, _ = load_image(
            "notifications/player_display_bg.png",
            scale=currentPlayerBackgroundScale,
        )

    def _textCoord(self):
        return (
            self.coord[0] + 20,
            self.coord[1] + 25,
        )

    def render(self):
        self.message = f"{self.playerName}'s score: {self.points}"
        self._setTextSurface()

        return (
            (self.backgroundSurface, self.coord),
            (self.textSurface, self._textCoord()),
        )


class PlayerOnePointsInstance:
    """
    Declare a single instance of the PlayerPointsSurface class for
    the entire application. Uses Singleton design pattern.
    """

    obj = None

    @staticmethod
    def getInstance() -> PlayerPointsSurface:
        if not PlayerOnePointsInstance.obj:
            PlayerOnePointsInstance.obj = PlayerPointsSurface(
                playerName=PLAYER_1,
                coord=(0, 0),
            )
        return PlayerOnePointsInstance.obj


class PlayerTwoPointsInstance:
    """
    Declare a single instance of the PlayerPointsSurface class for
    the entire application. Uses Singleton design pattern.
    """

    obj = None

    @staticmethod
    def getInstance() -> PlayerPointsSurface:
        if not PlayerTwoPointsInstance.obj:
            PlayerTwoPointsInstance.obj = PlayerPointsSurface(
                playerName=PLAYER_2,
                coord=(0, 100),
            )
        return PlayerTwoPointsInstance.obj
