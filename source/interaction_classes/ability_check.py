from character_classes import Player
from typing import Callable


class AbilityCheck:
    def __init__(self, on_pass: tuple[Callable], on_fail: tuple[Callable]):
        self.on_pass = on_pass
        self.on_fail = on_fail

    def strength(self, dc: int):
        if Player.instance.roll.strength() >= dc:
            for outcome in self.on_pass:
                outcome()
        for outcome in self.on_fail:
            outcome()

    def dexterity(self, dc: int):
        if Player.instance.roll.dexterity() >= dc:
            for outcome in self.on_pass:
                outcome()
        for outcome in self.on_fail:
            outcome()

    def intelligence(self, dc: int):
        if Player.instance.roll.intelligence() >= dc:
            for outcome in self.on_pass:
                outcome()
        for outcome in self.on_fail:
            outcome()

    def wisdom(self, dc: int):
        if Player.instance.roll.wisdom() >= dc:
            for outcome in self.on_pass:
                outcome()
        for outcome in self.on_fail:
            outcome()

    def charisma(self, dc: int):
        if Player.instance.roll.charisma() >= dc:
            for outcome in self.on_pass:
                outcome()
        for outcome in self.on_fail:
            outcome()

    def constition(self, dc: int):
        if Player.instance.roll.constitution() >= dc:
            for outcome in self.on_pass:
                outcome()
        for outcome in self.on_fail:
            outcome()
