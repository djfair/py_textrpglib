"""
py_textrpglib
: A text-based role-playing game library for Python developers

Number formatting rules
: Money is given in US dollar cent amounts.
: Weight is given in grams.
"""

from .character_classes import Player, NPC
from .containable_classes import Armor, Item, Spell, Weapon
from .funcs import ProxyCallable, listen_for_enter
from .interaction_classes import AbilityCheck, DialogBranch, MultipleChoice
from .dice import Dice


__all__ = [
    "Player",
    "NPC",
    "Armor",
    "Item",
    "Spell",
    "Weapon",
    "ProxyCallable",
    "listen_for_enter",
    "Dice",
    "AbilityCheck",
    "DialogBranch",
    "MultipleChoice",
    "player",
]

player = Player("Default_Player_Name")
