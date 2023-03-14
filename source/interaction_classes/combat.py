from ..character_classes.npc import NPC
from ..character_classes.player import player
from ..funcs.listen_for_enter import listen_for_enter
from typing import Callable


class Combat:
    def __init__(self, opponent: NPC, exit_callable: Callable | None = None) -> None:
        self.opponent = opponent
        if exit_callable is not None:
            self.exit_callable = exit_callable
        else:
            self.exit_callable = self.opponent.location

    def __call__(self) -> None:
        def roll_for_initiative() -> bool:
            player_initiative = player.roll.initiative()
            opponent_initiative = self.opponent.roll.initiative()
            return player_initiative >= opponent_initiative

        listen_for_enter(message="to roll initiative")
        player_wins_initiative = roll_for_initiative()
        if player_wins_initiative:
            self.player_turn()
            return
        else:
            self.opponent_turn()
            return

    def player_turn(self):
        def player_turn_menu() -> None:
            menu_options = ["Attack", "Change weapons", "Use Spell"]
            for i, option in enumerate(menu_options):
                print(f"\t{i}. {option}")
            print(" ")
            return

        def choose_option() -> int:
            chosen_option = input("\t>  What do you want to do? [1-3]: ")
            print(" ")
            return int(chosen_option) - 1

        def call_chosen_option_by_index(index: int) -> None:
            option_callables = [attack, change_weapon, use_spell]
            option_callables[index]()
            return

        def opponent_killed() -> bool:
            if self.opponent.hp() == 0:
                return True
            return False

        def attack():
            print(f"You attack with your {player.slots.weapon.name}.")
            listen_for_enter(message="to roll attack")
            attack_roll = player.roll.attack()
            if attack_roll >= self.opponent.ac:
                listen_for_enter(message="to roll damage")
                player.slots.weapon.fire_if_applicable()
                damage_roll = player.roll.damage()
                self.opponent.hp.take_damage(damage_roll)
            if opponent_killed():
                self.victory()
            else:
                self.opponent_turn()
            return

        def change_weapon():
            pass

        def use_spell():
            pass

        try:
            player_turn_menu()
            chosen_option_index = choose_option()
            call_chosen_option_by_index(chosen_option_index)
            return

        except IndexError:
            print("You must choose from the options!")
            print(" ")
            self.player_turn()
        except ValueError:
            print("You must choose from the options!")
            self.player_turn()

    def opponent_turn(self):
        pass

    def victory(self):
        pass

    def defeat(self):
        pass
