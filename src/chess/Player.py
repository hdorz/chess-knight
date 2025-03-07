from .engine.SaveLoadMixin import SaveLoadMixin


class Player(SaveLoadMixin):
    def __init__(self, name: str, points: int = 0):
        self.name: str = name
        self.points: int = points

    def incrementPoints(self, points: int):
        self.points += points

    def getPoints(self) -> int:
        return self.points

    def getName(self) -> str:
        return self.name

    def save(self, **kwargs):
        config = self.getParser()
        playerState = {
            "name": self.name,
            "points": self.points,
        }
        config.set("players", f"{kwargs['number']}", playerState)
