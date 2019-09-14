# Create road mask based on moving vehicles
# TODO: Too much noise in black and white output
import cv2
import numpy as np

cap = cv2.VideoCapture('../data/aic19-track3-train-data/3.mp4')
fgbg = cv2.createBackgroundSubtractorMOG2()

_, frame = cap.read()
gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
gray_frame = cv2.GaussianBlur(gray_frame, (5, 5), 0)

mask = fgbg.apply(gray_frame)
_, mask = cv2.threshold(mask, 5, 255, cv2.THRESH_BINARY)
mask = cv2.bitwise_not(mask)

while True:
    _, frame = cap.read()
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame = cv2.GaussianBlur(gray_frame, (5, 5), 0)

    fgmask = fgbg.apply(gray_frame)
    _, fgmask = cv2.threshold(fgmask, 5, 255, cv2.THRESH_BINARY)

    mask = cv2.add(mask, fgmask)

    cv2.imshow("Original", frame)
    cv2.imshow("Fgmask", fgmask)
    cv2.imshow("Mask", mask)

    key = cv2.waitKey(30) & 0xff
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
