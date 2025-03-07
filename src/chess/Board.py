from .engine.SaveLoadMixin import SaveLoadMixin
from .Knight import Knight
from .Player import Player
from .Tile import Tile


class Board(SaveLoadMixin):
    def __init__(self, players: dict[str, Player] | None = None) -> None:
        self.tiles = None
        self.knights = None
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

    def deselectPiece(self):
        self.selectedPiece.findTiles(highlight=False)
        self.selectedPiece = None

    def getSelectedPiece(self) -> Knight:
        return self.selectedPiece

    def getKnights(self):
        return self.knights

    def setKnights(self, knights: list[Knight]):
        self.knights = knights

    def getTiles(self):
        return self.tiles

    def setTiles(self, tiles: list[Tile]):
        self.tiles = tiles

    def highlightPotentialTiles(self):
        if self.isAPieceSelected():
            self.selectedPiece.findTiles(highlight=True)

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

        sections = ["tiles", "knights", "players", "board"]
        for section in sections:
            if config.has_section(section):
                config.remove_section(section)
            config.add_section(section)

        config.set("tiles", "length", len(self.tiles))
        config.set("knights", "length", len(self.knights))
        config.set("players", "length", len(self.players.values()))
        config.set("board", "length", 1)

        boardState = {"currentPlayer": str(self.getCurrentPlayer().getName())}
        config.set("board", "0", boardState)

        for number in range(0, len(self.knights)):
            self.knights[number].save(number=number)

        for number in range(0, len(self.players.values())):
            [p for p in self.players.values()][number].save(number=number)

        with open("save.cfg", "w") as configFile:
            config.write(configFile)
