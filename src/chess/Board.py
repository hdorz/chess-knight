from typing import Type

from .Bishop import Bishop
from .constants.BoardConfigSectionKeys import BoardConfigSectionKeys as cfgKeys
from .engine.SaveLoadMixin import SaveLoadMixin
from .King import King
from .Knight import Knight
from .Pawn import Pawn
from .Piece import Piece, TPiece
from .Player import Player
from .Queen import Queen
from .Rook import Rook
from .schemas.MoveRecord import MoveRecord
from .Tile import Tile


class Board(SaveLoadMixin):
    def __init__(self, players: dict[str, Player] | None = None) -> None:
        self.tiles = None
        self.pieces = None
        self.gameWon: bool = False
        self.selectedPiece = None
        self.selectedTile = None
        self._currentPlayerIndex: int = 0
        self.currentPlayer: Player | None = None
        self.players: dict[str, Player] | None = players
        self.checkmate: bool = False
        self.moveStack: list = []

    def setMoveStack(self, moveStack: list[dict]):
        for index in range(0, len(moveStack)):
            self.moveStack.append(MoveRecord(**moveStack[index]))

    def addMoveToMoveStack(self, moveDict: dict):
        self.moveStack.append(MoveRecord(**moveDict))

    def popMoveFromMoveStack(self) -> MoveRecord:
        if self.moveStack:
            return self.moveStack.pop(-1)

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

    def selectPiece(self, piece: TPiece):
        self.selectedPiece = piece
        self.selectedPiece.highlight()

    def deselectPiece(self):
        if self.selectedPiece is not None:
            self.selectedPiece.stopHighlight()
            self.selectedPiece.highlightTiles(highlight=False)
            self.selectedPiece = None

    def getSelectedPiece(self) -> Knight:
        return self.selectedPiece

    def getPieces(self) -> list[Piece]:
        return self.pieces

    def getPiecesOnBoard(self) -> list[Piece]:
        return [piece for piece in self.pieces if piece.getIsOnBoard()]

    def getCurrentPlayersPiecesOnBoard(self) -> list[Piece]:
        return [
            piece
            for piece in self.pieces
            if piece.getPlayerName() == self.getCurrentPlayer().getName()
            and piece.getIsOnBoard()
        ]

    def setPieces(self, pieces: list[Piece]):
        self.pieces = pieces

    def makeAllPiecesFindPotentialTiles(self):
        for tile in self.tiles:
            tile.resetCanBeReachedByAPiece()
        piecesOnBoard = self.filterForPiecesOnBoard(self._getPiecesNotThisType(King))
        for piece in piecesOnBoard:
            piece.findAndRememberPotentialTiles()
        for _repeat in range(0, 2):
            for king in self.getKings():
                king.findAndRememberPotentialTiles()

    def getCurrentPlayersKing(self) -> King:
        kings: list[King] = self.getKings()
        king: King = [
            king
            for king in kings
            if king.getPlayerName() == self.getCurrentPlayer().getName()
        ][0]
        return king

    def checkIsThereCheck(self):
        # to follow after calling makeAllPiecesFindPotentialTiles()
        # and changeCurrentPlayer()
        king = self.getCurrentPlayersKing()
        return king.getSpace().getCanBeReachedByAPiece(king.getOpponentTeam())

    def isInCheck(self) -> bool:
        return self.checkmate

    def setIsCheck(self, checkmate: bool):
        self.checkmate = checkmate

    def getKnights(self) -> list[Knight]:
        return self._getPiecesByType(Knight)

    def getRooks(self) -> list[Rook]:
        return self._getPiecesByType(Rook)

    def getPawns(self) -> list[Pawn]:
        return self._getPiecesByType(Pawn)

    def getBishops(self) -> list[Bishop]:
        return self._getPiecesByType(Bishop)

    def getQueens(self) -> list[Queen]:
        return self._getPiecesByType(Queen)

    def getKings(self) -> list[King]:
        return self._getPiecesByType(King)

    def filterForPiecesOnBoard(self, pieces: list[TPiece]):
        return [piece for piece in pieces if piece.getIsOnBoard()]

    def _getPiecesByType(self, pieceClass: Type[TPiece]) -> list[TPiece]:
        return [
            piece
            for piece in self.pieces
            if type(piece).__name__ == pieceClass.__name__
        ]

    def _getPiecesNotThisType(self, pieceClass: Type[TPiece]) -> list[TPiece]:
        return [
            piece
            for piece in self.pieces
            if type(piece).__name__ != pieceClass.__name__
        ]

    def getTiles(self):
        return self.tiles

    def setTiles(self, tiles: list[Tile]):
        self.tiles = tiles

    def highlightPotentialTiles(self):
        if self.isAPieceSelected():
            self.selectedPiece.highlightTiles(highlight=True)

    def areAnyTilesHighlighted(self) -> bool:
        for tile in self.tiles:
            if tile.isHighlighted():
                return True
        return False

    def setPlayers(self, players: dict[str, Player]):
        self.players = players
        self.setCurrentPlayer([p for p in players.keys()][0])

    def getPlayers(self) -> list[Player]:
        if self.players is not None:
            return [p for p in self.players.values()]

    def getCurrentPlayer(self) -> Player:
        return self.currentPlayer

    def getOtherPlayer(self) -> Player:
        players = [p for p in self.players.values()]
        numberOfPlayers = len(players)
        otherPlayerIndex = (self._currentPlayerIndex + 1) % numberOfPlayers
        return players[otherPlayerIndex]

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
            cfgKeys.QUEENS,
            cfgKeys.KINGS,
            cfgKeys.PLAYERS,
            cfgKeys.BOARD,
            cfgKeys.MOVES,
        ]
        for section in sections:
            if config.has_section(section):
                config.remove_section(section)
            config.add_section(section)

        knights: list[Knight] = self.getKnights()
        rooks: list[Rook] = self.getRooks()
        pawns: list[Pawn] = self.getPawns()
        bishops: list[Bishop] = self.getBishops()
        queens: list[Queen] = self.getQueens()
        kings: list[King] = self.getKings()

        config.set(cfgKeys.TILES, "length", len(self.tiles))
        config.set(cfgKeys.KNIGHTS, "length", len(knights))
        config.set(cfgKeys.ROOKS, "length", len(rooks))
        config.set(cfgKeys.PAWNS, "length", len(pawns))
        config.set(cfgKeys.BISHOPS, "length", len(bishops))
        config.set(cfgKeys.QUEENS, "length", len(queens))
        config.set(cfgKeys.KINGS, "length", len(kings))
        config.set(cfgKeys.PLAYERS, "length", len(self.players.values()))
        config.set(cfgKeys.BOARD, "length", 1)
        config.set(cfgKeys.MOVES, "length", len(self.moveStack))

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
        for number in range(0, len(queens)):
            queens[number].save(number=number)
        for number in range(0, len(kings)):
            kings[number].save(number=number)

        for number in range(0, len(self.players.values())):
            [p for p in self.players.values()][number].save(number=number)

        for number in range(0, len(self.moveStack)):
            move: MoveRecord = self.moveStack[number]
            moveRecordState = {
                "piece": move.piece.getObjectName(),
                "otherPiece": (
                    move.otherPiece.getObjectName()
                    if move.otherPiece is not None
                    else None
                ),
                "oldSpace": move.oldSpace.getNumber(),
                "newSpace": move.newSpace.getNumber(),
            }
            config.set(cfgKeys.MOVES, f"{number}", moveRecordState)

        with open("save.cfg", "w") as configFile:
            config.write(configFile)
