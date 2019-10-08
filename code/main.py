import cv2
import numpy as np
from yolo_detector import yolo_detect

capture = cv2.VideoCapture('../data/aic19-track3-train-data/6.mp4')
car_cascade = cv2.CascadeClassifier("../data/cars.xml")


while True:
    _, frame = capture.read()

    detected = yolo_detect(frame)

    cv2.imshow("Detections", detected)

    key = cv2.waitKey(30) & 0xff
    if key == 27:
        break

capture.release()
cv2.destroyAllWindows()
