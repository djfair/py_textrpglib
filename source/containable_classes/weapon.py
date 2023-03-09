from .containable import Containable, dataclass
from ..dice_class.dice import Dice


@dataclass
class Weapon(Containable):
    attack: Dice
    damage: Dice
    ammo: int | None = 1

    def set_ammo(self, amount: int):
        """Sets ammo to given amount. Use when stocking a character or NPC's inventory, and
        when creating loot caches for player reward."""
        try:
            self.ammo += amount  # type: ignore
            return self
        except TypeError:
            print(
                f"TypeError: method set_ammo used for weapon '{self.name}' "
                "with attribute 'ammo' set to None."
            )
            return self

    def fire(self, ammo_spent: int = 1) -> None:
        """Spends weapon's ammo if weapon's ammo is not None. With no args, will spend 1 ammo."""
        if self.ammo is not None:
            self.ammo -= ammo_spent
            if self.ammo < 0:
                self.ammo = 0
