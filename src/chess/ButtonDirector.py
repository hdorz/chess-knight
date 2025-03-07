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
