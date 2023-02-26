from random import randint


class Dice:
    def __init__(self, mod: int, dice: int = 20, no_of_dice: int = 1):
        self.mod = mod
        self.dice = dice
        self.no_of_dice = no_of_dice

    def __call__(self) -> int:
        return (
            sum([randint(1, self.dice) for current_dice in range(self.no_of_dice)])
            + self.mod
        )
