import pandas as pd
import cv2
import random

def draw(frame, same, color=(0, 0, 255)):
    for index, row in same.iterrows():
        cv2.circle(frame, (int(row.x), int(row.y)), 2, color, 2)
    return frame

def get_color_dict(df):
    clusters = df.cluster.unique()
    d = dict((i, (rand_rgb(), rand_rgb(), rand_rgb())) for i in clusters)
    return d

def rand_rgb():
    return random.random()*10*255%255