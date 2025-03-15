from __future__ import annotations

from abc import abstractmethod
from typing import Literal

from .engine.SpriteImage import SpriteImage


class Space(SpriteImage):
    def __init__(
        self,
        fileName: str | None = None,
        relativeDir: str = "chess/data/",
        scale: int = 1,
        coord: list = [0, 0],
        number: int = 0,
    ):
        if type(self) is Space:
            raise Exception("Space class is an abstract class")
        SpriteImage.__init__(self, fileName, relativeDir, None, scale, coord)

        self.north = None
        self.south = None
        self.east = None
        self.west = None

        self.occupied = False
        self.number = number

        self.canBeReachedByAPiece: dict = {
            "black": False,
            "white": False,
        }

    @abstractmethod
    def placePiece(self, piece) -> bool:
        pass

    @abstractmethod
    def removePiece(self) -> bool:
        pass

    @abstractmethod
    def getPiece(self):
        pass

    def resetCanBeReachedByAPiece(self):
        self.canBeReachedByAPiece["black"] = False
        self.canBeReachedByAPiece["white"] = False

    def updateCanBeReachedByAPiece(self, team: Literal["black", "white"]):
        self.canBeReachedByAPiece[team] = True

    def getCanBeReachedByAPiece(self, team: Literal["black", "white"]) -> bool:
        return self.canBeReachedByAPiece[team]

    def getNumber(self) -> int:
        return self.number

    def isOccupied(self) -> bool:
        return self.occupied

    def isNowOccupied(self):
        self.occupied = True

    def isNoLongerOccupied(self):
        self.occupied = False

    def linkSpace(self, space: Space, direction: str):
        if direction == "north":
            self.north = space
        elif direction == "south":
            self.south = space
        elif direction == "east":
            self.east = space
        elif direction == "west":
            self.west = space

    def getAdjacentSpace(self, direction: str) -> Space:
        space = None
        if direction == "north":
            space = self.north
        elif direction == "south":
            space = self.south
        elif direction == "east":
            space = self.east
        elif direction == "west":
            space = self.west

        return space

    def update(self):
        super().update()
