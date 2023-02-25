from containable import Containable, dataclass
from funcs import ProxyFunc

@dataclass
class Spell(Containable):
    name: str
    weight: int
    desc: str
    effect: ProxyFunc | list[ProxyFunc]

    def cast(self, target=None):
        pass