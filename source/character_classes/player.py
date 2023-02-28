from ..dice_class.dice import Dice
from ..containable_classes.armor import Armor
from ..containable_classes.item import Item
from ..containable_classes.spell import Spell
from ..containable_classes.weapon import Weapon


class Player:
    def __new__(cls, name):
        """Creates a singleton object, if it is not created,
        or else returns the previous singleton object"""
        if not hasattr(cls, "instance"):
            cls.instance = super(Player, cls).__new__(cls)
        return cls.instance

    def __init__(self, name: str) -> None:
        self.name = name
        self.hp = self.HitPoints()
        self.ac = 10
        self.scores = self.Scores(outer=self)
        self.slots = self.Slots(outer=self)
        self.weapons = self.Weapons(outer=self)
        self.inventory = self.Inventory(outer=self)
        self.spells = self.SpellBook(outer=self)
        self.money = self.Money(outer=self)
        self.roll = self.Roll(outer=self)

    class HitPoints:
        def __init__(self) -> None:
            self._hp = 10
            self._max = 10

        def __call__(self) -> int:
            return self._hp

        def max(self) -> int:
            return self._max

        def heal(self, amount: int) -> None:
            if self._hp + amount > self._max:
                self._hp = 0 + self._max
            self._hp += amount

    class Scores:
        def __init__(self, outer) -> None:
            self.strength = 10
            self.dexterity = 10
            self.intelligence = 10
            self.wisdom = 10
            self.charisma = 10
            self.constitution = 10
            self.initiative = 0
            self.outer = outer

        def assign(
            self,
            strength: int | None = None,
            dexterity: int | None = None,
            intelligence: int | None = None,
            wisdom: int | None = None,
            charisma: int | None = None,
            constitution: int | None = None,
        ):

            if strength is not None:
                self.strength = strength
            if dexterity is not None:
                self.dexterity = dexterity
            if intelligence is not None:
                self.intelligence = intelligence
            if wisdom is not None:
                self.wisdom = wisdom
            if charisma is not None:
                self.charisma = charisma
            if constitution is not None:
                self.constitution = constitution

            self.outer.hp.max = (
                10 + (self.strength - 10) // 2 + (self.constitution - 10) // 2
            )
            self.outer.ac = 10 + (self.dexterity - 10) // 2 + self.outer.slots.armor.mod
            self.initiative = (self.dexterity - 10) // 2 + (self.intelligence - 10) // 2

            return self.outer

    class Slots:
        def __init__(self, outer) -> None:
            self.armor: Armor = Armor(name="No armor", cost=0, desc="No armor", mod=0)
            self.weapon: Weapon = Weapon(
                name="Fist",
                cost=0,
                desc="A closed fist",
                attack=Dice(0),
                damage=Dice(0, 4),
            )
            self.outer = outer

        def equip(self, armor_or_weapon: Armor | Weapon):
            if isinstance(armor_or_weapon, Armor):
                self.armor = armor_or_weapon
                self.outer.ac = 10 + self.outer.scores.dexterity + self.armor.mod
            elif isinstance(armor_or_weapon, Weapon):
                self.weapon = armor_or_weapon
            return self.outer

        def stow_armor(self):
            self.equip(Armor(name="No armor", cost=0, desc="No armor", mod=0))
            return self.outer

        def stow_weapon(self):
            self.equip(
                Weapon(
                    name="Fist",
                    cost=0,
                    desc="A closed fist",
                    attack=Dice(0),
                    damage=Dice(0, 4),
                )
            )
            return self.outer

    class Weapons:
        def __init__(self, outer) -> None:
            self._contents: list[Weapon] = []
            self.outer = outer
            self.failed: dict[str, str] = {}

        def __call__(self) -> list[Weapon]:
            return self._contents

        def len(self) -> int:
            return len(self._contents)

        def add(self, *new_weapons: Weapon):
            self.failed: dict[str, str] = {}
            for new_weapon in new_weapons:
                for owned_weapon in self._contents:
                    if (
                        owned_weapon.name == new_weapon.name
                        and new_weapon.ammo is not None
                    ):
                        owned_weapon.ammo += new_weapon.ammo  # type: ignore
                        break
                    if owned_weapon.name == new_weapon.name and new_weapon.ammo is None:
                        self.failed[new_weapon.name] = "Failed: Weapon already owned."
                else:
                    self._contents.append(new_weapon)
            return self.outer

        def remove(self, *weapons: Weapon):
            for weapon in weapons:
                for owned_weapon in self._contents:
                    if weapon.name == owned_weapon.name:
                        self._contents.remove(owned_weapon)
                        break
            return self.outer

    class Inventory:
        def __init__(self, outer) -> None:
            self._contents: list[Item | Armor] = []
            self.outer = outer
            self.failed: dict[str, str] = {}

        def __call__(self) -> list[Item | Armor]:
            return self._contents

        def len(self) -> int:
            return len(self._contents)

        def add(self, *new_items: Item | Armor):
            self.failed: dict[str, str] = {}
            for new_item in new_items:
                for owned_item in self._contents:
                    if owned_item.name == new_item.name and "count" in dir(new_item):
                        owned_item.count += new_item.count  # type: ignore -- armor already excluded
                        break
                    elif owned_item.name == new_item.name and "count" not in dir(
                        new_item
                    ):
                        self.failed[new_item.name] = "Failed: item already owned."
                        break
                else:
                    self._contents.append(new_item)
            return self.outer

        def remove(self, *items_or_armor: Item | Armor):
            for i_a in items_or_armor:
                if isinstance(i_a, Item):
                    for owned_i_a in self._contents:
                        if i_a.name == owned_i_a.name and isinstance(owned_i_a, Item):
                            owned_i_a.set_count(owned_i_a.count - i_a.count)
                            if owned_i_a.count < 1:
                                self._contents.remove(owned_i_a)
                            break
                else:
                    for owned_i_a in self._contents:
                        if i_a.name == owned_i_a.name:
                            self._contents.remove(owned_i_a)
                            break
            return self.outer

    class SpellBook:
        def __init__(self, outer) -> None:
            self._contents: list[Spell] = []
            self.outer = outer
            self.failed: dict[str, str] = {}

        def __call__(self) -> list[Spell]:
            return self._contents

        def len(self) -> int:
            return len(self._contents)

        def add(self, *new_spells: Spell):
            self.failed: dict[str, str] = {}
            for new_spell in new_spells:
                for learned_spell in self._contents:
                    if learned_spell.name == new_spell.name:
                        self.failed[new_spell.name] = "Failed: spell already known."
                        break
                else:
                    self._contents.append(new_spell)
            return self.outer

        def remove(self, *spells: Spell):
            for spell in spells:
                for known_spell in self._contents:
                    if spell.name == known_spell.name:
                        self._contents.remove(known_spell)
                        break
            return self.outer

    class Money:
        def __init__(self, outer):
            self._amount: int = 0
            self.outer = outer

        def __call__(self) -> int:
            return self._amount

        def __str__(self) -> str:
            if self._amount > 0:
                if self._amount > 99:
                    return f"${self._amount / 100:,.2f}"
                return f"{self._amount} cents"
            return "no money"

        def spend(self, amount: int) -> bool:
            if self._amount >= amount:
                self._amount -= amount
                return True
            return False

        def receive(self, amount: int):
            self._amount += amount
            return self.outer

    class Roll:
        def __init__(self, outer) -> None:
            self.outer = outer

        def strength(self) -> int:
            return Dice((self.outer.scores.strength - 10) // 2)()

        def dexterity(self) -> int:
            return Dice((self.outer.scores.dexterity - 10) // 2)()

        def intelligence(self) -> int:
            return Dice((self.outer.scores.intelligence - 10) // 2)()

        def wisdom(self) -> int:
            return Dice((self.outer.scores.wisdom - 10) // 2)()

        def charisma(self) -> int:
            return Dice((self.outer.scores.charisma - 10) // 2)()

        def constitution(self) -> int:
            return Dice((self.outer.scores.constitution - 10) // 2)()

        def attack(self) -> int:
            return self.outer.slots.weapon.attack()

        def damage(self) -> int:
            return self.outer.slots.weapon.damage()

    def purchase(self, *items: Item | Armor | Weapon | Spell) -> bool:
        """Method for purchasing anything that will then be added to the
        character's belongings."""

        total_cost = 0
        for item in items:
            if isinstance(item, Item):
                total_cost += item.cost * item.count
            else:
                total_cost += item.cost

        weapons = [weapon for weapon in items if isinstance(weapon, Weapon)]
        items_and_armor = [i_a for i_a in items if isinstance(i_a, (Item, Armor))]
        spells = [spell for spell in items if isinstance(spell, Spell)]

        if self.money.spend(total_cost) is True:
            (
                self.weapons.add(*weapons)
                .inventory.add(*items_and_armor)
                .spells.add(*spells)
            )
            return True

        self.weapons.failed = {
            weapon.name: "Failed: Insufficient funds." for weapon in weapons
        }
        self.inventory.failed = {
            i_a.name: "Failed: Insufficient funds." for i_a in items_and_armor
        }
        self.spells.failed = {
            spell.name: "Failed: Insufficient funds." for spell in spells
        }
        return False

    def pick_up(self, *items: Item | Armor | Weapon | Spell):
        """Method for picking up items without paying for them."""

        weapons = [weapon for weapon in items if isinstance(weapon, Weapon)]
        items_and_armor = [i_a for i_a in items if isinstance(i_a, (Item, Armor))]
        spells = [spell for spell in items if isinstance(spell, Spell)]

        self.weapons.add(*weapons).inventory.add(*items_and_armor).spells.add(*spells)
        return self


player = Player("Default_Player_Name")
