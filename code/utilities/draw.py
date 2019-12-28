import pandas as pd
import cv2

def draw(frame, same):
    for index, row in same.iterrows():
        cv2.circle(frame, (int(row.x), int(row.y)), 2, (0, 0, 255), 2)
    return frame