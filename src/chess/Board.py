from typing import Type

from .Bishop import Bishop
from .BoardConfigSectionKeys import BoardConfigSectionKeys as cfgKeys
from .engine.SaveLoadMixin import SaveLoadMixin
from .Knight import Knight
from .Pawn import Pawn
from .Piece import Piece, TPiece
from .Player import Player
from .Rook import Rook
from .Tile import Tile


class Board(SaveLoadMixin):
    def __init__(self, players: dict[str, Player] | None = None) -> None:
        self.tiles = None
        self.pieces = None
        self.gameWon = False
        self.selectedPiece = None
        self.selectedTile = None
        self._currentPlayerIndex: int = 0
        self.currentPlayer: Player | None = None
        self.players: dict[str, Player] | None = players

    def isATileSelected(self) -> bool:
        if self.selectedTile is not None:
            return True
        return False

    def selectTile(self, tile: Tile):
        self.selectedTile = tile

    def deselectTile(self):
        self.selectedTile = None

    def isAPieceSelected(self) -> bool:
        if self.selectedPiece is not None:
            return True
        return False

    def selectPiece(self, knight: Knight):
        self.selectedPiece = knight
        self.selectedPiece.highlight()

    def deselectPiece(self):
        self.selectedPiece.stopHighlight()
        self.selectedPiece.highlightTiles(highlight=False)
        self.selectedPiece = None

    def getSelectedPiece(self) -> Knight:
        return self.selectedPiece

    def getPieces(self) -> list[Piece]:
        return self.pieces

    def setPieces(self, pieces: list[Piece]):
        self.pieces = pieces

    def getKnights(self) -> list[Knight]:
        return self._getPiecesByType(Knight)

    def getRooks(self) -> list[Rook]:
        return self._getPiecesByType(Rook)

    def getPawns(self) -> list[Pawn]:
        return self._getPiecesByType(Pawn)

    def getBishops(self) -> list[Bishop]:
        return self._getPiecesByType(Bishop)

    def _getPiecesByType(self, pieceClass: Type[TPiece]) -> list[TPiece]:
        return [
            piece
            for piece in self.pieces
            if type(piece).__name__ == pieceClass.__name__
        ]

    def getTiles(self):
        return self.tiles

    def setTiles(self, tiles: list[Tile]):
        self.tiles = tiles

    def highlightPotentialTiles(self):
        if self.isAPieceSelected():
            self.selectedPiece.highlightTiles(highlight=True)

    def setPlayers(self, players: dict[str, Player]):
        self.players = players
        self.setCurrentPlayer([p for p in players.keys()][0])

    def getPlayers(self) -> list[Player]:
        if self.players is not None:
            return [p for p in self.players.values()]

    def getCurrentPlayer(self) -> Player:
        return self.currentPlayer

    def setCurrentPlayer(self, player: str) -> bool:
        if self.players is not None:
            if player in self.players.keys():
                self.currentPlayer = self.players[player]
                self._currentPlayerIndex = [p for p in self.players.keys()].index(
                    player
                )
                return True
        return False

    def changeCurrentPlayer(self):
        players = [p for p in self.players.values()]
        numberOfPlayers = len(players)
        self._currentPlayerIndex = (self._currentPlayerIndex + 1) % numberOfPlayers
        self.currentPlayer = players[self._currentPlayerIndex]

    def save(self, **kwargs):
        config = self.getParser()

        sections = [
            cfgKeys.TILES,
            cfgKeys.KNIGHTS,
            cfgKeys.ROOKS,
            cfgKeys.PAWNS,
            cfgKeys.BISHOPS,
            cfgKeys.PLAYERS,
            cfgKeys.BOARD,
        ]
        for section in sections:
            if config.has_section(section):
                config.remove_section(section)
            config.add_section(section)

        knights: list[Knight] = self.getKnights()
        rooks: list[Rook] = self.getRooks()
        pawns: list[Pawn] = self.getPawns()
        bishops: list[Bishop] = self.getBishops()

        config.set(cfgKeys.TILES, "length", len(self.tiles))
        config.set(cfgKeys.KNIGHTS, "length", len(knights))
        config.set(cfgKeys.ROOKS, "length", len(rooks))
        config.set(cfgKeys.PAWNS, "length", len(pawns))
        config.set(cfgKeys.BISHOPS, "length", len(bishops))
        config.set(cfgKeys.PLAYERS, "length", len(self.players.values()))
        config.set(cfgKeys.BOARD, "length", 1)

        boardState = {"currentPlayer": str(self.getCurrentPlayer().getName())}
        config.set(cfgKeys.BOARD, "0", boardState)

        for number in range(0, len(knights)):
            knights[number].save(number=number)
        for number in range(0, len(rooks)):
            rooks[number].save(number=number)
        for number in range(0, len(pawns)):
            pawns[number].save(number=number)
        for number in range(0, len(bishops)):
            bishops[number].save(number=number)

        for number in range(0, len(self.players.values())):
            [p for p in self.players.values()][number].save(number=number)

        with open("save.cfg", "w") as configFile:
            config.write(configFile)
