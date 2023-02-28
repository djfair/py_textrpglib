from ..character_classes.npc import NPC
from ..character_classes.player import player
from ..containable_classes.armor import Armor
from ..containable_classes.item import Item
from ..containable_classes.weapon import Weapon
from ..containable_classes.spell import Spell
from typing import Callable


class Trade:
    def __init__(self, npc: NPC, exit_callable: Callable | None = None) -> None:
        self.npc: NPC = npc
        if exit_callable is None:
            self.exit_callable: Callable = self.npc
        else:
            self.exit_callable: Callable = exit_callable

    def __call__(self):
        try:
            for i, option in enumerate(["Buy", "Sell", "Go back"]):
                print(f"\t{i + 1}. {option}")
            print(" ")
            chosen_option = int(input("\t>  What do you want to do? [1-3]: ")) - 1
            print(" ")
            [self.player_buying, self.player_selling, self.exit_callable][
                chosen_option
            ]()
        except TypeError:
            print(" ")
            print(f"\t{self.npc.name} has nothing left to sell you.")
            print(" ")
            return self()
        except ValueError:
            print(" ")
            print("You must choose one of the options!")
            print(" ")
            return self()
        except IndexError:
            print("You must choose one of the options!")
            print(" ")
            return self()

    def player_buying(self):
        try:
            player_buyables: list[Armor | Item | Weapon | Spell] = []
            player_buyables.append(
                *self.npc.inventory(), *self.npc.weapons(), *self.npc.spells()
            )
            for i, buyable in enumerate(player_buyables):
                print(
                    f"\t{i + 1}. {buyable.name.capitalize()} (${buyable.cost / 100:,.2f})"
                )
            print(" ")
            chosen_buyable = (
                int(
                    input(
                        f"\t>  What would you like to buy? [1-{len(player_buyables)}]: "
                    )
                )
                - 1
            )
            print(" ")
            chosen_buyable = player_buyables[chosen_buyable]
            if isinstance(chosen_buyable, Item) and chosen_buyable.count > 1:
                chosen_count = int(
                    input(
                        f"\t>  How many would you like to buy? [1-{chosen_buyable.count}] "
                    )
                )
                print(" ")
                chosen_buyable = chosen_buyable.copy().set_count(chosen_count)
            purchase_success = player.purchase(chosen_buyable)
            if not purchase_success:
                print("\tInsufficient funds!")
                print(" ")
                return self()
            if isinstance(chosen_buyable, Item):
                print(
                    f"\tBought {chosen_buyable.count} x {chosen_buyable.name} for "
                    f"${(chosen_buyable.cost / 100) * chosen_buyable.count:,.2f}"
                )
                print(" ")
                self.npc.money.receive(chosen_buyable.cost * chosen_buyable.count)
            else:
                print(
                    f"\tBought {chosen_buyable.name} for {chosen_buyable.cost / 100:,.2f}"
                )
                print(" ")
                self.npc.money.receive(chosen_buyable.cost)
            if (
                chosen_buyable.name in player.weapons.failed.keys()
                or chosen_buyable.name in player.inventory.failed.keys()
                or chosen_buyable.name in player.spells.failed.keys()
            ):
                print(
                    "\tYou go to stow your new purchase away, but as you do, you notice you "
                    f"already own it. You ask for a refund but {self.npc.name} refuses, and "
                    "you leave the dead weight next to you."
                )
                print(" ")
            if isinstance(chosen_buyable, (Item, Armor)):
                self.npc.inventory.remove(chosen_buyable)
            if isinstance(chosen_buyable, Weapon):
                self.npc.weapons.remove(chosen_buyable)
            if isinstance(chosen_buyable, Spell):
                self.npc.spells.remove(chosen_buyable)
            return self()
        except TypeError:
            print(f"\t{self.npc.name} has nothing left to sell you.")
            print(" ")
            return self()
        except ValueError:
            print(" ")
            print("You must choose one of the options!")
            print(" ")
            return self.player_buying()
        except IndexError:
            print("You must choose one of the options!")
            print(" ")
            return self.player_buying()

    def player_selling(self):
        try:
            player_sellables: list[Armor | Item | Weapon | Spell] = []
            player_sellables.append(
                *player.inventory(), *player.weapons(), *player.spells()
            )
            for i, sellable in enumerate(player_sellables):
                print(
                    f"\t{i + 1}. {sellable.name.capitalize()} (${sellable.cost / 100:,.2f})"
                )
            print(" ")
            chosen_sellable = (
                int(
                    input(
                        f"\t>  What would you like to sell? [1-{len(player_sellables)}]: "
                    )
                )
                - 1
            )
            print(" ")
            chosen_sellable = player_sellables[chosen_sellable]
            if isinstance(chosen_sellable, Item) and chosen_sellable.count > 1:
                chosen_count = int(
                    input(
                        f"\t>  How many would you like to sell? [1-{chosen_sellable.count}] "
                    )
                )
                print(" ")
                chosen_sellable = chosen_sellable.copy().set_count(chosen_count)
            sale_success = self.npc.purchase(chosen_sellable)
            if not sale_success:
                print(f"\t{self.npc.name} can't afford it!")
                print(" ")
                return self()
            if isinstance(chosen_sellable, (Item, Armor)):
                player.inventory.remove(chosen_sellable)
            if isinstance(chosen_sellable, Weapon):
                player.weapons.remove(chosen_sellable)
            if isinstance(chosen_sellable, Spell):
                player.spells.remove(chosen_sellable)
            if isinstance(chosen_sellable, Item):
                print(
                    f"\tSold {chosen_sellable.count} x {chosen_sellable.name} for "
                    f"${(chosen_sellable.cost / 100) * chosen_sellable.count:,.2f}"
                )
                print(" ")
                player.money.receive(chosen_sellable.cost * chosen_sellable.count)
            else:
                print(
                    f"\tSold {chosen_sellable.name} for {chosen_sellable.cost / 100:,.2f}"
                )
                print(" ")
                player.money.receive(chosen_sellable.cost)
            return self()
        except TypeError:
            print(f"\tYou have nothing left to sell to {self.npc.name}.")
            print(" ")
            return self()
        except ValueError:
            print(" ")
            print("You must choose one of the options!")
            print(" ")
            return self.player_buying()
        except IndexError:
            print("You must choose one of the options!")
            print(" ")
            return self.player_buying()
