import time
import cv2
import numpy as np

from utilities.to_df import to_df, to_coordinates
from utilities.draw import draw

df = to_coordinates("../data/testing/detections.txt")

capture = cv2.VideoCapture('../data/testing/video1.mp4')

_, img = capture.read()

coordinate_frame = np.zeros((img.shape[:2][0],img.shape[:2][1],3), np.uint8)

curr_frame = 1

for index, row in df.iterrows():
    _, frame = capture.read()

    coordinate_frame = draw(curr_frame, coordinate_frame, df)

    cv2.imshow("Video", cv2.bitwise_or(frame, coordinate_frame))

    #print(index, row["id"], row['x'], row['y'])

    curr_frame += 1

    key = cv2.waitKey(30) & 0xff
    if key == 27:
        break

capture.release()
cv2.destroyAllWindows()
    