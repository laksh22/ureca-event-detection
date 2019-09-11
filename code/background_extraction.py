# Background extraction using running average
import cv2
import numpy as np

cap = cv2.VideoCapture('../data/aic19-track3-train-data/2.mp4')
_, frame = cap.read()

average = np.float32(frame)

while True:
    _, frame = cap.read()

    cv2.accumulateWeighted(frame, average, 0.01)

    res = cv2.convertScaleAbs(average)

    cv2.imshow('Video', frame)
    cv2.imshow('Clean Plate', res)

    k = cv2.waitKey(20)

    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
