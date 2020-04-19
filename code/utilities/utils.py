import math
import numpy as np


def get_distance(p1, p2):
    return math.sqrt(((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2))


def get_direction(p1, p2):
    return math.atan2(p2[1]-p1[1], p2[0]-p1[0])


def get_median(xs):
    mid = len(xs) // 2
    if len(xs) % 2 == 1:  # check if the len of list is odd
        return sorted(xs)[mid]
    else:
        return 0.5 * np.sum(sorted(xs)[mid - 1:mid + 1])
