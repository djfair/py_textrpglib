from .containable import Containable, dataclass
from typing import Callable


@dataclass
class Spell(Containable):
    name: str
    desc: str
    effects: tuple[Callable]

    def cast(self, target=None):
        for effect in self.effects:
            effect()
