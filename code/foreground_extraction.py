# MOG moving object detection
import cv2
import numpy as np

capture = cv2.VideoCapture('../data/aic19-track3-train-data/3.mp4')
subtractor = cv2.createBackgroundSubtractorMOG2()

while True:
    _, frame = capture.read()
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Noise reduction
    blurred_frame = cv2.GaussianBlur(gray_frame, (5, 5), 0)
    denoised_frame = cv2.morphologyEx(
        blurred_frame, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))

    # Foreground extraction
    foreground = subtractor.apply(denoised_frame)
    _, foreground = cv2.threshold(foreground, 5, 255, cv2.THRESH_BINARY)

    cv2.imshow("Original", frame)
    cv2.imshow("Foreground", foreground)
    cv2.imshow("Opening", denoised_frame)

    key = cv2.waitKey(30) & 0xff
    if key == 27:
        break

capture.release()
cv2.destroyAllWindows()
