from .containable import Containable, dataclass
from typing import Callable


@dataclass
class Spell(Containable):
    name: str
    desc: str
    effect: Callable

    def cast(self):
        self.effect()
