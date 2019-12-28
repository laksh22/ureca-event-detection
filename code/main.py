import cv2
import numpy as np

from utilities.to_df import to_df, to_coordinates
from utilities.draw import draw, get_color_dict
from utilities.tdbscan import T_DBSCAN

df = to_coordinates("../data/testing/detections.txt")
capture = cv2.VideoCapture('../data/testing/video1.mp4')

_, img = capture.read()

coordinate_frame = np.zeros((img.shape[:2][0],img.shape[:2][1],3), np.uint8)

curr_frame = 1

# Get trajectory clusters
clustered_df = T_DBSCAN(df, 300, 40, 2)
#clustered_df.to_csv("clusters.csv")
print("CLUSTER: ", clustered_df)
colors = get_color_dict(clustered_df)

for index, row in df.iterrows():
    _, frame = capture.read()

    #Make dataframe of objects in current frame
    same = df.loc[df['frame'] == curr_frame]

    #Draw points for current frame
    coordinate_frame = draw(coordinate_frame, same, colors[clustered_df.loc[index, "cluster"]])

    cv2.imshow("Video", cv2.bitwise_or(frame, coordinate_frame))

    #print(index, row["index"], row['x'], row['y'])

    curr_frame += 1

    key = cv2.waitKey(30) & 0xff
    if key == 27:
        break

capture.release()
cv2.destroyAllWindows()
    