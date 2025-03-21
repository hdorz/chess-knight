import pygame as pg


class Events:
    WIN_GAME_EVENT = pg.event.custom_type()
    TAKE_PIECE_EVENT = pg.event.custom_type()
    CHANGE_PLAYER_EVENT = pg.event.custom_type()
    CHECK_EVENT = pg.event.custom_type()
    STOP_CHECK_EVENT = pg.event.custom_type()
    UNDO_MOVE_EVENT = pg.event.custom_type()
    UNDO_MOVE_REPLACE_SPRITE_EVENT = pg.event.custom_type()
    FREEZE_DISPLAY_EVENT = pg.event.custom_type()
    STOP_FREEZE_DISPLAY_EVENT = pg.event.custom_type()


class EventManagerInstance:
    """
    Declare a single instance of the EventManager class for the entire application.
    Uses Singleton design pattern.
    """

    obj = None

    @staticmethod
    def getInstance():
        if not EventManagerInstance.obj:
            EventManagerInstance.obj = EventManager()
        return EventManagerInstance.obj


class EventManager:
    """
    Wrap the pygame event post function with EventManager.post() for
    easier readability.
    """

    def __init__(self) -> None:
        self.eventQueue: list[EventHolder] = []

    def post(self, event, data: dict | None = None, delay: int = 0):
        if data is not None:
            event = pg.event.Event(event, data)
        else:
            event = pg.event.Event(event, {})
        eventObj = EventHolder(event, delay)
        self.eventQueue.append(eventObj)

    def listen(self):
        if self.eventQueue:
            event = self.eventQueue[0].getEvent()
            if event:
                pg.event.post(event)
                self.eventQueue.pop(0)


class EventHolder:
    """
    An Event holder class that returns its event when the amount of time passed
    is greater than the assigned delay.
    """

    def __init__(self, event: pg.event.Event, delay: int = 0) -> None:
        self.event = event
        self.delay = delay  # milliseconds

        self.timestamp = pg.time.get_ticks()

    def getEvent(self):
        if pg.time.get_ticks() - self.timestamp >= self.delay:
            return self.event
        return None
