import time
from abc import ABC, abstractmethod

from .Board import Board
from .engine.EventManager import EventManagerInstance, Events
from .engine.Notification import NotificationInstance
from .Piece import Piece
from .Space import Space

notification = NotificationInstance.getInstance()
eventManager = EventManagerInstance.getInstance()


class Turn(ABC):
    """
    Turn class defines an atomic step in the game. It defines how the game should
    progress during a turn.
    """

    def __init__(self, board: Board) -> None:
        if type(self) is Turn:
            raise Exception("Turn class is an abstract class")
        self.board = board

    @abstractmethod
    def execute(self):
        pass


class SelectPieceTurn(Turn):

    def __init__(self, board: Board) -> None:
        super().__init__(board)

    def execute(self, piece: Piece) -> bool:
        if not self.board.isAPieceSelected():
            if piece.getPlayerName() == self.board.getCurrentPlayer().getName():
                if piece.getIsOnBoard():
                    self.board.selectPiece(piece)
                    self.board.highlightPotentialTiles()
                    notification.push(f"{piece.getObjectName()} selected")

        elif piece is self.board.getSelectedPiece():
            self.board.deselectPiece()
            notification.push(f"{piece.getObjectName()} deselected")


class MovePieceTurn(Turn):

    def __init__(self, board: Board) -> None:
        super().__init__(board)

    def execute(self, selectedSpace: Space) -> bool:
        if self.board.isAPieceSelected():
            piece: Piece = self.board.getSelectedPiece()
            currentSpace = piece.getSpace()
            otherPiece: Piece = selectedSpace.getPiece()
            successful_move = piece.move(selectedSpace)
            if successful_move:
                if otherPiece is not None:
                    notification.push(
                        f"{otherPiece.getObjectName()} was defeated by {piece.getObjectName()}"
                    )
                    self.board.getCurrentPlayer().incrementPoints(
                        otherPiece.getPointsValue()
                    )
                    eventManager.post(
                        event=Events.TAKE_PIECE_EVENT,
                        data={
                            "player": piece.getPlayerName(),
                            "points": otherPiece.getPointsValue(),
                        },
                    )
                else:
                    notification.push("successfully moved")
                eventManager.post(event=Events.CHANGE_PLAYER_EVENT)
                self.board.changeCurrentPlayer()
                self.board.deselectPiece()
                # save board after every successful turn, in case the game crashes
                self.board.save()
            elif selectedSpace is not currentSpace:
                notification.push(f"invalid space")
