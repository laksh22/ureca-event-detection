import math
import numpy as np
import pandas as pd


def get_distance(p1, p2):
    return math.sqrt(((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2))


def get_direction(p1, p2):
    return math.degrees(math.atan2(p2[1]-p1[1], p2[0]-p1[0]))


def get_mean(values):
    return sum(values)/len(values)


def get_median(values):
    mid = len(values) // 2
    if len(values) % 2 == 1:  # check if the len of list is odd
        return sorted(values)[mid]
    else:
        return 0.5 * np.sum(sorted(values)[mid - 1:mid + 1])


def get_mad(values):
    df = pd.DataFrame()
    df["values"] = values
    return df["values"].mad()


def is_anomalous(value, median, mad):
    z_score = 0.6745*(value-median)/mad
    if(abs(z_score) > 3.75):
        return True
    return False
