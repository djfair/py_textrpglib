from character_classes import Player
from funcs import ProxyFunc


class AbilityCheck:
    def __init__(self,
                 on_pass: tuple[ProxyFunc],
                 on_fail: tuple[ProxyFunc]):
        self.on_pass = on_pass
        self.on_fail = on_fail

    def strength(self, dc: int):
        if Player.instance.roll.strength() >= dc:
            for callable in self.on_pass:
                callable()
        for callable in self.on_fail:
            callable()

    def dexterity(self, dc: int):
        if Player.instance.roll.dexterity() >= dc:
            for callable in self.on_pass:
                callable()
        for callable in self.on_fail:
            callable()

    def intelligence(self, dc: int):
        if Player.instance.roll.intelligence() >= dc:
            for callable in self.on_pass:
                callable()
        for callable in self.on_fail:
            callable()

    def wisdom(self, dc: int):
        if Player.instance.roll.wisdom() >= dc:
            for callable in self.on_pass:
                callable()
        for callable in self.on_fail:
            callable()

    def charisma(self, dc: int):
        if Player.instance.roll.charisma() >= dc:
            for callable in self.on_pass:
                callable()
        for callable in self.on_fail:
            callable()

    def constition(self, dc: int):
        if Player.instance.roll.constitution() >= dc:
            for callable in self.on_pass:
                callable()
        for callable in self.on_fail:
            callable()


test_check = AbilityCheck(
    on_pass=(ProxyFunc(print, "Hello world!"),),
    on_fail=(ProxyFunc(print, "Goodbye cruel world!"),)
)
