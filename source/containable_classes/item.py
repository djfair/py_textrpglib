from containable import Containable, dataclass


@dataclass
class Item(Containable):
    count: int = 1

    def set_count(self, count: int):
        self.count = count
        return self
