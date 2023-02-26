from dice import Dice
from containable_classes import Containable, Armor, Item, Spell, Weapon


class Player:
    def __new__(cls, name):
        """Creates a singleton object, if it is not created,
        or else returns the previous singleton object"""
        if not hasattr(cls, "instance"):
            cls.instance = super(Player, cls).__new__(cls)
        return cls.instance

    def __init__(self, name: str) -> None:
        self.name = name
        self.hp = 10
        self.ac = 10
        self.scores = self.Scores(outer=self)
        self.slots = self.Slots(outer=self)
        self.weapons = self.Weapons(outer=self)
        self.inventory = self.Inventory(outer=self)
        self.spells = self.SpellBook(outer=self)
        self.money = self.Money(outer=self)
        self.roll = self.Roll(outer=self)

    class Scores:
        def __init__(self, outer) -> None:
            self.strength = 10
            self.dexterity = 10
            self.intelligence = 10
            self.wisdom = 10
            self.charisma = 10
            self.constitution = 10
            self.initiative = 10
            self.max_hp = 10
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

            self.max_hp = 10 + (self.strength - 10) // 2 + (self.constitution - 10) // 2
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

        def __call__(self) -> list[Weapon]:
            return self._contents

        def len(self) -> int:
            return len(self._contents)

        def add(self, *new_weapons: Weapon, return_detail: bool = False):
            failed: dict[str, tuple[Weapon, str]] = {}
            for new_weapon in new_weapons:
                for owned_weapon in self._contents:
                    if (
                        owned_weapon.name == new_weapon.name
                        and new_weapon.ammo is not None
                    ):
                        owned_weapon.ammo += new_weapon.ammo  # type: ignore
                        break
                    if owned_weapon.name == new_weapon.name and new_weapon.ammo is None:
                        failed[new_weapon.name] = (
                            new_weapon,
                            "Failed: Weapon already owned.",
                        )
                else:
                    self._contents.append(new_weapon)

            if return_detail is False:
                return self.outer
            return failed, self.outer

    class Inventory:
        def __init__(self, outer) -> None:
            self._contents: list[Item | Armor] = []
            self.outer = outer

        def __call__(self) -> list[Item | Armor]:
            return self._contents

        def len(self) -> int:
            return len(self._contents)

        def add(self, *new_items: Item | Armor, return_detail: bool = False):
            failed: dict[str, tuple[Item | Armor, str]] = {}
            for new_item in new_items:
                for owned_item in self._contents:
                    if owned_item.name == new_item.name and "count" in dir(new_item):
                        owned_item.count += new_item.count  # type: ignore -- armor already excluded
                        break
                    elif owned_item.name == new_item.name and "count" not in dir(
                        new_item
                    ):
                        failed[new_item.name] = (
                            new_item,
                            "Failed: item already owned.",
                        )
                        break
                else:
                    self._contents.append(new_item)

            if return_detail is False:
                return self.outer
            return failed, self.outer

    class SpellBook:
        def __init__(self, outer) -> None:
            self._contents: list[Spell] = []
            self.outer = outer

        def __call__(self) -> list[Spell]:
            return self._contents

        def len(self) -> int:
            return len(self._contents)

        def add(self, *new_spells: Spell, return_detail: bool = True):
            failed: dict[str, tuple[Spell, str]] = {}
            for new_spell in new_spells:
                for learned_spell in self._contents:
                    if learned_spell.name == new_spell.name:
                        failed[new_spell.name] = (
                            new_spell,
                            "Failed: spell already known.",
                        )
                        break
                else:
                    self._contents.append(new_spell)

            if return_detail is False:
                return self.outer
            return failed, self.outer

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

        def receive(self, amount: int) -> None:
            self._amount += amount
            return None

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

    def purchase(self, *items, return_detail: bool = False):
        """Method for purchasing anything that will then be added to the
        character's belongings.

        if return_detail is False:
            returns bool
        if return detail is True:
            returns tuple[bool, dict[what failed and why], Player]"""

        total_cost = sum(item.cost for item in items)

        # Seperate *items into lists of different classes.
        weapons = [weapon for weapon in items if isinstance(weapon, Weapon)]
        items_and_armor = [i_a for i_a in items if isinstance(i_a, (Item, Armor))]
        spells = [spell for spell in items if isinstance(spell, Spell)]

        # Empty dict for failed purchases if return_detail=True
        failed: dict[str, dict[str, tuple[Containable, str]]] = {}

        if self.money.spend(total_cost) is True:
            # If player can afford, items will be added and failed additions
            # will be recorded in failed dict
            failed["weapons"] = self.weapons.add(*weapons, return_detail=True)[0]  # type: ignore
            failed["items_and_armor"] = (  # type: ignore
                self.inventory.add(*items_and_armor, return_detail=True)[0]  # type: ignore
            )  # type: ignore
            failed["spells"] = self.spells.add(*spells, return_detail=True)[0]  # type: ignore

            if return_detail is False:
                return True
            return True, failed, self

        # If player cannot afford, all items are recorded in failed dict
        failed["weapons"] = {
            weapon.name: (weapon, "Failed: Insufficient funds") for weapon in weapons
        }
        failed["items_and_armmor"] = {
            i_a.name: (i_a, "Failed: Insufficient funds") for i_a in items_and_armor
        }
        failed["spells"] = {
            spell.name: (spell, "Failed: Insufficient funds") for spell in spells
        }

        if return_detail is False:
            return False
        return False, failed, self

    def pick_up(self, *items, return_detail: bool = False):
        """Method for picking up items without paying for them.

        if return_detail is False:
            returns Player
        if return_detail is True:
            returns tuple[dict[what failed and why], Player]"""

        weapons = [weapon for weapon in items if isinstance(weapon, Weapon)]
        items_and_armor = [i_a for i_a in items if isinstance(i_a, (Item, Armor))]
        spells = [spell for spell in items if isinstance(spell, Spell)]

        failed: dict[str, dict[str, tuple[Containable, str]]] = {}
        failed["weapons"] = self.weapons.add(*weapons)[0]  # type: ignore
        failed["items_and_armor"] = self.inventory.add(*items_and_armor)[0]  # type: ignore
        failed["spells"] = self.spells.add(*spells)[0]  # type: ignore

        if return_detail is False:
            return self
        return failed, self
