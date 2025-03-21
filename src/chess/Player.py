from typing import Literal

from .BoardConfigSectionKeys import BoardConfigSectionKeys as cfgKeys
from .engine.SaveLoadMixin import SaveLoadMixin


class Player(SaveLoadMixin):
    def __init__(
        self,
        name: str,
        points: int = 0,
        team: Literal["black", "white"] = "default",
    ):
        self.name: str = name
        self.points: int = points
        self.team = team

    def incrementPoints(self, points: int):
        self.points += points

    def decreasePoints(self, points: int):
        self.points -= points

    def getPoints(self) -> int:
        return self.points

    def getName(self) -> str:
        return self.name

    def getTeam(self) -> Literal["black", "white"]:
        return self.team

    def save(self, **kwargs):
        config = self.getParser()
        playerState = {
            "name": self.name,
            "team": self.team,
            "points": self.points,
        }
        config.set(cfgKeys.PLAYERS, f"{kwargs['number']}", playerState)
