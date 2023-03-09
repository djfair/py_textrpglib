from ..character_classes.npc import NPC
from ..interaction_classes.multiple_choice import MultipleChoice
from ..containable_classes.armor import Armor
from ..containable_classes.weapon import Weapon
from ..containable_classes.spell import Spell
from ..containable_classes.item import Item


class Location:
    def __init__(self, name: str, entrance_message: str) -> None:
        self.name = name
        self.entrance_message = entrance_message
        self.buildings: list = []
        self.nearby_locations: list = []

    def __call__(self):
        pass

    class Building:
        def __init__(self, name: str, location) -> None:
            self.name = name
            self.desc: str
            self.entrance_message: str
            self.proprietor: NPC
            self.population: list[NPC] = []
            self.environmental_items: list[Item | Armor | Weapon | Spell] = []
            self.location = location

        def populate(self, *npc: NPC):
            for current_npc in npc:
                self.population.append(current_npc)
            return self

        def add_envionrmental_items(self, *items):
            for item in items:
                self.environmental_items.append(item)

    def add_building(
        self, name: str, desc: str, entrance_message: str, proprieter: NPC
    ):
        new_building = self.Building(name=name, location=self)
        new_building.desc = desc
        new_building.proprietor = proprieter
        new_building.entrance_message = entrance_message
        self.buildings.append(new_building)
        return new_building
