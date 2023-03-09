from ..character_classes.player import player
from typing import Callable


class AbilityCheck:
    def __init__(self, dc: int, on_pass: list[Callable], on_fail: list[Callable]):
        self.dc = dc
        self.on_pass = on_pass
        self.on_fail = on_fail

    def strength(self):
        if player.roll.strength() >= self.dc:
            for outcome in self.on_pass:
                outcome()
        else:
            for outcome in self.on_fail:
                outcome()

    def dexterity(self):
        if player.roll.dexterity() >= self.dc:
            for outcome in self.on_pass:
                outcome()
        else:
            for outcome in self.on_fail:
                outcome()

    def intelligence(self):
        if player.roll.intelligence() >= self.dc:
            for outcome in self.on_pass:
                outcome()
        else:
            for outcome in self.on_fail:
                outcome()

    def wisdom(self):
        if player.roll.wisdom() >= self.dc:
            for outcome in self.on_pass:
                outcome()
        else:
            for outcome in self.on_fail:
                outcome()

    def charisma(self):
        if player.roll.charisma() >= self.dc:
            for outcome in self.on_pass:
                outcome()
        else:
            for outcome in self.on_fail:
                outcome()

    def constitution(self):
        if player.roll.constitution() >= self.dc:
            for outcome in self.on_pass:
                outcome()
        else:
            for outcome in self.on_fail:
                outcome()
