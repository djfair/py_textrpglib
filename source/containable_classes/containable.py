from dataclasses import dataclass
from copy import deepcopy


@dataclass
class Containable:
    name: str
    cost: int
    desc: str

    def copy(self):
        return deepcopy(self)
