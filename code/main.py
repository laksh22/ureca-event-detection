# TODO: Live object detection inside main for loop
# TODO: Integrate code for stalled car detection
# TODO: Write code to identify traffic jam (if many cars detected in background plate)
# TODO: If the object gives an error in 1 window but not in another, then remove from event list.
# TODO: Migrate to automated path detection
# PROBLEM: Object can overspeed if its far away and underspeed if its close to camera

import cv2
import numpy as np
import pandas as pd

from utilities.background_extraction import extract_background
from utilities.draw import draw, get_color_dict, get_road_polygons, draw_arrow
from utilities.data_manipulation import to_df, to_coordinates, to_txt, allocate_polygon, find_road_specs, get_max, find_events

font = cv2.FONT_HERSHEY_SIMPLEX

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
roads = get_road_polygons(background)

# Make an empty dictionary to store speed and angle of roads, another to store background car density
road_details = {}
background_details = {}
event_details = {}
for i in range(len(roads)):
    x = [p[0] for p in roads[i]]
    y = [p[1] for p in roads[i]]
    centroid = (int(sum(x) / len(roads[i])), int(sum(y) / len(roads[i])))
    road_details[i] = {"speed": [], 
                        "angle": [], 
                        "centroid": centroid, 
                        "median_speed": 0, 
                        "speed_deviation": 0,
                        "median_angle": 0, 
                        "angle_deviation": 0}
    background_details[i] = {"density": 
                                {"count": 0, 
                                "time": 0}}

# Make a filter for drawing road boundaries
road_boundaries = np.zeros((frame.shape[:2][0],frame.shape[:2][1],3), np.uint8)
road_colours = get_color_dict(roads)

for i in range(len(roads)):
    cv2.putText(road_boundaries, str(i), roads[i][0], font, 1, (255, 255, 0), 2)
    cv2.fillConvexPoly(road_boundaries, np.asarray(roads[i]), road_colours[i])

# For doing the rest
capture = cv2.VideoCapture(video)

# Convert the tracks output into a dataframe
df = to_coordinates(tracks)

curr_frame = 1
allocations = None

# For stalled cars/traffic jam
average = np.float32(frame)
background = None
for index, row in df.iterrows():
    _, frame = capture.read()

    #Make dataframe of objects in current frame
    same = df.loc[df['frame'] == curr_frame]

    # Mask for drawing the road arrows
    road_details_frame = np.zeros((frame.shape[:2][0],frame.shape[:2][1],3), np.uint8)

    if (allocations == None):
        # Allocate a road ID to each object
        allocations = allocate_polygon(roads, same)
    else:
        prev_allocations = allocations.copy()
        allocations = allocate_polygon(roads, same)

        # Edit road speed and angle
        road_details = find_road_specs(prev_allocations, allocations, road_details)

        find_events(prev_allocations, allocations, road_details, event_details)
        
    for key in road_details.keys():
        road_details_frame = draw_arrow(road_details_frame, 
                                        road_details[key]["centroid"], 
                                        length=road_details[key]["median_speed"],
                                        angle=road_details[key]["median_angle"])
        cv2.putText(road_details_frame, str(key), road_details[key]["centroid"], font, 1, (255, 255, 0), 2)
        #print(road_details[key]["median_speed"], road_details[key]["median_angle"])
        if(curr_frame == 100):
            None
            #get_max(road_details[key]["speed"])

    

    #Draw points for current frame
    coordinate_frame = draw(coordinate_frame, same)

    # Generate the background frame to see stalled cars
    background, average = extract_background(frame, average)
    cv2.imshow("Bg", background)

    #Show the points on top of the video
    mask = road_boundaries
    mask = cv2.bitwise_or(mask, road_details_frame)
    mask = cv2.bitwise_or(mask, coordinate_frame)
    cv2.addWeighted(mask, 0.5, frame, 1 - 0.5, 0, frame)
    cv2.imshow("Video", frame)

    #print(index, row["index"], row['x'], row['y'])

    curr_frame += 1

    key = cv2.waitKey(30) & 0xff
    if key == 27:
        break

capture.release()
cv2.destroyAllWindows()