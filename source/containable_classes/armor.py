from containable import Containable, dataclass

@dataclass
class Armor(Containable):
    mod: int