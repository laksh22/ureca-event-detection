import cv2
import numpy as np

capture = cv2.VideoCapture('../data/aic19-track3-train-data/3.mp4')
car_cascade = cv2.CascadeClassifier("../data/cars.xml")


while True:
    _, frame = capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    cars = car_cascade.detectMultiScale(gray, 1.1, 1)

    for(x, y, w, h) in cars:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)

    cv2.imshow("Cars", frame)

    key = cv2.waitKey(30) & 0xff
    if key == 27:
        break

capture.release()
cv2.destroyAllWindows()
