# Background extraction using running average
import cv2
import numpy as np


def extract_background(frame, average):
    cv2.accumulateWeighted(frame, average, 0.01)
    res = cv2.convertScaleAbs(average)
    return res, average