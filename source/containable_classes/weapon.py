from containable import Containable, dataclass
from dice import Dice

@dataclass
class Weapon(Containable):
    attack: Dice
    damage: Dice
    ammo: int | None = None

    def fire(self, ammo_spent: int = 1):
        if self.ammo is not None:
            self.ammo -= ammo_spent
            if self.ammo < 0:
                self.ammo = 0
            return self
        print(
            f"Error: method fire() used on weapon {self.name} with ammo set to None.")
        raise TypeError