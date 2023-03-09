"""
py_textrpglib
: A text-based role-playing game library for Python developers

Number formatting rules
: Money is given in US dollar cent amounts.
: Weight is given in grams.
"""

from .character_classes.player import player
from .character_classes.npc import NPC
from .containable_classes.armor import Armor
from .containable_classes.item import Item
from .containable_classes.spell import Spell
from .containable_classes.weapon import Weapon
from .funcs.proxy_callable import ProxyCallable
from .funcs.listen_for_enter import listen_for_enter
from .interaction_classes.ability_check import AbilityCheck
from .interaction_classes.dialog_branch import DialogBranch
from .interaction_classes.multiple_choice import MultipleChoice
from .interaction_classes.trade import Trade
from .dice_class.dice import Dice
from .location_classes.location import Location
from .location_classes.world_map import world_map


__all__ = [
    "player",
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
    "Trade",
    "Location",
    "world_map",
]
