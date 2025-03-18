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
                self.board.addMoveToMoveStack(
                    {
                        "piece": piece,
                        "otherPiece": otherPiece,
                        "oldSpace": currentSpace,
                        "newSpace": selectedSpace,
                    }
                )
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
                            "playerName": piece.getPlayerName(),
                            "points": otherPiece.getPointsValue(),
                        },
                    )
                else:
                    notification.push("successfully moved")
                eventManager.post(event=Events.CHANGE_PLAYER_EVENT)
                self.board.changeCurrentPlayer()
                self.board.deselectPiece()
                self.board.makeAllPiecesFindPotentialTiles()
                self.board.setIsCheck(self.board.checkIsThereCheck())
                if self.board.isInCheck():
                    eventManager.post(event=Events.CHECK_EVENT)
                # save board after every successful turn, in case the game crashes
                # self.board.save()
            elif selectedSpace is not currentSpace:
                notification.push(f"invalid space")


class IsBoardInCheckMateTurn(Turn):
    """
    Check if a player is in checkmate.
    """

    def __init__(self, board: Board) -> None:
        super().__init__(board)

    def _undoMove(self):
        lastMove = self.board.popMoveFromMoveStack()
        if lastMove is not None:
            lastMove.oldSpace.highlight()
            lastMove.piece.move(lastMove.oldSpace, updatePosition=False)
            lastMove.piece.setCoord(lastMove.oldSpace.getCoord())
            lastMove.oldSpace.stopHighlight()
            if lastMove.otherPiece is not None:
                lastMove.newSpace.highlight()
                lastMove.otherPiece.move(lastMove.newSpace, updatePosition=False)
                lastMove.otherPiece.setCoord(lastMove.newSpace.getCoord())
                lastMove.newSpace.stopHighlight()
        else:
            raise Exception("IsBoardInCheckMateTurn _undoMove: no move was found")

    def _checkAllPiecesForCheckmate(self) -> bool:
        """Brute force to see if checkmate has occurred"""
        currentPlayerPieces = self.board.getCurrentPlayersPiecesOnBoard()
        stopLoop = False
        for piece in currentPlayerPieces:
            self.board.selectPiece(piece)
            potentialSpaces = piece.getPotentialSpaces()
            for space in potentialSpaces:
                self.board.highlightPotentialTiles()
                oldSpace = piece.getSpace()
                otherPiece = space.getPiece()
                successful_move = piece.move(space, updatePosition=False)
                if successful_move:
                    self.board.addMoveToMoveStack(
                        {
                            "piece": piece,
                            "otherPiece": otherPiece,
                            "oldSpace": oldSpace,
                            "newSpace": space,
                        }
                    )
                    self.board.makeAllPiecesFindPotentialTiles()
                if not self.board.checkIsThereCheck():
                    stopLoop = True
                self._undoMove()
                self.board.makeAllPiecesFindPotentialTiles()
                if stopLoop:
                    break
            self.board.deselectPiece()
            if stopLoop:
                return False
        return True

    def execute(self):
        king = self.board.getCurrentPlayersKing()
        if king.getPlayerName() == self.board.getCurrentPlayer().getName():
            if king.getIsOnBoard():
                self.board.selectPiece(king)
                self.board.highlightPotentialTiles()
                # king can move
                if self.board.areAnyTilesHighlighted():
                    self.board.deselectPiece()
                    return
                # king cannot move, look at other pieces
                self.board.deselectPiece()
                eventManager.post(event=Events.FREEZE_DISPLAY_EVENT)
                isCheckmate = self._checkAllPiecesForCheckmate()
                eventManager.post(event=Events.STOP_FREEZE_DISPLAY_EVENT)
                if isCheckmate:
                    otherPlayer = self.board.getOtherPlayer()
                    notification.push(
                        f"Game finished! {otherPlayer.getName()} ({otherPlayer.getTeam()}) won!"
                    )


