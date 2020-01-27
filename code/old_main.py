import cv2
import numpy as np

from utilities.background_extraction import extract_background
from utilities.foreground_extraction import get_foreground
from utilities.road_mask_creation import *
from utilities.draw_polygon import get_road_polygons

#video = '../data/aic19-track3-train-data/49.mp4'
video = '../data/trimmed_49.avi'

capture = cv2.VideoCapture(video)
width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH) + 0.5)
height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT) + 0.5)
size = (width, height)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
output = cv2.VideoWriter("stalled_car.avi", fourcc, 20.0, size)

_, frame = capture.read()
average = np.float32(frame)

# For gettin the user-drawn road masks
background = None
frame_num = 0
while True:
    _, frame = capture.read()

    # Background Extraction
    background, average = extract_background(frame, average)

    frame_num += 1

    if(frame_num == 200):
        cv2.imwrite('background.png', background)
        break

roads = get_road_polygons(background)[:-1]
print(roads)

# For doing the rest
capture = cv2.VideoCapture(video)
while True:
    _, frame = capture.read()

    background, average = extract_background(frame, average)
    cv2.imshow("Background", background)
    output.write(background)

    key = cv2.waitKey(30) & 0xff
    if key == 27:
        break

capture.release()
output.release()
cv2.destroyAllWindows()