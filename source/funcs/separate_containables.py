from ..containable_classes.weapon import Weapon
from ..containable_classes.armor import Armor
from ..containable_classes.item import Item
from ..containable_classes.spell import Spell


def separate_containables(*containables: Armor | Item | Weapon | Spell):
    weapons: list[Weapon] = []
    armor: list[Armor] = []
    items: list[Item] = []
    spells: list[Spell] = []
    for containable in containables:
        if isinstance(containable, Weapon):
            weapons.append(containable)
        elif isinstance(containable, Armor):
            armor.append(containable)
        elif isinstance(containable, Item):
            items.append(containable)
        elif isinstance(containable, Spell):
            spells.append(containable)
    return weapons, armor, items, spells
