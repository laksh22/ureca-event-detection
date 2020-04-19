import matplotlib.path as mPath

from utilities.utils import get_median


class RoadData:
    # Constructor
    def __init__(self, id, boundaries):
        self.id = id
        self.boundaries = boundaries
        self.speed_list = []
        self.direction_list = []
        self.traffic_list = []
        self.current_traffic_count = 0
        self.path = mPath.Path(self.boundaries)

    def update_traffic_count(self):
        self.current_traffic_count += 1

    def add_speed(self, speed):
        self.speed_list.append(speed)

    def add_direction(self, direction):
        self.direction_list.append(direction)

    def add_traffic(self):
        self.traffic_list.append(self.current_traffic_count)
        self.current_traffic_count = 0

    def get_median_speed(self):
        return get_median(self.speed_list)

    def get_median_direction(self):
        return get_median(self.direction_list)

    def get_median_traffic(self):
        return get_median(self.traffic_list)

    def get_boundaries(self):
        return self.boundaries

    def get_id(self):
        return self.id

    def contains(self, pts):
        return self.path.contains_point([pts[0], pts[1]])

    def debug(self):
        print(
            f'ID: {self.get_id()} | Speed : {self.get_median_speed()} | Direction: {self.get_median_direction()} | Traffic: {self.get_median_traffic()}')
