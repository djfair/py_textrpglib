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

    def __call__(self) -> None:
        """Method for calling trade dialog screen."""

        def show_menu() -> None:
            """Cycles through options and prints to terminal."""

            for i, option in enumerate(["Buy", "Sell", "Go back"]):
                print(f"\t{i + 1}. {option}")
            print(" ")

        def choose_menu_option() -> int:
            """Asks player for input and modifies to match 0-indexing."""

            chosen_option = int(input("\t>  What do you want to do? [1-3]: ")) - 1
            print(" ")
            return chosen_option

        def call_chosen_option(chosen_option_index: int) -> None:
            """Calls other Trade dialog screens or exit_callable based on player choice."""

            callables = [self.player_buying, self.player_selling, self.exit_callable]
            return callables[chosen_option_index]()

        try:
            show_menu()
            chosen_option_index = choose_menu_option()
            call_chosen_option(chosen_option_index)

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
        """Method for presenting buying options to player, and executing on trade."""

        def present_buyables():
            """Cycles through buyables in npc's inventory and prints to terminal. If inventory
            is empty, returns to trade dialog main menu."""

            if len(self.npc.inventory()) > 0:
                for i, buyable in enumerate(self.npc.inventory()):
                    print(
                        f"{i + 1}. {buyable.name.capitalize()} (${buyable.cost / 100:,.2f})"
                    )
                print(" ")
                return
            else:
                print(f"\t{self.npc.name} has nothing left to sell to you.")
                print(" ")
                return self()

        def choose_buyable() -> int:
            """Asks player for input on what to buy. Modifies player response to match
            0-indexing."""

            chosen_buyable_index = input(
                f"\t>  What would you like to buy? [1-{len(self.npc.inventory())}]: "
            )
            print(" ")
            return int(chosen_buyable_index) - 1

        def lookup_buyable_by_index(index: int) -> Weapon | Armor | Item | Spell:
            """Looks up buyable by index in npc's inventory."""
            return self.npc.inventory()[index]

        def choose_count_if_applicable(buyable: Item) -> int:
            """If buyable count > 1, asks for input from player as to how many to buy.
            Otherwise returns 1."""

            if buyable.count > 1:
                chosen_count = int(
                    input(f"\t>  How many would you like to buy? [1-{buyable.count}] ")
                )
                print(" ")
                return chosen_count
            return 1

        def purchase_sucess(successful_purchase: Weapon | Armor | Item | Spell) -> None:
            """Prints to terminal a message upon a successful purchase."""

            if isinstance(successful_purchase, Item):
                print(
                    f"Bought {successful_purchase.count} {successful_purchase.name} for",
                    f"{successful_purchase.cost} each.",
                )
                print(" ")
            else:
                print(
                    f"Bought {successful_purchase.name} for {successful_purchase.cost}."
                )
                print(" ")
            return

        def purchase_failure(failed_purchase: Weapon | Armor | Item | Spell) -> None:
            """Prints to terminal a message upon a failed purchase."""

            print(
                f"Couldn't buy {failed_purchase.name} for {failed_purchase.cost}:",
                "insufficient funds!",
            )
            print(" ")
            return

        try:
            present_buyables()
            chosen_buyable_index = choose_buyable()
            chosen_buyable = lookup_buyable_by_index(chosen_buyable_index)

            if isinstance(chosen_buyable, Item):
                chosen_count = choose_count_if_applicable(chosen_buyable)
                chosen_buyable = chosen_buyable.copy().set_count(chosen_count)
            else:
                chosen_buyable = chosen_buyable.copy()

            if player.purchase(chosen_buyable):
                purchase_sucess(chosen_buyable)
                self.npc.sell(chosen_buyable)
            else:
                purchase_failure(chosen_buyable)
            return self()

        except ValueError:
            print("You must choose one of the options!")
            print(" ")
            return self.player_buying()

        except IndexError:
            print("You must choose one of the options!")
            print(" ")
            return self.player_buying()

    def player_selling(self):
        """Method for presenting selling options to player, and to execute on trade."""

        def present_sellables():
            """Cycles through sellables in player's inventory and prints to terminal. If
            inventory is empty, returns to trade dialog main menu."""

            if len(player.inventory()) > 0:
                for i, sellable in enumerate(player.inventory()):
                    print(
                        f"{i + 1}. {sellable.name.capitalize()} (${sellable.cost / 100:,.2f})"
                    )
                print(" ")
                return None
            else:
                print(f"\tYou have nothing left to sell.")
                print(" ")
                return self()

        def choose_sellable() -> int:
            """Asks player for input on what to buy. Modifies player response to match
            0-indexing."""

            chosen_sellable_index = input(
                f"\t>  What would you like to sell? [1-{len(player.inventory())}]: "
            )
            print(" ")
            return int(chosen_sellable_index) - 1

        def lookup_sellable_by_index(index: int) -> Weapon | Armor | Item | Spell:
            """Looks up sellable by index in player's inventory."""
            return player.inventory()[index]

        def choose_count_if_applicable(sellable: Item) -> int:
            """If buyable count > 1, asks for input from player as to how many to buy.
            Otherwise returns 1."""

            if sellable.count > 1:
                chosen_count = int(
                    input(
                        f"\t>  How many would you like to sell? [1-{sellable.count}] "
                    )
                )
                print(" ")
                return chosen_count
            return 1

        def sale_sucess(successful_sale: Weapon | Armor | Item | Spell) -> None:
            """Prints to terminal a message upon a successful sale."""

            if isinstance(successful_sale, Item):
                print(
                    f"Sold {successful_sale.count} {successful_sale.name} for",
                    f"${successful_sale.cost / 100:,.2f} each.",
                )
                print(" ")
            else:
                print(
                    f"Sold {successful_sale.name} for ${successful_sale.cost / 100:,.2f}."
                )
                print(" ")
            return None

        def sale_failure(failed_sale: Weapon | Armor | Item | Spell):
            """Prints to terminal a message upon a failed sale."""

            print(
                f"Couldn't sell {failed_sale.name} for ${failed_sale.cost / 100:,.2f}:",
                f"{self.npc.name} has insufficient funds!",
            )
            print(" ")
            return None

        try:
            present_sellables()
            chosen_sellable_index = choose_sellable()
            chosen_sellable = lookup_sellable_by_index(chosen_sellable_index)

            if isinstance(chosen_sellable, Item):
                chosen_count = choose_count_if_applicable(chosen_sellable)
                chosen_sellable = chosen_sellable.copy().set_count(chosen_count)
            else:
                chosen_sellable = chosen_sellable.copy()

            if player.purchase(chosen_sellable):
                sale_sucess(chosen_sellable)
                self.npc.sell(chosen_sellable)
            else:
                sale_failure(chosen_sellable)
            return self.player_selling()

        except ValueError:
            print("You must choose one of the options!")
            print(" ")
            return self.player_selling()

        except IndexError:
            print("You must choose one of the options!")
            print(" ")
            return self.player_selling()
