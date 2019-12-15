import time
import cv2
import numpy as np

from utilities.to_df import to_df, to_coordinates

df = to_coordinates("../data/detections.txt")

capture = cv2.VideoCapture('../data/aic19-track3-train-data/2.mp4')

_, img = capture.read()

coordinate_frame = np.zeros((img.shape[:2][0],img.shape[:2][1],3), np.uint8)

for index, row in df.iterrows():
    _, frame = capture.read()

    cv2.circle(coordinate_frame, (int(row.x/2), int(row.y/2)), 2, (0, 0, 255), 2)

    cv2.imshow("Video", cv2.bitwise_or(frame, coordinate_frame))

    print(row["id"], row['x'], row['y'])

    key = cv2.waitKey(30) & 0xff
    if key == 27:
        break

capture.release()
cv2.destroyAllWindows()


    