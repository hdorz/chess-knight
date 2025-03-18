import pygame as pg

from .utilities import load_image


class SpriteImage(pg.sprite.Sprite):
    """
    Class which concerns itself with displaying objects on screen.
    """

    def __init__(
        self,
        fileName,
        relativeDir,
        colorkey=None,
        scale: int = 1,
        coord: list = [0, 0],
    ) -> None:
        if type(self) is SpriteImage:
            raise Exception("SpriteImage class is an abstract class")
        self.fileName = fileName
        self.relativeDir = relativeDir
        self.colorkey = colorkey
        self.scale = scale

        pg.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image(
            f"{fileName}.png", relativeDir, colorkey, scale
        )
        try:
            self.hover_image, _ = load_image(
                f"{fileName}-hover.png", relativeDir, colorkey, scale
            )
        except:
            self.hover_image = self.image

        try:
            self.highlighted_image, _ = load_image(
                f"{fileName}-highlighted.png", relativeDir, colorkey, scale
            )
        except:
            self.highlighted_image = self.image
        self.original_image = self.image
        self._highlighted = False
        self.coord = None
        self.setCoord(coord)

        self.movementSpeed = 4

    def setCoord(self, coord: list):
        """
        Set coordinate of Sprite and immediately reflect that on the display.
        """
        self.updatePosition(coord)
        vec = pg.math.Vector2
        vector = vec(self.coord) - vec(self.rect.topleft)
        self.rect.move_ip(*vector)

    def getCoord(self):
        return self.coord

    def getWidth(self):
        return self.rect.width

    def getHeight(self):
        return self.rect.height

    def resizeSprite(self, width):
        size = (width, width)
        self.image = pg.transform.scale(self.image, size)
        self.rect = self.image.get_rect()

    def updatePosition(self, coord):
        """
        Set coordinate of Sprite and allow sprite to move to that position
        through animate().
        """
        self.coord = coord

    def animate(self):
        """
        Animate movement of Sprite from self.rect.topleft to self.coord.
        Incrementally update on screen position of sprite using pg.math.Vector2.
        """
        vec = pg.math.Vector2
        vector = vec(self.coord) - vec(self.rect.topleft)
        if vector.length() > self.movementSpeed:
            vector.scale_to_length(self.movementSpeed)
        self.rect.move_ip(*vector)

    def isHighlighted(self) -> bool:
        return self._highlighted

    def highlight(self):
        self._highlighted = True

    def stopHighlight(self):
        self._highlighted = False

    def update(self):
        pos = pg.mouse.get_pos()
        hit = self.rect.collidepoint(pos)
        size = self.image.get_size()

        if hit:
            self.image = pg.transform.scale(self.hover_image, size)
        elif self.isHighlighted():
            self.image = pg.transform.scale(self.highlighted_image, size)
        else:
            self.image = pg.transform.scale(self.original_image, size)

        self.animate()
