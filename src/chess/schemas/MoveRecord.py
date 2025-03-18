from typing import Optional

from ..Piece import TPiece
from ..Tile import Tile


class MoveRecord:
    def __init__(self, **kwargs):
        self.piece: TPiece = kwargs["piece"]
        self.otherPiece: Optional[TPiece] = kwargs["otherPiece"]
        self.oldSpace: Tile = kwargs["oldSpace"]
        self.newSpace: Tile = kwargs["newSpace"]
