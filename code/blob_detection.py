import cv2
import numpy as np
from foreground_extraction import get_foreground

capture = cv2.VideoCapture('../data/aic19-track3-train-data/3.mp4')
subtractor = cv2.createBackgroundSubtractorMOG2()
params = cv2.SimpleBlobDetector_Params()

params.filterByArea = True
params.minArea = 1
params.maxArea = 10000
params.filterByColor = True
params.blobColor = 255

detector = cv2.SimpleBlobDetector_create(params)

while True:
    _, frame = capture.read()

    foreground = get_foreground(frame, subtractor)

    cv2.imshow("Foreground", foreground)

    keypoints = detector.detect(foreground)

    imgKeyPoints = cv2.drawKeypoints(frame, keypoints, np.array(
        []), (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    cv2.imshow("Keypoints", imgKeyPoints)

    key = cv2.waitKey(30) & 0xff
    if key == 27:
        break

capture.release()
cv2.destroyAllWindows()
