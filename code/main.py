import cv2
import numpy as np
import pandas as pd

from utilities.background_extraction import extract_background
from utilities.draw import draw, get_color_dict, get_road_polygons
from utilities.data_manipulation import to_df, to_coordinates, to_txt, allocate_polygon

# Getting the data
video = '../data/testing/video1.mp4'
tracks = '../data/testing/detections.txt'

# Start the capture for generating background plate
capture = cv2.VideoCapture(video)
_, frame = capture.read()
average = np.float32(frame)
coordinate_frame = np.zeros((frame.shape[:2][0],frame.shape[:2][1],3), np.uint8) # For drawing the objects

# For gettin the user-drawn road masks
background = None
frame_num = 0
while True:
    _, frame = capture.read()

    # Background Extraction
    background, average = extract_background(frame, average)

    frame_num += 1

    if(frame_num == 200):
        break

# Ask user to draw the road masks
roads = get_road_polygons(background)[:-1]
print(roads)

# For doing the rest
capture = cv2.VideoCapture(video)

# Convert the tracks output into a dataframe
df = to_coordinates(tracks)

curr_frame = 1
for index, row in df.iterrows():
    _, frame = capture.read()

    #Make dataframe of objects in current frame
    same = df.loc[df['frame'] == curr_frame]

    # Allocate a road ID to each object
    allocate_polygon(roads, same)

    #Draw points for current frame
    coordinate_frame = draw(coordinate_frame, same)

    #Show the points on top of the video
    cv2.imshow("Video", cv2.bitwise_or(frame, coordinate_frame))

    #print(index, row["index"], row['x'], row['y'])

    curr_frame += 1

    key = cv2.waitKey(30) & 0xff
    if key == 27:
        break

capture.release()
cv2.destroyAllWindows()