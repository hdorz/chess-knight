import pygame as pg

from ..constants.constants import blackFontColour, windowSize
from .utilities import load_image, resource_path

notificationTextCoord = (windowSize[0] * 0.02, windowSize[1] * 0.93)
notificationBackgroundCoord = (windowSize[0] * 0.005, windowSize[1] * 0.92)
notificationFontSize = int(windowSize[1] * 0.04)
notificationBackgroundScale = windowSize[1] / 1280


class NotificationInstance:
    """
    Declare a single instance of the Notification class for the entire application.
    Uses Singleton design pattern.
    """

    obj = None

    @staticmethod
    def getInstance():
        if not NotificationInstance.obj:
            NotificationInstance.obj = Notification()
        return NotificationInstance.obj


class NotificationHolder:
    """
    Notification holder class returns its message once time elapsed is greater
    than the assigned delay.
    """

    def __init__(self, msg: str, persist: int = 1000):
        self.msg = msg
        self.persist = persist  # milliseconds

    def getMessage(self):
        return self.msg

    def getPersistTime(self):
        return self.persist


class Notification:
    """
    Notification class handles the appearance of notifications whenever they are pushed.
    """

    def __init__(self) -> None:
        self.messageQueue = []
        self.font_size = notificationFontSize
        self.font = None
        self.message = ""
        self.textSurface = None
        self.backgroundSurface = None
        self.textAlpha = 255
        self.backgroundAlpha = 255
        self.msgPersistTime = 1000  # milliseconds
        self.lastMessageTime = pg.time.get_ticks()
        self.textCoord = notificationTextCoord
        self.backgroundCoord = notificationBackgroundCoord
        self.fadeOutSpeed = 10

    def clear(self):
        """
        Clear the message queue.
        """
        self.messageQueue = []

    def setup(self, font):
        """
        Should be run after pygame.init()
        """
        self._setFont(font)
        self._setTextSurface()
        self._setBackgroundSurface()

    def _setFont(self, font):
        """
        Pass in pygame.font.Font function. Call this after pygame.init()
        """
        self.font = font(
            resource_path("chess/data/font/BerlinSansFB.TTF"), self.font_size
        )

    def _setTextSurface(self):
        """
        Set text surface based on font. Call this after pygame.init()
        """
        self.textSurface = self.font.render(self.message, False, blackFontColour)

    def _setBackgroundSurface(self):
        """
        Set text box for messages. Call this after pygame.init()
        """
        self.backgroundSurface, _ = load_image(
            "notifications/notification_window.png",
            scale=notificationBackgroundScale,
        )

    def push(self, message: str, persist: int = 1000):
        self.messageQueue.append(NotificationHolder(msg=message, persist=persist))

    def _renderMessage(self, message):
        self.textSurface = self.font.render(message, False, blackFontColour)

    def _fadeOutText(self, persist: int):
        """
        Start fading notification once message lands in queue
        """
        currentTime = pg.time.get_ticks()
        if currentTime - self.lastMessageTime >= persist:
            self.textAlpha -= self.fadeOutSpeed
        self.textSurface.set_alpha(self.textAlpha)
        if self.textAlpha <= 0:
            self.message = ""

    def _fadeOutBackground(self, persist: int):
        """
        Start fading background when no messages left in queue.
        """
        currentTime = pg.time.get_ticks()
        if currentTime - self.lastMessageTime >= persist:
            self.backgroundAlpha -= self.fadeOutSpeed
        self.backgroundSurface.set_alpha(self.backgroundAlpha)

    def render(self):
        """
        Start rendering messages when messageQueue fills up with messages.
        """
        if (not self.message) and self.messageQueue:
            msgHolder: NotificationHolder = self.messageQueue.pop(0)
            self.message = msgHolder.getMessage()
            self.msgPersistTime = msgHolder.getPersistTime()
            self.backgroundAlpha = 255
            self.backgroundSurface.set_alpha(self.backgroundAlpha)
            self.textAlpha = 255
            self._renderMessage(self.message)
            self.lastMessageTime = pg.time.get_ticks()
            return (self.textSurface, self.textCoord), (
                self.backgroundSurface,
                self.backgroundCoord,
            )

        if self.message:
            self._fadeOutText(self.msgPersistTime)
        if not self.messageQueue:
            self._fadeOutBackground(self.msgPersistTime)

        return (self.textSurface, self.textCoord), (
            self.backgroundSurface,
            self.backgroundCoord,
        )
