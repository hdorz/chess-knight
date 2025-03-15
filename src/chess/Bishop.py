from .Piece import Piece
from .Space import Space


class Bishop(Piece):
    def __init__(
        self,
        fileName: str = "bishop_white",
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

    def getPointsValue(self) -> int:
        return 3

    def findAndRememberPotentialTiles(self):
        paths = [
            ["north", "east"],
            ["north", "west"],
            ["south", "east"],
            ["south", "west"],
        ]
        potentialSpaces: list[Space] = []
        for path in paths:
            space = self.getSpace()
            while space is not None:
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
                        break
                    else:
                        potentialSpaces.append(space)

        self.potentialSpaces = potentialSpaces

    def highlightTiles(self, highlight: bool = False):
        for space in self.potentialSpaces:
            if highlight:
                space.highlight()
            else:
                space.stopHighlight()
