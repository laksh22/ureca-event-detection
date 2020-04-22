import numpy as np

from utilities.utils import get_distance, get_direction


class ObjectData:
    # Constructor
    def __init__(self, point):
        self.curr_point = point
        self.prev_point = None
        self.speed = None
        self.direction = None
        self.mapper = None

    def update_object(self, point):
        self.prev_point = self.curr_point
        self.curr_point = point

    def get_position(self):
        return self.get_mapped_curr()

    def get_speed(self):
        mapped_prev, mapped_curr = self.get_mapped_prev(), self.get_mapped_curr()
        return get_distance(mapped_prev, mapped_curr)

    def get_direction(self):
        mapped_prev, mapped_curr = self.get_mapped_prev(), self.get_mapped_curr()
        return get_direction(mapped_prev, mapped_curr)

    def get_mapped_prev(self):
        mapping_input_prev = np.array([np.array(
            [[self.prev_point[0], self.prev_point[1]]], dtype='float32')])
        mapped_prev = self.mapper.transform_pts(mapping_input_prev)[0][0]
        return [mapped_prev[0], mapped_prev[1]]

    def get_mapped_curr(self):
        mapping_input_curr = np.array([np.array(
            [[self.curr_point[0], self.curr_point[1]]], dtype='float32')])
        mapped_curr = self.mapper.transform_pts(mapping_input_curr)[0][0]

        return [mapped_curr[0], mapped_curr[1]]
