from typing import Literal

from .Piece import Piece
from .Space import Space


class Knight(Piece):
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

    def getPointsValue(self) -> int:
        return 3

    def findAndRememberPotentialTiles(self):
        paths = [
            ["north", "north", "east"],
            ["north", "north", "west"],
            ["south", "south", "east"],
            ["south", "south", "west"],
            ["west", "west", "north"],
            ["west", "west", "south"],
            ["east", "east", "north"],
            ["east", "east", "south"],
        ]
        potentialSpaces: list[Space] = []
        if self.getIsOnBoard():
            for path in paths:
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
                    else:
                        potentialSpaces.append(space)

        self.potentialSpaces = potentialSpaces
