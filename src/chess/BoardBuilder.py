from abc import ABC, abstractmethod

from .Board import Board
from .Piece import Piece
from .Player import Player
from .Tile import Tile


class BoardBuilder(ABC):
    """
    An abstract class which has the responsibility of "building" a "board" class
    """

    def __init__(self) -> None:
        if type(self) is BoardBuilder:
            raise Exception("BoardBuilder class is an abstract class")

    @abstractmethod
    def setTiles(self, tiles: list[Tile]):
        pass

    @abstractmethod
    def setPieces(self, pieces: list[Piece]):
        pass

    @abstractmethod
    def setPlayers(self, players: dict[str, Player]):
        pass

    @abstractmethod
    def setCurrentPlayer(self, player: str):
        pass


class StandardBoardBuilder(BoardBuilder):

    def __init__(self) -> None:
        super().__init__()
        self.board = None
        self.reset()

    def setTiles(self, spaces: list[Tile]):
        self.board.setTiles(spaces)

    def setPieces(self, pieces: list[Piece]):
        self.board.setPieces(pieces)

    def setPlayers(self, players: dict[str, Player]):
        self.board.setPlayers(players)

    def setCurrentPlayer(self, player: str):
        success = self.board.setCurrentPlayer(player)
        if not success:
            raise KeyError("Player doesn't exist")

    def reset(self):
        self.board = Board()

    def getBoard(self):
        board = self.board
        self.reset()
        return board
