from ..character_classes.npc import NPC
from ..interaction_classes.multiple_choice import MultipleChoice


class Building:
    def __init__(
        self, name: str, desc: str, proprietor: NPC, entrance_message: str = ""
    ):
        self.name = name
        self.desc = desc
        self.proprietor = proprietor
        self.population: list = []
        self.entrance_message = entrance_message

    def populate(self, *npc):
        for npc in npc:
            self.population.append(npc)
