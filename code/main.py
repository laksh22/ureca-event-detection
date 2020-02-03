import cv2
import numpy as np
import pandas as pd

from utilities.background_extraction import extract_background
from utilities.draw import draw, get_color_dict, get_road_polygons, draw_arrow
from utilities.data_manipulation import to_df, to_coordinates, to_txt, allocate_polygon, find_road_specs

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

# Make an empty dictionary to store speed and angle of roads
road_details = {}
for i in range(len(roads)):
    x = [p[0] for p in roads[i]]
    y = [p[1] for p in roads[i]]
    centroid = (sum(x) / len(roads[i]), sum(y) / len(roads[i]))
    road_details[i] = {"speed": [], "angle": [], "centroid": centroid}
    coordinate_frame = draw_arrow(coordinate_frame, centroid)

# For doing the rest
capture = cv2.VideoCapture(video)

# Convert the tracks output into a dataframe
df = to_coordinates(tracks)

curr_frame = 1
allocations = None

for index, row in df.iterrows():
    _, frame = capture.read()

    #Make dataframe of objects in current frame
    same = df.loc[df['frame'] == curr_frame]

    if (allocations == None):
        # Allocate a road ID to each object
        allocations = allocate_polygon(roads, same)
    else:
        prev_allocations = allocations.copy()
        allocations = allocate_polygon(roads, same)

        # Edit road speed and angle
        road_details = find_road_specs(prev_allocations, allocations, road_details)
        print(road_details)
        print("===")

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