from abc import ABC, abstractmethod

import pygame as pg

from .BoardBuilder import StandardBoardBuilder
from .Button import Button
from .ButtonDirector import ButtonDirector
from .Director import Director
from .engine.BackgroundSet import GameBackground, StartingBackground
from .engine.constants import windowSize
from .engine.CurrentPlayerSurface import (
    CurrentPlayerSurfaceInstance,
    PlayerOnePointsInstance,
    PlayerTwoPointsInstance,
)
from .engine.Display import DisplayInstance
from .engine.EventManager import EventManagerInstance, Events
from .engine.Notification import NotificationInstance
from .engine.SpriteGroup import SpriteGroup
from .Piece import Piece
from .Tile import Tile
from .TriggerKey import TriggerKey
from .Turn import (
    IsBoardInCheckMateTurn,
    MovePieceCheckTurn,
    MovePieceTurn,
    SelectPieceTurn,
    UndoTurn,
)


class State(ABC):
    def __init__(self):
        if type(self) is State:
            raise Exception("State class is an abstract class")

    @abstractmethod
    def initialise(self):
        pass

    @abstractmethod
    def run(self) -> bool:
        pass


class InitialiseState(State):

    screen = None
    clock = None
    background = None
    boardBuilder = None
    director: Director = None
    buttonDirector: ButtonDirector = None
    eventManager = None
    notification = None
    playerOneSurface = None
    playerTwoSurface = None
    currentPlayerSurface = None
    playerSurfacesDict = None
    display = None
    playingBackground = None
    startScreenBackground = None
    loadFromSave = None
    board = None
    gameSprites = None
    startScreenSprites = None
    selectPieceTurn = None
    movePieceTurn = None
    isBoardInCheckMateTurn = None
    movePieceCheckTurn = None
    undoTurn = None
    isInCheck = False

    updateTheDisplay = True

    @staticmethod
    def initialise():
        s = InitialiseState

        pg.init()
        s.screen = pg.display.set_mode(windowSize)
        s.clock = pg.time.Clock()
        pg.display.set_caption("Knight Chess")
        s.background = pg.Surface(s.screen.get_size())
        s.background = s.background.convert()
        s.background.fill((0, 99, 0))

        s.boardBuilder = StandardBoardBuilder()
        s.director = Director()

        s.eventManager = EventManagerInstance.getInstance()

        s.notification = NotificationInstance.getInstance()
        s.notification.setup(pg.font.Font)

        s.playerOneSurface = PlayerOnePointsInstance.getInstance()
        s.playerOneSurface.setup(pg.font.Font)

        s.playerTwoSurface = PlayerTwoPointsInstance.getInstance()
        s.playerTwoSurface.setup(pg.font.Font)

        s.currentPlayerSurface = CurrentPlayerSurfaceInstance.getInstance()
        s.currentPlayerSurface.setup(pg.font.Font)

        s.playerSurfacesDict = {
            s.playerOneSurface.getPlayerName(): s.playerOneSurface,
            s.playerTwoSurface.getPlayerName(): s.playerTwoSurface,
        }

        # Display class to handle display updates per tick
        s.display = DisplayInstance.getInstance()
        s.display.setup(
            screen=s.screen, backgroundSet=None, background=s.background, sprites=None
        )

        s.playingBackground = GameBackground(s.background)
        s.startScreenBackground = StartingBackground(s.background)

        s.buttonDirector = ButtonDirector()
        s.startScreenSprites = SpriteGroup(
            [
                *s.buttonDirector.createStartButtons(),
            ]
        )

        s.boardBuilder.reset()
        s.loadFromSave = False

    @staticmethod
    def run():
        raise Exception("InitialiseState run() not implemented")


class GameRunningState(InitialiseState):

    @staticmethod
    def initialise():
        raise Exception("GameRunningState initialise() not implemented")

    @staticmethod
    def run() -> dict:
        s = GameRunningState
        s.display.setBackgroundSet(s.playingBackground.getSet())
        s.display.setBackground(s.playingBackground.getBackground())
        s.display.setSprites(s.gameSprites)
        if s.updateTheDisplay:
            s.display.updateDisplay()
        s.display.clear()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                s.director.exportSaveFile(s.board)
                return {
                    "quit": True,
                    "nextState": None,
                }
            if event.type == pg.MOUSEBUTTONDOWN:
                pos = pg.mouse.get_pos()
                clickedSprites = [
                    spr for spr in s.display.getSprites() if spr.rect.collidepoint(pos)
                ]
                for sprite in clickedSprites:
                    if isinstance(sprite, Piece):
                        s.selectPieceTurn.execute(sprite)
                    elif isinstance(sprite, Tile):
                        if s.isInCheck:
                            print("movePieceCheckTurn")
                            s.movePieceCheckTurn.execute(sprite)
                        else:
                            print("movePieceTurn")
                            s.movePieceTurn.execute(sprite)

            if event.type == pg.MOUSEBUTTONUP:
                pos = pg.mouse.get_pos()
                clickedSprites = [
                    spr for spr in s.display.getSprites() if spr.rect.collidepoint(pos)
                ]
                for sprite in clickedSprites:
                    if isinstance(sprite, Button):
                        s.undoTurn.execute()

            if event.type == Events.TAKE_PIECE_EVENT:
                print("Events.TAKE_PIECE_EVENT")
                playerName = event.dict.get("playerName")
                points = event.dict.get("points")
                s.playerSurfacesDict[playerName].incrementPoints(points)
                s.display.clear()

            if event.type == Events.CHANGE_PLAYER_EVENT:
                print("Events.CHANGE_PLAYER_EVENT")
                s.currentPlayerSurface.setCurrentPlayer(
                    s.board.getCurrentPlayer().getName()
                )
            if event.type == Events.CHECK_EVENT:
                print("Events.CHECK_EVENT")
                s.isInCheck = True
                s.isBoardInCheckMateTurn.execute()
                s.notification.push("Check!")

            if event.type == Events.STOP_CHECK_EVENT:
                print("Events.STOP_CHECK_EVENT")
                s.isInCheck = False

            if event.type == Events.UNDO_MOVE_EVENT:
                print("Events.UNDO_MOVE_EVENT")
                s.gameSprites.addSprites([event.dict.get("otherPiece")])
                playerName = event.dict.get("playerName")
                points: int = event.dict.get("points")
                s.playerSurfacesDict[playerName].incrementPoints(-points)

            if event.type == Events.FREEZE_DISPLAY_EVENT:
                print("Events.FREEZE_DISPLAY_EVENT")
                s.updateTheDisplay = False

            if event.type == Events.STOP_FREEZE_DISPLAY_EVENT:
                print("Events.STOP_FREEZE_DISPLAY_EVENT")
                s.updateTheDisplay = True

        s.clock.tick(60)
        s.eventManager.listen()

        return {
            "quit": False,
            "nextState": GameRunningState,
        }