class MovePieceCheckTurn(Turn):

    def __init__(self, board: Board) -> None:
        super().__init__(board)

    def _undoMove(self):
        lastMove = self.board.popMoveFromMoveStack()
        if lastMove is not None:
            lastMove.oldSpace.highlight()
            lastMove.piece.move(lastMove.oldSpace, updatePosition=False)
            lastMove.piece.setCoord(lastMove.oldSpace.getCoord())
            lastMove.oldSpace.stopHighlight()
            if lastMove.otherPiece is not None:
                lastMove.newSpace.highlight()
                lastMove.otherPiece.move(lastMove.newSpace, updatePosition=False)
                lastMove.otherPiece.setCoord(lastMove.newSpace.getCoord())
                lastMove.newSpace.stopHighlight()
        else:
            raise Exception("MovePieceCheckTurn _undoMove: no move was found")

    def execute(self, selectedSpace: Space) -> bool:
        isCheckmate = self.board.isInCheck()
        if self.board.isAPieceSelected() and isCheckmate:
            piece: Piece = self.board.getSelectedPiece()
            currentSpace = piece.getSpace()
            otherPiece: Piece = selectedSpace.getPiece()
            successful_move = piece.move(selectedSpace, updatePosition=False)
            # mock a successful turn to see if the board is still in checkmate
            if successful_move:
                self.board.addMoveToMoveStack(
                    {
                        "piece": piece,
                        "otherPiece": otherPiece,
                        "oldSpace": currentSpace,
                        "newSpace": selectedSpace,
                    }
                )
                self.board.makeAllPiecesFindPotentialTiles()
                self.board.setIsCheck(self.board.checkIsThereCheck())
                if self.board.isInCheck():
                    self._undoMove()
                    self.board.makeAllPiecesFindPotentialTiles()
                    self.board.highlightPotentialTiles()
                    notification.push("invalid space, still in checkmate")

                else:
                    if otherPiece is not None:
                        otherPiece.kill()
                        piece.setCoord(piece.getSpace().getCoord())
                        notification.push(
                            f"{otherPiece.getObjectName()} was defeated by {piece.getObjectName()}"
                        )
                        self.board.getCurrentPlayer().incrementPoints(
                            otherPiece.getPointsValue()
                        )
                        eventManager.post(
                            event=Events.TAKE_PIECE_EVENT,
                            data={
                                "playerName": piece.getPlayerName(),
                                "points": otherPiece.getPointsValue(),
                            },
                        )
                    else:
                        notification.push("successfully moved")
                    eventManager.post(event=Events.STOP_CHECK_EVENT)
                    eventManager.post(event=Events.CHANGE_PLAYER_EVENT)
                    self.board.changeCurrentPlayer()
                    self.board.deselectPiece()
                    self.board.makeAllPiecesFindPotentialTiles()
                    self.board.setIsCheck(self.board.checkIsThereCheck())
                    if self.board.isInCheck():
                        eventManager.post(event=Events.CHECK_EVENT)
                    # save board after every successful turn, in case the game crashes
                    # self.board.save()
            elif selectedSpace is not currentSpace:
                notification.push(f"invalid space")


class UndoTurn(Turn):

    def __init__(self, board: Board) -> None:
        super().__init__(board)

    def _undoMove(self) -> bool:
        lastMove = self.board.popMoveFromMoveStack()
        if lastMove is not None:
            lastMove.oldSpace.highlight()
            lastMove.piece.move(lastMove.oldSpace)
            # lastMove.piece.setCoord(lastMove.oldSpace.getCoord())
            lastMove.oldSpace.stopHighlight()
            if lastMove.otherPiece is not None:
                lastMove.newSpace.highlight()
                lastMove.otherPiece.move(lastMove.newSpace, updatePosition=False)
                lastMove.otherPiece.setCoord(lastMove.newSpace.getCoord())
                lastMove.newSpace.stopHighlight()
                eventManager.post(
                    event=Events.UNDO_MOVE_EVENT,
                    data={
                        "otherPiece": lastMove.otherPiece,
                        "playerName": lastMove.piece.getPlayerName(),
                        "points": lastMove.otherPiece.getPointsValue(),
                    },
                )
            return True
        return False

    def execute(self) -> bool:
        if not self.board.isAPieceSelected():
            undo_successful = self._undoMove()
            if undo_successful:
                notification.push("undo last move")
                eventManager.post(event=Events.CHANGE_PLAYER_EVENT)
                self.board.changeCurrentPlayer()
                self.board.deselectPiece()
                self.board.makeAllPiecesFindPotentialTiles()
                self.board.setIsCheck(self.board.checkIsThereCheck())
                if self.board.isInCheck():
                    eventManager.post(event=Events.CHECK_EVENT)
                else:
                    eventManager.post(event=Events.STOP_CHECK_EVENT)
            else:
                notification.push("cannot undo, no move left to undo")
        else:
            notification.push("cannot undo, deselect piece first")
