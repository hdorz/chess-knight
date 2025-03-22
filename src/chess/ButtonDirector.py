import os.path

from .Button import Button
from .engine.constants import windowSize
from .TriggerKey import TriggerKey

windowCentre = (windowSize[0] * 0.5, windowSize[1] * 0.5)


class ButtonDirector:
    def __init__(self):
        pass

    def createStartButtons(self):
        newButton = Button(TriggerKey.NEW)
        newButton.setCoord(
            [
                windowCentre[0] - newButton.getWidth(),
                windowCentre[1] - newButton.getHeight(),
            ]
        )

        loadButton = Button(TriggerKey.LOAD)
        loadButton.setCoord(
            [
                windowCentre[0],
                windowCentre[1] - newButton.getHeight(),
            ]
        )

        if not os.path.isfile("save.cfg"):
            loadButton.changeEnableState(enableButton=False)

        return [newButton, loadButton]

    def createUndoButton(self):
        undoButton = Button(TriggerKey.UNDO, scale=0.155)
        undoButton.setCoord([1200, 0])

        return [undoButton]

    def createBackButton(self):
        backButton = Button(TriggerKey.BACK, scale=0.155)
        backButton.setCoord([1200, 870])

        return [backButton]

    def createSelectModeButtons(self):
        newButton = Button(TriggerKey.ALL_KNIGHTS)
        newButton.setCoord(
            [
                windowCentre[0] - newButton.getWidth(),
                windowCentre[1] - newButton.getHeight(),
            ]
        )

        loadButton = Button(TriggerKey.STANDARD)
        loadButton.setCoord(
            [
                windowCentre[0],
                windowCentre[1] - newButton.getHeight(),
            ]
        )

        return [newButton, loadButton]
