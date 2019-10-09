import cv2
import numpy as np

car_cascade = cv2.CascadeClassifier("../data/cars.xml")


def haar_detect(frame):
    haar_frame = frame.copy()

    gray = cv2.cvtColor(haar_frame, cv2.COLOR_BGR2GRAY)

    cars = car_cascade.detectMultiScale(gray, 1.1, 1)

    for(x, y, w, h) in cars:
        cv2.rectangle(haar_frame, (x, y), (x+w, y+h), (0, 0, 255), 2)

    return haar_frame
