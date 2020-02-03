import cv2
import numpy as np
import pandas as pd
import math
import random

prev = -1
curr = -1
start = -1
shapes = [[]]
color = (255, 0, 0)

def get_road_polygons(background):

    def get_distance(p1, p2):
        return math.sqrt( ((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2) )

    def click_event(event, x, y, flags, param):
        global curr
        global prev
        global color
        global start
        font = cv2.FONT_HERSHEY_SIMPLEX

        if event == cv2.EVENT_LBUTTONDOWN:
            if curr == -1:
                curr = (x, y)
                start = curr

                strID = str(len(shapes))
                cv2.putText(img, strID, (x, y), font, 1, (255, 255, 0), 2)
            else:
                prev = curr
                curr = (x, y)
                shapes[len(shapes)-1].append(curr)
                if(get_distance(start, curr) > 10):
                    cv2.line(img, prev, curr, color, 2)
                else:
                    cv2.line(img, prev, start, color, 2)
                    shapes.append([])
                    curr = -1
                    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

            cv2.imshow('image', img)

    img = background
    cv2.imshow('image', img)

    cv2.setMouseCallback('image', click_event)

    while(True):
        cv2.setMouseCallback('image', click_event)
        cv2.imshow('image', img)
        k=cv2.waitKey(1) & 0xFF
        if k==27: #Escape KEY
            break

        cv2.imshow('image', img)

    cv2.destroyAllWindows()

    return shapes


def draw(frame, same, color=(0, 0, 255)):
    for index, row in same.iterrows():
        cv2.circle(frame, (int(row.x), int(row.y)), 2, color, 2)
    return frame

def draw_arrow(frame, point, color=(0, 255, 0)):
    cv2.arrowedLine(frame, (int(point[0]), int(point[1])), (int(point[0])+20, int(point[1])+20), color, 2)
    return frame

def get_color_dict(df):
    clusters = df.cluster.unique()
    d = dict((i, (rand_rgb(), rand_rgb(), rand_rgb())) for i in clusters)
    return d

def rand_rgb():
    return random.random()*10*255%255