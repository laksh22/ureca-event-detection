import cv2
import numpy as np

from utilities.background_extraction import extract_background
from utilities.foreground_extraction import get_foreground
from utilities.road_mask_creation import *

#video = '../data/aic19-track3-train-data/49.mp4'
video = '../data/trimmed_49.avi'

capture = cv2.VideoCapture(video)
width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH) + 0.5)
height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT) + 0.5)
size = (width, height)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
output = cv2.VideoWriter("stalled_car.avi", fourcc, 20.0, size)

subtractor = cv2.createBackgroundSubtractorMOG2()

_, frame = capture.read()
average = np.float32(frame)

# First we create the road mask
mask = get_road_mask(video, 1300)
mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

while True:
    _, frame = capture.read()

    # Background Extraction
    background, average = extract_background(frame, average)
    cv2.imshow("Background", background)
    output.write(background)
    # Foreground Extraction
    foreground = get_foreground(frame, subtractor)
    cv2.imshow("Foreground", foreground)
    # Road Mask
    driveable_area = cv2.bitwise_and(mask, frame)
    cv2.imshow("Driveable Area", mask)

    key = cv2.waitKey(30) & 0xff
    if key == 27:
        break

capture.release()
output.release()
cv2.destroyAllWindows()