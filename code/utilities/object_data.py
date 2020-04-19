from utilities.utils import get_distance, get_direction


class ObjectData:
    # Constructor
    def __init__(self, point):
        self.curr_point = point
        self.prev_point = None
        self.speed = None
        self.direction = None

    def update_object(self, point):
        self.prev_point = self.curr_point
        self.curr_point = point
        self.speed = get_distance(self.prev_point, self.curr_point)
        self.direction = get_direction(self.prev_point, self.curr_point)

    def get_speed(self):
        return self.speed

    def get_direction(self):
        return self.direction
