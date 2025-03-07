from .engine.SpriteImage import SpriteImage
from .engine.utilities import load_image


class Button(SpriteImage):

    def __init__(
        self,
        fileName,
        relativeDir="chess/data/menu/",
        colorkey=None,
        scale: int = 1,
        coord: list = [0, 0],
    ) -> None:
        SpriteImage.__init__(
            self=self,
            fileName=fileName,
            relativeDir=relativeDir,
            colorkey=colorkey,
            scale=scale,
            coord=coord,
        )
        self.enabled = True

    def changeEnableState(self, enableButton: bool):
        if enableButton:
            enableImage, _ = load_image(f"{self.fileName}.png", self.relativeDir)
            self.image = enableImage
            self.original_image = enableImage
            self.hover_image, _ = load_image(
                f"{self.fileName}-hover.png", self.relativeDir
            )
            self.highlighted_image = enableImage
            self.enabled = True

        else:
            disableImage, _ = load_image(
                f"{self.fileName}-disabled.png", self.relativeDir
            )
            self.image = disableImage
            self.original_image = disableImage
            self.hover_image = disableImage
            self.highlighted_image = disableImage
            self.enabled = False

    def getFileName(self):
        return self.fileName

    def isEnabled(self):
        return self.enabled
