import matplotlib.path as mPath
import numpy as np

from utilities.utils import get_median, get_mad, is_anomalous
from utilities.perspective import Perspective


class RoadData:
    # Constructor
    def __init__(self, road_id, boundaries):
        self.id = road_id
        self.boundaries = boundaries
        self.speed_list = []
        self.direction_list = []
        self.traffic_list = []
        self.current_traffic_count = 0

        self.perspective = Perspective(boundaries)
        self.path = mPath.Path(self.perspective.dst)

    # Constructor for testing stage
    def set_trained_params(self, speed, direction, traffic, speed_mad, direction_mad, traffic_mad):
        self.speed = speed
        self.direction = direction
        self.traffic = traffic
        self.speed_mad = speed_mad
        self.direction_mad = direction_mad
        self.traffic_mad = traffic_mad

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

    def get_mad_speed(self):
        return get_mad(self.speed_list)

    def get_mad_direction(self):
        return get_mad(self.direction_list)

    def get_mad_traffic(self):
        return get_mad(self.traffic_list)

    def get_latest_traffic_level(self):
        return self.traffic_list[len(self.traffic_list)-1]

    def get_boundaries(self):
        return self.boundaries

    def get_id(self):
        return self.id

    def check_anomalous_speed(self, object_speed):
        return is_anomalous(object_speed, self.speed, self.speed_mad)

    def check_anomalous_direction(self, object_direction):
        diff = self.direction-object_direction
        if diff > 150 or diff < -150:
            return True
        return False

    def check_anomalous_traffic(self):
        latest_traffic = self.get_latest_traffic_level()
        return is_anomalous(latest_traffic, self.traffic, self.traffic_mad)

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