class NewScreenState(InitialiseState):

    @staticmethod
    def initialise():
        raise Exception("NewScreenState initialise() not implemented")

    @staticmethod
    def run() -> dict:
        s = GameRunningState
        s.display.setBackgroundSet(s.startScreenBackground.getSet())
        s.display.setBackground(s.startScreenBackground.getBackground())
        s.display.setSprites(s.startScreenSprites)
        s.display.updateDisplay()
        s.display.clear()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                return {
                    "quit": True,
                    "nextState": None,
                }
            if event.type == pg.MOUSEBUTTONDOWN:
                pos = pg.mouse.get_pos()
                clickedSprites = [
                    spr for spr in s.display.getSprites() if spr.rect.collidepoint(pos)
                ]
                for sprite in clickedSprites:
                    if isinstance(sprite, Button):
                        s.notification.clear()

                        # New game
                        if sprite.getFileName() == TriggerKey.NEW:
                            s.notification.push("Creating new game...")
                            s.director.createStandardBoard(s.boardBuilder)

                        # Load game
                        elif (
                            sprite.getFileName() == TriggerKey.LOAD
                            and sprite.isEnabled()
                        ):
                            s.notification.push("Loading save...")

                            s.director.createStandardBoardFromSaveData(s.boardBuilder)
                            s.loadFromSave = True

                        # If no save file exists
                        elif (
                            sprite.getFileName() == TriggerKey.LOAD
                            and not sprite.isEnabled()
                        ):
                            return {
                                "quit": False,
                                "nextState": NewScreenState,
                            }

                        s.board = s.boardBuilder.getBoard()

                        s.gameSprites = SpriteGroup(
                            [
                                *s.board.getTiles(),
                                *s.board.getPieces(),
                                *s.buttonDirector.createUndoButton(),
                            ]
                        )

                        # print(f"Number of knights: {len(s.board.getKnights())}")
                        # print([str(knight) for knight in s.board.getKnights()])

                        # print(f"Number of rooks: {len(s.board.getRooks())}")
                        # print([str(rook) for rook in s.board.getRooks()])

                        # print(f"Number of pawns: {len(s.board.getPawns())}")
                        # print([str(pawn) for pawn in s.board.getPawns()])

                        # print(f"Number of bishops: {len(s.board.getBishops())}")
                        # print([str(bishop) for bishop in s.board.getBishops()])

                        # print(f"Number of queens: {len(s.board.getQueens())}")
                        # print([str(queen) for queen in s.board.getQueens()])

                        # print(f"Number of kings: {len(s.board.getKings())}")
                        # print([str(king) for king in s.board.getKings()])

                        s.currentPlayerSurface.setCurrentPlayer(
                            s.board.getCurrentPlayer().getName()
                        )

                        s.selectPieceTurn = SelectPieceTurn(s.board)
                        s.movePieceTurn = MovePieceTurn(s.board)
                        s.isBoardInCheckMateTurn = IsBoardInCheckMateTurn(s.board)
                        s.movePieceCheckTurn = MovePieceCheckTurn(s.board)
                        s.undoTurn = UndoTurn(s.board)

                        if s.loadFromSave:
                            for player in s.board.getPlayers():
                                s.playerSurfacesDict[player.getName()].incrementPoints(
                                    player.getPoints()
                                )
                            for piece in s.board.getPieces():
                                if not piece.getIsOnBoard():
                                    piece.kill()
                            s.board.setIsCheck(s.board.checkIsThereCheck())
                            if s.board.isInCheck():
                                s.eventManager.post(event=Events.CHECK_EVENT)

                        s.notification.push("Starting game!")

                        return {
                            "quit": False,
                            "nextState": GameRunningState,
                        }

        s.clock.tick(60)
        s.eventManager.listen()

        return {
            "quit": False,
            "nextState": NewScreenState,
        }
