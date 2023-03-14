from ..containable_classes.weapon import Weapon
from ..containable_classes.armor import Armor
from ..containable_classes.item import Item
from ..containable_classes.spell import Spell


def calculate_containables_cost(self, *to_buy: Weapon | Armor | Item | Spell) -> int:
    total_cost = 0
    for containable in to_buy:
        if isinstance(containable, Item):
            total_cost += containable.cost * containable.count
        else:
            total_cost += containable.cost
    return total_cost
