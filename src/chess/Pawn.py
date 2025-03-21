from typing import Literal

from .Piece import Piece
from .Space import Space


class Pawn(Piece):
    def __init__(
        self,
        fileName: str = "pawn_white",
        relativeDir: str = "chess/data/piece/",
        scale: int = 0.47,
        coord: list = [0, 0],
        playerName: str = "defaultPlayerName",
        objectName: str = "defaultPieceName",
        space: Space | None = None,
        team: Literal["black", "white"] = "default",
    ):
        Piece.__init__(
            self=self,
            fileName=fileName,
            relativeDir=relativeDir,
            scale=scale,
            coord=coord,
            playerName=playerName,
            objectName=objectName,
            space=space,
            team=team,
        )

        self._homeSpace = None

    def setHomeSpace(self, homeSpace: Space) -> bool:
        self._homeSpace = homeSpace

    def getPointsValue(self) -> int:
        return 1

    def findAndRememberPotentialTiles(self):
        potentialSpaces: list[Space] = []
        normalPathBeginning = {
            "black": [
                ["south", "south"],
            ],
            "white": [
                ["north", "north"],
            ],
        }
        normalPath = {
            "black": [
                ["south"],
            ],
            "white": [
                ["north"],
            ],
        }
        attackPath = {
            "black": [
                ["south", "east"],
                ["south", "west"],
            ],
            "white": [
                ["north", "east"],
                ["north", "west"],
            ],
        }

        if self._homeSpace is self.getSpace():
            for path in normalPathBeginning[self.getTeam()]:
                space = self.getSpace()
                for direction in path:
                    space = space.getAdjacentSpace(direction)
                    if space is None:
                        break
                if space is not None:
                    if space.isOccupied():
                        break
                    else:
                        potentialSpaces.append(space)

        for path in normalPath[self.getTeam()]:
            space = self.getSpace()
            for direction in path:
                space = space.getAdjacentSpace(direction)
                if space is None:
                    break
            if space is not None:
                if space.isOccupied():
                    break
                else:
                    potentialSpaces.append(space)

        for path in attackPath[self.getTeam()]:
            space = self.getSpace()
            for direction in path:
                space = space.getAdjacentSpace(direction)
                if space is None:
                    break
            if space is not None:
                space.updateCanBeReachedByAPiece(self.getTeam())
                if space.isOccupied():
                    otherPiece: Piece = space.getPiece()
                    if otherPiece.getTeam() != self.getTeam():
                        potentialSpaces.append(space)

        self.potentialSpaces = potentialSpaces

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
            "homeSpace": self._homeSpace.getNumber(),
        }
        # config.set("knights", f"{kwargs['number']}", pieceState)
        config.set(
            str(type(self).__name__).lower() + "s", f"{kwargs['number']}", pieceState
        )
