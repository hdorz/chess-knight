from __future__ import annotations

from .Piece import Piece
from .Space import Space


class Tile(Space):
    def __init__(
        self,
        fileName: str | None = None,
        relativeDir: str = "chess/data/tile/",
        coord: list = [0, 0],
        scale=1,
        number: int = 0,
    ):
        if fileName is None:
            fileName = "black"
        Space.__init__(self, fileName, relativeDir, scale, coord, number)

        self.colour = fileName
        self.piece = None

    def placePiece(self, piece: Piece) -> bool:
        if not self.isOccupied() and self.piece is None:
            self.piece = piece
            self.isNowOccupied()
            return True
        return False

    def removePiece(self) -> bool:
        self.piece = None
        self.isNoLongerOccupied()
        return True

    def getPiece(self) -> Piece:
        return self.piece
