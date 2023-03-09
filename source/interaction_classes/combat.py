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

    def __call__(self):
        listen_for_enter(message="to roll initiative")
        if player.roll.initiative() > self.opponent.roll.initiative():
            self.player_turn()
        else:
            self.opponent_turn()

    def player_turn(self):
        try:
            menu_options = ["Attack", "Change weapon", "Use spell"]
            for i, menu_option in enumerate(menu_options):
                print(f"\t{i + 1}. {menu_option}")
            print(" ")
            chosen_option = int(input("\t> What you want to do? [1-3]: ")) - 1
            print(" ")
            if chosen_option == 0:  # Attack
                print(f"You use your {player.slots.weapon.name} to attack.")
                print(" ")
                listen_for_enter(message="to roll attack")
                if player.roll.attack() >= self.opponent.ac:
                    print("You hit!")
                    print(" ")
                    listen_for_enter(message="to roll damage")
                    damage = player.roll.damage()
                    player.slots.weapon.fire()  # If applicable
                    self.opponent.hp.take_damage(damage)
                    print(f"Opponent {self.opponent.name} took {damage} damage.")
                    print(" ")
                    if self.opponent.hp() <= 0:
                        return self.victory()
                    return self.opponent_turn()
            elif chosen_option == 1:  # Change weapon
                for i, weapon in enumerate(player.weapons()):
                    print(f"\t{i + 1}. {weapon.name}")
                    print(" ")
                chosen_option = int(input("\t> What you want to equip? [1-3]: ")) - 1
                print(" ")
                player.slots.equip(player.weapons()[chosen_option])
                print(f"You equipped {player.weapons()[chosen_option].name}.")
                print(" ")
                return self.opponent_turn()
            elif chosen_option == 2:  # Use spell
                for i, spell in enumerate(player.spells()):
                    print(f"\t{i + 1}. {spell.name}")
                    print(" ")
                chosen_option = int(input("\t> What you want to cast? [1-3]: ")) - 1
                print(" ")
                player.spells()[chosen_option].cast()
                return self.opponent_turn()
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
