import configparser
from math import sqrt
from typing import Type

from .Board import Board
from .BoardBuilder import BoardBuilder
from .BoardConfig import BoardConfig
from .BoardConfigSectionKeys import BoardConfigSectionKeys as cfgKeys
from .engine.constants import PLAYER_1, PLAYER_2, windowSize
from .Knight import Knight
from .Piece import TPiece
from .Player import Player
from .Rook import Rook
from .Tile import Tile

boardDistanceEdgeToCentre = windowSize[1] * 0.4
windowCentre = (windowSize[0] * 0.5, windowSize[1] * 0.5)


class Director:
    """
    The Director class has the responsibility of instantiating the necessary objects
    related to building a board. The logic of how a board is setup should be defined
    here.
    """

    def __init__(self) -> None:
        pass

    def _getTileSpriteWidth(self, lengthTiles):
        """
        Calculate how wide Tile sprites should be based on how many tiles
        there are.
        """

        sideLength = int(sqrt(lengthTiles))
        return (boardDistanceEdgeToCentre * 2) / (sideLength)

    def _resizeSprites(self, sprites, width):
        for sprite in sprites:
            sprite.resizeSprite(width)

    def _getTileCoords(self, numberOfTiles, tileWidth) -> list:
        """
        Generate tile coordinates relative to the screen size.
        """
        assert (
            numberOfTiles % sqrt(numberOfTiles) == 0
        ), f"Number of tiles is not square number. Length: {numberOfTiles}"
        sideLengthInTiles = int(sqrt(numberOfTiles))
        tileCoords = []

        x_start = windowCentre[0] - boardDistanceEdgeToCentre
        y_start = windowCentre[1] - boardDistanceEdgeToCentre

        x_coords = x_start
        y_coords = y_start

        for _y in range(0, sideLengthInTiles):
            x_coords = x_start
            for _x in range(0, sideLengthInTiles):
                tileCoords.append([x_coords, y_coords])
                x_coords += tileWidth
            y_coords += tileWidth

        return tileCoords

    def _setTileCoords(self, tiles: list[Tile]):
        """
        Set coordinates for every tile.
        """

        tileWidth = self._getTileSpriteWidth(len(tiles))
        self._resizeSprites(tiles, tileWidth)

        tileCoords = self._getTileCoords(len(tiles), tileWidth)
        tileCoords_iter = iter(tileCoords)
        for tile in tiles:
            tile.setCoord(next(tileCoords_iter))

    def _linkTiles(self, tiles: list[Tile]):
        """
        When tiles are instantiated, link each tile with its adjacent tiles
        for piece traversal.
        """
        assert (
            len(tiles) % sqrt(len(tiles)) == 0
        ), f"Number of tiles is not square number. Number {len(tiles)}"

        sideLength = int(sqrt(len(tiles)))
        numberOfTiles = len(tiles)

        def _validVerticalIndex(index, total):
            isIndexInBounds = (index >= 0) and (index < total)
            return isIndexInBounds

        def _validEastIndex(index, newIndex, total):
            sideLength = sqrt(total)
            if (index % sideLength) == sideLength - 1:
                if (newIndex % sideLength) == 0:
                    return False
            return True

        def _validWestIndex(index, newIndex, total):
            sideLength = sqrt(total)
            if (index % sideLength) == 0:
                if (newIndex % sideLength) == sideLength - 1:
                    return False
            return True

        n = numberOfTiles
        for tileIndex in range(0, n):
            northIndex = tileIndex - sideLength
            northTile = (
                tiles[northIndex] if _validVerticalIndex(northIndex, n) else None
            )

            southIndex = tileIndex + sideLength
            southTile = (
                tiles[southIndex] if _validVerticalIndex(southIndex, n) else None
            )

            eastIndex = tileIndex + 1
            eastTile = (
                tiles[eastIndex] if _validEastIndex(tileIndex, eastIndex, n) else None
            )

            westIndex = tileIndex - 1
            westTile = (
                tiles[westIndex] if _validWestIndex(tileIndex, westIndex, n) else None
            )

            tiles[tileIndex].linkSpace(northTile, "north")
            tiles[tileIndex].linkSpace(southTile, "south")
            tiles[tileIndex].linkSpace(eastTile, "east")
            tiles[tileIndex].linkSpace(westTile, "west")

    def _createTiles(self, numberOfTiles) -> list[Tile]:
        assert (
            numberOfTiles % sqrt(numberOfTiles) == 0
        ), f"Number of tiles is not square number. Number {numberOfTiles}"
        sideLength = sqrt(numberOfTiles)
        tiles = []
        colours = {
            True: "white",
            False: "black",
        }
        currentColour = False
        for tileNumber in range(0, numberOfTiles):
            if tileNumber % sideLength == 0:
                currentColour = not currentColour
            tiles.append(
                Tile(
                    fileName=colours[currentColour],
                    number=tileNumber,
                )
            )
            currentColour = not currentColour

        return tiles

    def _createKnights(self, tiles: list[Tile]) -> list[Knight]:
        knights = []

        sideLength = int(sqrt(len(tiles)))

        for i in range(0, sideLength * 2):
            knight = Knight(
                playerName=PLAYER_2,
                fileName="knight_black",
                team="black",
                objectName=f"knight_{i}",
            )
            knights.append(knight)

            knight.setSpace(tiles[i])
            knight.getSpace().placePiece(knight)

        for i in range(len(tiles) - 1, len(tiles) - sideLength * 2 - 1, -1):
            knight = Knight(
                playerName=PLAYER_1,
                fileName="knight_white",
                team="white",
                objectName=f"knight_{i}",
            )
            knight.setSpace(tiles[i])
            tiles[i].placePiece(knight)

            knights.append(knight)

        width = self._getTileSpriteWidth(len(tiles))
        self._resizeSprites(knights, width)

        for knight in knights:
            knight.setCoord(knight.getSpace().getCoord())

        for knight in knights:
            knight.findAndRememberPotentialTiles()

        return knights

    def _createPiecesFromConfig(
        self, tiles: list[Tile], pieceConfigs: list[dict]
    ) -> list[TPiece]:
        pieces: list[TPiece] = []
        for pConfig in pieceConfigs:
            pieceClass: Type[TPiece] = pConfig["class"]
            piece = pieceClass(
                playerName=pConfig["playerName"],
                fileName=pConfig["fileName"],
                team=pConfig["team"],
                objectName=pConfig["objectName"],
            )
            piece.setTimesMoved(pConfig["timesMoved"])
            piece.setClaimedPieces(pConfig["claimedPieces"])

            tileNumber: int | None = (
                pConfig["space"] if (pConfig["space"] is not None) else None
            )

            if tileNumber is not None:
                piece.setSpace(tiles[tileNumber])
                tiles[tileNumber].placePiece(piece)

            pieces.append(piece)

        width = self._getTileSpriteWidth(len(tiles))
        self._resizeSprites(pieces, width)

        for piece in pieces:
            if piece.getIsOnBoard():
                piece.setCoord(piece.getSpace().getCoord())

        for piece in pieces:
            if piece.getIsOnBoard():
                piece.findAndRememberPotentialTiles()

        return pieces

    def _createKnightsFromSaveData(
        self, tiles: list[Tile], knightsSaveData: list[dict]
    ) -> list[Knight]:
        return self._createPiecesFromSaveData(
            tiles=tiles,
            pieceClass=Knight,
            piecesSaveData=knightsSaveData,
        )

    def _createRooksFromSaveData(
        self, tiles: list[Tile], rooksSaveData: list[dict]
    ) -> list[Rook]:
        return self._createPiecesFromSaveData(
            tiles=tiles,
            pieceClass=Rook,
            piecesSaveData=rooksSaveData,
        )

    def _createPiecesFromSaveData(
        self, tiles: list[Tile], pieceClass: Type[TPiece], piecesSaveData: list[dict]
    ) -> list[TPiece]:
        pieces: list[TPiece] = []
        for pConfig in piecesSaveData:
            piece = pieceClass(
                playerName=pConfig["playerName"],
                fileName=pConfig["fileName"],
                team=pConfig["team"],
                objectName=pConfig["objectName"],
            )
            piece.setTimesMoved(pConfig["timesMoved"])
            piece.setClaimedPieces(pConfig["claimedPieces"])

            tileNumber: int | None = (
                pConfig["space"] if (pConfig["space"] is not None) else None
            )

            if tileNumber is not None:
                piece.setSpace(tiles[tileNumber])
                tiles[tileNumber].placePiece(piece)

            pieces.append(piece)

        width = self._getTileSpriteWidth(len(tiles))
        self._resizeSprites(pieces, width)

        for piece in pieces:
            if piece.getIsOnBoard():
                piece.setCoord(piece.getSpace().getCoord())

        for piece in pieces:
            if piece.getIsOnBoard():
                piece.findAndRememberPotentialTiles()

        return pieces

    def _createPlayers(self) -> dict[str, Player]:
        return {
            PLAYER_1: Player(name=PLAYER_1),
            PLAYER_2: Player(name=PLAYER_2),
        }

    def _createPlayersFromSaveData(self, playersSaveData) -> dict[str, Player]:
        playersDict = {}
        for playerConfig in playersSaveData:
            name: str = playerConfig["name"]
            player = Player(name=name)
            points: int = playerConfig["points"]
            player.incrementPoints(points=points)
            playersDict[name] = player
        return playersDict

    def _getCurrentPlayerFromSaveData(self, boardSaveData):
        boardConfig = boardSaveData[0]
        currentPlayer: str = boardConfig["currentPlayer"]
        return currentPlayer

    def createStandardBoard(self, boardBuilder: BoardBuilder):
        # self._createNewStandardBoardWithKnightsOnly(boardBuilder=boardBuilder)
        self._createNewStandardBoardFromConfig(boardBuilder=boardBuilder)

    def _createNewStandardBoardWithKnightsOnly(self, boardBuilder: BoardBuilder):
        """
        Create a standard configuration for the board with knights only.
        """
        print("_createNewStandardBoardWithKnightsOnly")
        tiles = self._createTiles(64)
        self._linkTiles(tiles)
        self._setTileCoords(tiles)

        knights = self._createKnights(tiles)

        players = self._createPlayers()

        boardBuilder.setTiles(tiles)
        boardBuilder.setPieces(knights)
        boardBuilder.setPlayers(players)

    def _createNewStandardBoardFromConfig(self, boardBuilder: BoardBuilder):
        """
        Create a standard configuration for the board.
        """
        print("_createNewStandardBoardFromConfig")
        tiles = self._createTiles(64)
        self._linkTiles(tiles)
        self._setTileCoords(tiles)

        pieceConfigs = BoardConfig.getPieceConfigs()

        pieces = self._createPiecesFromConfig(tiles, pieceConfigs)

        players = self._createPlayers()

        boardBuilder.setTiles(tiles)
        boardBuilder.setPieces(pieces)
        boardBuilder.setPlayers(players)

    def _getSectionLength(self, config, section):
        return int(config.get(section, "length"))

    def _loadSectionData(self, config, section):
        length = self._getSectionLength(config, section)
        saveData = []
        for number in range(0, int(length)):
            dictionaryStr = config.get(section, f"{number}")
            saveData.append(eval(dictionaryStr))
        return saveData

    def createStandardBoardFromSaveData(self, boardBuilder: BoardBuilder):
        print("createStandardBoardFromSaveData")
        config = configparser.RawConfigParser()
        config.read("save.cfg")

        numberOfTiles = self._getSectionLength(config, cfgKeys.TILES)
        tiles = self._createTiles(numberOfTiles)
        self._linkTiles(tiles)
        self._setTileCoords(tiles)

        knightsSaveData = self._loadSectionData(config, cfgKeys.KNIGHTS)
        knights = self._createKnightsFromSaveData(tiles, knightsSaveData)

        rooksSaveData = self._loadSectionData(config, cfgKeys.ROOKS)
        rooks = self._createRooksFromSaveData(tiles, rooksSaveData)

        playersSaveData = self._loadSectionData(config, cfgKeys.PLAYERS)
        players = self._createPlayersFromSaveData(playersSaveData)

        boardSaveData = self._loadSectionData(config, cfgKeys.BOARD)
        currentPlayer = self._getCurrentPlayerFromSaveData(boardSaveData)

        boardBuilder.setTiles(tiles)
        boardBuilder.setPieces([*knights, *rooks])
        boardBuilder.setPlayers(players)
        boardBuilder.setCurrentPlayer(currentPlayer)

    def exportSaveFile(self, board: Board):
        board.save()
