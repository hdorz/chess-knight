from __future__ import annotations

from abc import abstractmethod
from typing import Literal, TypeVar

from .engine.SaveLoadMixin import SaveLoadMixin
from .engine.SpriteImage import SpriteImage
from .Space import Space


class Piece(SpriteImage, SaveLoadMixin):
    def __init__(
        self,
        fileName: str = "knight_white",
        relativeDir: str = "chess/data/piece/",
        scale: int = 0.47,
        coord: list = [0, 0],
        playerName: str = "defaultPlayerName",
        objectName: str = "defaultPieceName",
        space: Space | None = None,
        team: Literal["black", "white"] = "default",
    ):
        if type(self) is Piece:
            raise Exception("Piece class is an abstract class")

        self._layer = 3
        SpriteImage.__init__(self, fileName, relativeDir, -1, scale, coord)
        self.objectName = objectName
        self.playerName = playerName
        self.space = None
        self.team = team

        self.timesMoved = 0
        self.claimedPieces = 0

        self.message = ""
        self.isOnBoard = False

        if space is not None:
            self.setSpace(space)

        self.movementSpeed = 30

        self.type: str = type(self).__name__
        self.potentialSpaces: list[Space] | None = None

        self.opponentTeam = ""
        if self.team == "black":
            self.opponentTeam = "white"
        elif self.team == "white":
            self.opponentTeam = "black"

    def __str__(self):
        return self.objectName

    @abstractmethod
    def getPointsValue(self) -> int:
        pass

    @abstractmethod
    def findAndRememberPotentialTiles(self):
        pass

    @abstractmethod
    def highlightTiles(self, highlight: bool = False):
        pass

    def setTimesMoved(self, timesMoved: int):
        self.timesMoved = timesMoved

    def setClaimedPieces(self, numOfClaimedPieces: int):
        self.claimedPieces = numOfClaimedPieces

    def getIsOnBoard(self) -> bool:
        return self.isOnBoard

    def getPlayerName(self):
        return self.playerName

    def getObjectName(self):
        return f"{self.objectName} ({self.team})"

    def getfileName(self):
        return self.fileName

    def getSpace(self) -> Space | None:
        return self.space

    def getPotentialSpaces(self) -> list[Space]:
        return self.potentialSpaces

    def setSpace(self, newSpace: Space) -> bool:
        if not newSpace.isOccupied():
            self.isOnBoard = True
            self.space = newSpace
            self.findAndRememberPotentialTiles()
            return True
        return False

    def getTeam(self) -> Literal["black", "white"]:
        return self.team

    def getOpponentTeam(self) -> Literal["black", "white"]:
        return self.opponentTeam

    def takeOffBoard(self) -> bool:
        self.isOnBoard = False

    def update(self):
        super().update()

    def move(self, newSpace: Space) -> bool:
        if newSpace.isHighlighted():
            if not newSpace.isOccupied():
                self.highlightTiles(highlight=False)

                # remove piece from space
                self.getSpace().removePiece()

                # place piece on new space
                self.setSpace(newSpace)
                newSpace.placePiece(self)

                self.updatePosition(self.getSpace().getCoord())
            else:
                oldPiece: Piece = newSpace.getPiece()

                if oldPiece.getTeam() == self.getTeam():
                    return False

                oldPiece.takeOffBoard()
                oldPiece.kill()

                self.highlightTiles(highlight=False)

                # remove pieces from spaces
                newSpace.removePiece()
                self.getSpace().removePiece()

                # place piece on new space
                self.setSpace(newSpace)
                newSpace.placePiece(self)

                self.updatePosition(self.getSpace().getCoord())

                self.claimedPieces += 1

            self.timesMoved += 1
            return True
        return False

    def save(self, **kwargs):
        config = self.getParser()
        pieceState = {
            "fileName": self.fileName,
            "playerName": self.playerName,
            "objectName": self.objectName,
            "space": (
                self.space.getNumber()
                if (self.space is not None and self.isOnBoard)
                else None
            ),
            "team": self.team,
            "timesMoved": self.timesMoved,
            "claimedPieces": self.claimedPieces,
            "isOnBoard": self.isOnBoard,
        }
        # config.set("knights", f"{kwargs['number']}", pieceState)
        config.set(
            str(type(self).__name__).lower() + "s", f"{kwargs['number']}", pieceState
        )


TPiece = TypeVar("TPiece", bound=Piece)
