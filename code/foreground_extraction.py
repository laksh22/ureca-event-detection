# MOG moving object detection
import cv2
import numpy as np

cap = cv2.VideoCapture('../data/aic19-track3-train-data/3.mp4')
fgbg = cv2.createBackgroundSubtractorMOG2()

while True:
    _, frame = cap.read()
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame = cv2.GaussianBlur(gray_frame, (5, 5), 0)

    fgmask = fgbg.apply(gray_frame)
    _, fgmask = cv2.threshold(fgmask, 5, 255, cv2.THRESH_BINARY)

    cv2.imshow("Original", frame)
    cv2.imshow("Fg", fgmask)

    key = cv2.waitKey(30) & 0xff
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
