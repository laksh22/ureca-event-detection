import numpy as np

from utilities.utils import get_distance, get_direction, get_mean


class ObjectData:
    # Constructor
    def __init__(self, point):
        self.curr_point = point
        self.prev_point = None
        self.curr_speed = None
        self.prev_speed = None
        self.curr_direction = None
        self.prev_direction = None
        self.speed = None
        self.direction = None
        self.mapper = None

    # TODO: Use smoothing algorithm
    def update_object(self, point):
        self.prev_point = self.curr_point
        self.curr_point = point

    def get_position(self):
        return self.get_mapped_curr()

    def get_speed(self):
        mapped_prev, mapped_curr = self.get_mapped_prev(), self.get_mapped_curr()
        if(self.prev_speed == None):
            self.curr_speed = get_distance(mapped_prev, mapped_curr)
        else:
            self.curr_speed = get_mean(
                self.prev_speed, get_distance(mapped_prev, mapped_curr))
        return self.curr_speed

    def get_direction(self):
        mapped_prev, mapped_curr = self.get_mapped_prev(), self.get_mapped_curr()
        if(self.prev_direction == None):
            self.curr_direction = get_distance(mapped_prev, mapped_curr)
        else:
            self.curr_direction = get_mean(
                self.prev_direction, get_distance(mapped_prev, mapped_curr))
        return self.curr_direction

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
