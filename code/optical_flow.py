import cv2
import numpy as np

from utilities.to_df import to_df, to_coordinates
from utilities.draw import draw, get_color_dict
from utilities.to_txt import to_txt

df = to_coordinates("../data/testing/detections.txt")

curr_frame = 1

# Get a VideoCapture object from video and store it in vs
vc = cv2.VideoCapture("../data/testing/video1.mp4")
# Read first frame
ret, first_frame = vc.read()
coordinate_frame = np.zeros((first_frame.shape[:2][0],first_frame.shape[:2][1],3), np.uint8)
# Scale and resize image
resize_dim = 600
max_dim = max(first_frame.shape)
scale = resize_dim/max_dim
first_frame = cv2.resize(first_frame, None, fx=scale, fy=scale)
# Convert to gray scale 
prev_gray = cv2.cvtColor(first_frame, cv2.COLOR_BGR2GRAY)


# Create mask
mask = np.zeros_like(first_frame)
# Sets image saturation to maximum
mask[..., 1] = 255


out = cv2.VideoWriter('video.mp4',-1,1,(600, 600))

for index, row in df.iterrows():
    # Read a frame from video
    ret, frame = vc.read()

    #Make dataframe of objects in current frame
    same = df.loc[df['frame'] == curr_frame]

    #Draw points for current frame
    coordinate_frame = draw(coordinate_frame, same)
    
    # Convert new frame format`s to gray scale and resize gray frame obtained
    gray = cv2.cvtColor(coordinate_frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, None, fx=scale, fy=scale)

    # Calculate dense optical flow by Farneback method
    # https://docs.opencv.org/3.0-beta/modules/video/doc/motion_analysis_and_object_tracking.html#calcopticalflowfarneback
    flow = cv2.calcOpticalFlowFarneback(prev_gray, gray, None, pyr_scale = 0.5, levels = 5, winsize = 11, iterations = 5, poly_n = 5, poly_sigma = 1.1, flags = 0)
    # Compute the magnitude and angle of the 2D vectors
    magnitude, angle = cv2.cartToPolar(flow[..., 0], flow[..., 1])
    # Set image hue according to the optical flow direction
    mask[..., 0] = angle * 180 / np.pi / 2
    # Set image value according to the optical flow magnitude (normalized)
    mask[..., 2] = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX)
    # Convert HSV to RGB (BGR) color representation
    rgb = cv2.cvtColor(mask, cv2.COLOR_HSV2BGR)
    
    # Resize frame size to match dimensions
    coordinate_frame = cv2.resize(coordinate_frame, None, fx=scale, fy=scale)
    
    # Open a new window and displays the output frame
    dense_flow = cv2.addWeighted(coordinate_frame, 1,rgb, 2, 0)
    cv2.imshow("Dense optical flow", rgb)
    out.write(dense_flow)
    # Update previous frame
    prev_gray = gray
    # Frame are read by intervals of 1 millisecond. The programs breaks out of the while loop when the user presses the 'q' key
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
# The following frees up resources and closes all windows
vc.release()

cv2.destroyAllWindows()