import cv2
import math
import random
import numpy as np
import pandas as pd

from utilities.utils import get_distance


class DrawTool:
    def __init__(self):
        self.prev = -1
        self.curr = -1
        self.start = -1
        self.shapes = [[]]
        self.color = (255, 0, 0)

    def draw_coordinates(self, frame, frame_objects, color=(0, 0, 255)):
        coordinate_frame = np.zeros(
            (frame.shape[:2][0], frame.shape[:2][1], 3), np.uint8)
        for index, row in frame_objects.iterrows():
            cv2.circle(coordinate_frame, (int(row.x), int(row.y)), 2, color, 2)
        return coordinate_frame

    def draw_anomalies(self, frame, frame_objects, color=(0, 0, 255)):
        coordinate_frame = np.zeros(
            (frame.shape[:2][0], frame.shape[:2][1], 3), np.uint8)
        for index, row in frame_objects.iterrows():
            if row.type == "stall":
                color = (0, 255, 0)
            elif row.type == "speed":
                color = (0, 0, 255)
            elif row.type == "direction":
                color = (255, 0, 0)
            elif row.type == "traffic":
                color = (255, 255, 0)
            cv2.circle(coordinate_frame, (int(row.x), int(row.y)), 2, color, 2)
        return coordinate_frame

    def get_road_boundaries(self, background):
        self.img = cv2.resize(
            background, (int(background.shape[:2][1]/2), int(background.shape[:2][0]/2)))

        cv2.setMouseCallback('image', self.click_event)

        while(True):
            cv2.setMouseCallback('image', self.click_event)
            cv2.imshow('image', self.img)
            k = cv2.waitKey(1) & 0xFF
            if k == 27:  # Escape KEY
                break

        cv2.destroyAllWindows()

        return np.asarray(self.shapes[:-1])*2

    def click_event(self, event, x, y, flags, param):
        font = cv2.FONT_HERSHEY_SIMPLEX

        if event == cv2.EVENT_LBUTTONDOWN:
            if self.curr == -1:
                self.curr = (x, y)
                self.start = self.curr
                self.shapes[len(self.shapes)-1].append(self.curr)

                strID = str(len(self.shapes))
                cv2.putText(self.img, strID, (x, y), font, 1, (255, 255, 0), 2)
            else:
                self.prev = self.curr
                self.curr = (x, y)
                self.shapes[len(self.shapes)-1].append(self.curr)
                if(get_distance(self.start, self.curr) > 10 and len(self.shapes[len(self.shapes)-1]) <= 4):
                    cv2.line(self.img, self.prev, self.curr, self.color, 2)
                else:
                    cv2.line(self.img, self.prev, self.start, self.color, 2)
                    self.shapes[len(self.shapes)-1].pop()
                    self.shapes.append([])
                    self.curr = -1
                    self.color = (random.randint(0, 255), random.randint(
                        0, 255), random.randint(0, 255))

            cv2.imshow('image', self.img)
