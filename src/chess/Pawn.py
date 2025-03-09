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
        team: str = "default",
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

    def setSpace(self, newSpace: Space) -> bool:
        onBoard = self.getIsOnBoard()
        # if false, then piece not placed on board yet
        # so first placement on a space is home space
        success = super().setSpace(newSpace=newSpace)
        if success and not onBoard and self.timesMoved == 0:
            self._homeSpace = self.getSpace()

        return success

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
                if space.isOccupied():
                    otherPiece: Piece = space.getPiece()
                    if otherPiece.getTeam() != self.getTeam():
                        potentialSpaces.append(space)

        self.potentialSpaces = potentialSpaces

    def highlightTiles(self, highlight: bool = False):
        self.findAndRememberPotentialTiles()
        for space in self.potentialSpaces:
            if highlight:
                space.highlight()
            else:
                space.stopHighlight()
