import matplotlib.path as mPath
import numpy as np

from utilities.utils import get_median
from utilities.perspective import Perspective


class RoadData:
    # Constructor
    def __init__(self, id, boundaries):
        self.id = id
        self.boundaries = boundaries
        self.speed_list = []
        self.direction_list = []
        self.traffic_list = []
        self.current_traffic_count = 0

        self.perspective = Perspective(boundaries)
        self.path = mPath.Path(self.perspective.dst)

    # Constructor for testing stage
    def set_trained_params(self, speed, direction, traffic):
        self.speed = speed
        self.direction = direction
        self.traffic = traffic

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
        pts = np.array([[pts[0], pts[1]]], dtype='float32')
        pts = np.array([pts])
        pts = self.perspective.transform_pts(pts)[0][0]
        return self.path.contains_point([pts[0], pts[1]])

    def debug(self):
        print(
            f'ID: {self.get_id()} | Speed : {self.get_median_speed()} | Direction: {self.get_median_direction()} | Traffic: {self.get_median_traffic()}')

    def debug_trained(self):
        print(
            f'ID: {self.get_id()} | Speed : {self.speed} | Direction: {self.direction} | Traffic: {self.traffic}')
