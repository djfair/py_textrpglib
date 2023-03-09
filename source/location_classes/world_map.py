from .location import Location


class WorldMap:
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(WorldMap, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.locations: dict[Location, list[tuple[Location, int, str]]] = {}

    def add_relationship(
        self,
        location_a: Location,
        location_b: Location,
        distance: int,
        direction_a_to_b: str,
    ):
        if location_a not in self.locations.keys():
            self.locations[location_a] = []
        self.locations[location_a].append((location_b, distance, direction_a_to_b))

        direction_b_to_a: str = ""
        opposing_directions = [("N", "S"), ("E", "W"), ("NW", "SE"), ("NE", "SW")]
        for direction_pair in opposing_directions:
            for i, direction in enumerate(direction_pair):
                if direction_a_to_b == direction:
                    direction_b_to_a = direction_pair[1 if i == 0 else 0]

        if location_b not in self.locations.keys():
            self.locations[location_b] = []
        self.locations[location_b].append((location_a, distance, direction_b_to_a))

        return self


world_map = WorldMap()
