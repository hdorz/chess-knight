from __future__ import annotations

from abc import abstractmethod

from .engine.SpriteImage import SpriteImage
from .Space import Space


class Piece(SpriteImage):
    def __init__(
        self,
        fileName: str = "knight_white",
        relativeDir: str = "chess/data/piece/",
        scale: int = 0.47,
        coord: list = [0, 0],
        playerName: str = "defaultPlayerName",
        objectName: str = "defaultPieceName",
        space: Space | None = None,
        team: str = "default",
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

        self.type = "defaultPiece"

    @abstractmethod
    def findTiles(self, highlight: bool = False):
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
        return self.objectName

    def getfileName(self):
        return self.fileName

    def getSpace(self):
        return self.space

    def setSpace(self, newSpace: Space) -> bool:
        if not newSpace.isOccupied():
            self.isOnBoard = True
            self.space = newSpace
            return True
        return False

    def getTeam(self) -> str:
        return self.team

    def takeOffBoard(self) -> bool:
        self.isOnBoard = False

    def update(self):
        super().update()

    def move(self, newSpace: Space) -> bool:
        if newSpace.isHighlighted():
            if not newSpace.isOccupied():
                self.findTiles(highlight=False)

                self.getSpace().removePiece()

                self.setSpace(newSpace)
                newSpace.placePiece(self)
                self.updatePosition(self.getSpace().getCoord())
            else:
                oldPiece: Piece = newSpace.getPiece()

                if oldPiece.getTeam() == self.getTeam():
                    return False

                oldPiece.takeOffBoard()
                oldPiece.kill()

                self.findTiles(highlight=False)

                newSpace.removePiece()
                self.getSpace().removePiece()

                self.setSpace(newSpace)
                newSpace.placePiece(self)

                self.updatePosition(self.getSpace().getCoord())

                self.claimedPieces += 1
                self.timesMoved += 1

            return True
        return False
