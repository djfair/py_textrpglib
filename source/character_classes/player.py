from ..dice_class.dice import Dice
from ..containable_classes.armor import Armor
from ..containable_classes.item import Item
from ..containable_classes.spell import Spell
from ..containable_classes.weapon import Weapon
from ..funcs.separate_containables import separate_containables
from ..funcs.calculate_containables_cost import calculate_containables_cost
from typing import Type


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
        self.scores = self.Scores(owner=self)
        self.slots = self.Slots(owner=self)
        self.inventory = self.Inventory(owner=self)
        self.money = self.Money(owner=self)
        self.roll = self.Roll(owner=self)

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

        def take_damage(self, amount: int) -> None:
            if self._hp < amount:
                self._hp = 0
            else:
                self._hp -= amount

    class Scores:
        def __init__(self, owner) -> None:
            self.strength = 10
            self.dexterity = 10
            self.intelligence = 10
            self.wisdom = 10
            self.charisma = 10
            self.constitution = 10
            self.initiative = 0
            self.owner = owner

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

            self.owner.hp.max = (
                10 + (self.strength - 10) // 2 + (self.constitution - 10) // 2
            )
            self.owner.ac = 10 + (self.dexterity - 10) // 2 + self.owner.slots.armor.mod
            self.initiative = (self.dexterity - 10) // 2 + (self.intelligence - 10) // 2

            return self.owner

    class Slots:
        def __init__(self, owner) -> None:
            self.armor: Armor = Armor(name="No armor", cost=0, desc="No armor", mod=0)
            self.weapon: Weapon = Weapon(
                name="Fist",
                cost=0,
                desc="A closed fist",
                attack=Dice(0),
                damage=Dice(0, 4),
            )
            self.owner = owner

        def equip(self, armor_or_weapon: Armor | Weapon):
            if isinstance(armor_or_weapon, Armor):
                self.armor = armor_or_weapon
                self.owner.ac = 10 + self.owner.scores.dexterity + self.armor.mod
            elif isinstance(armor_or_weapon, Weapon):
                self.weapon = armor_or_weapon
            return self.owner

        def stow_armor(self):
            self.equip(Armor(name="No armor", cost=0, desc="No armor", mod=0))
            self.owner.ac = 10 + self.owner.scores.dexterity + self.armor.mod
            return self.owner

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
            return self.owner

    class Inventory:
        def __init__(self, owner) -> None:
            self._weapons: list[Weapon] = []
            self._armor: list[Armor] = []
            self._items: list[Item] = []
            self._spells: list[Spell] = []
            self.owner = owner

        def __call__(
            self,
            filter_type: Type[Weapon]
            | Type[Armor]
            | Type[Item]
            | Type[Spell]
            | None = None,
        ):
            if filter_type is not None:
                filtered_inventory: list[filter_type] = []  # type: ignore
                for containable in (
                    *self._weapons,
                    *self._armor,
                    *self._items,
                    *self._spells,
                ):
                    if isinstance(containable, filter_type):
                        filtered_inventory.append(containable)
            else:
                filtered_inventory: list[Weapon | Armor | Item | Spell] = [
                    *self._weapons,
                    *self._armor,
                    *self._items,
                    *self._spells,
                ]
            return tuple(filtered_inventory)

        def pick_up_weapons(self, *weapons: Weapon) -> None:
            for picked_up_weapon in weapons:
                if picked_up_weapon.ammo is not None:
                    for owned_weapon in self._weapons:
                        if (
                            owned_weapon.name == picked_up_weapon.name
                            and owned_weapon.ammo is not None
                        ):
                            owned_weapon.ammo += picked_up_weapon.ammo
                            break
                else:
                    self._weapons.append(picked_up_weapon)
            return None

        def drop_weapons(self, *weapons: Weapon) -> None:
            for drop_weapon in weapons:
                for owned_weapon in self._weapons:
                    if drop_weapon is owned_weapon:
                        self._weapons.remove(owned_weapon)
                        break
            return None

        def pick_up_armor(self, *armor: Armor) -> None:
            for picked_up_armor in armor:
                self._armor.append(picked_up_armor)
            return None

        def drop_armor(self, *armor: Armor) -> None:
            for drop_armor in armor:
                for owned_armor in self._armor:
                    if drop_armor is owned_armor:
                        self._armor.remove(owned_armor)
                        break
            return None

        def pick_up_items(self, *items: Item) -> None:
            for picked_up_item in items:
                for owned_item in self._items:
                    if picked_up_item.name == owned_item.name:
                        owned_item.count += picked_up_item.count
                        break
                else:
                    self._items.append(picked_up_item)
            return None

        def drop_items(self, *items: Item) -> None:
            for drop_item in items:
                for owned_item in self._items:
                    if drop_item is owned_item:
                        self._items.remove(owned_item)
                        break
            return None

        def pick_up_spells(self, *spells: Spell) -> None:
            for picked_up_spell in spells:
                for owned_spell in self._spells:
                    if picked_up_spell.name == owned_spell.name:
                        break
                else:
                    self._spells.append(picked_up_spell)
            return None

        def drop_spells(self, *spells: Spell) -> None:
            for drop_spell in spells:
                for owned_spell in self._spells:
                    if drop_spell is owned_spell:
                        self._spells.remove(drop_spell)
                        break
            return None

    class Money:
        def __init__(self, owner):
            self._amount: int = 0
            self.owner = owner

        def __call__(self) -> str:
            if self._amount > 0:
                if self._amount > 99:
                    return f"${self._amount / 100:,.2f}"
                return f"{self._amount} cents"
            return "no money"

        def is_enough(self, amount: int) -> bool:
            """Tests to see if npc has enough money to cover the cost of a purchase."""
            if self._amount >= amount:
                return True
            return False

        def spend(self, amount: int) -> None:
            self._amount -= amount
            return None

        def receive(self, amount: int) -> None:
            self._amount += amount
            return None

    class Roll:
        def __init__(self, owner) -> None:
            self.owner = owner

        def strength(self) -> int:
            return Dice((self.owner.scores.strength - 10) // 2)()

        def dexterity(self) -> int:
            return Dice((self.owner.scores.dexterity - 10) // 2)()

        def intelligence(self) -> int:
            return Dice((self.owner.scores.intelligence - 10) // 2)()

        def wisdom(self) -> int:
            return Dice((self.owner.scores.wisdom - 10) // 2)()

        def charisma(self) -> int:
            return Dice((self.owner.scores.charisma - 10) // 2)()

        def constitution(self) -> int:
            return Dice((self.owner.scores.constitution - 10) // 2)()

        def initiative(self) -> int:
            return Dice(self.owner.scores.iniative)()

        def attack(self) -> int:
            return self.owner.slots.weapon.attack()

        def damage(self) -> int:
            return self.owner.slots.weapon.damage()

    def purchase(self, *containables: Weapon | Armor | Item | Spell) -> bool:
        """Method for purchasing anything that will then be added to the npc's belongings."""
        total_cost = calculate_containables_cost(*containables)
        if self.money.is_enough(total_cost):
            self.money.spend(total_cost)
            weapons, armor, items, spells = separate_containables(*containables)
            self.inventory.pick_up_weapons(*weapons)
            self.inventory.pick_up_armor(*armor)
            self.inventory.pick_up_items(*items)
            self.inventory.pick_up_spells(*spells)
            return True
        return False

    def sell(self, *containables: Weapon | Armor | Item | Spell) -> None:
        """Method for selling things the npc owns."""
        total_cost = calculate_containables_cost(*containables)
        self.money.receive(total_cost)
        weapons, armor, items, spells = separate_containables(*containables)
        for weapon in weapons:
            if weapon is self.slots.weapon:
                self.slots.stow_weapon()
                break
        for armor_piece in armor:
            if armor_piece is self.slots.armor:
                self.slots.stow_armor
                break
        self.inventory.drop_weapons(*weapons)
        self.inventory.drop_armor(*armor)
        self.inventory.drop_items(*items)
        self.inventory.drop_spells(*spells)

    def pick_up(self, *containables: Weapon | Armor | Item | Spell):
        """Method for picking up items without paying for them."""
        weapons, armor, items, spells = separate_containables(*containables)
        self.inventory.pick_up_weapons(*weapons)
        self.inventory.pick_up_armor(*armor)
        self.inventory.pick_up_items(*items)
        self.inventory.pick_up_spells(*spells)
        return self

    def drop(self, *containables: Weapon | Armor | Item | Spell) -> None:
        """Method for dropping items. Will automatically stow weapons and armor before dropping."""
        weapons, armor, items, spells = separate_containables(*containables)
        for weapon in weapons:
            if weapon is self.slots.weapon:
                self.slots.stow_weapon()
                break
        for armor_piece in armor:
            if armor_piece is self.slots.armor:
                self.slots.stow_armor
                break
        self.inventory.drop_weapons(*weapons)
        self.inventory.drop_armor(*armor)
        self.inventory.drop_items(*items)
        self.inventory.drop_spells(*spells)
        return None


player = Player("Default_Player_Name")
