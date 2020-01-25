import cv2
import numpy as np

vc = cv2.VideoCapture("../data/testing/video1.mp4")
# Read first frame
ret, first_frame = vc.read()
# Scale and resize image
resize_dim = 600
max_dim = max(first_frame.shape)
scale = resize_dim/max_dim
first_frame = cv2.resize(first_frame, None, fx=scale, fy=scale)
# Convert to gray scale 
prev_gray = cv2.cvtColor(first_frame, cv2.COLOR_BGR2GRAY)


# Create mask
mask = np.zeros_like(first_frame)
total_mask = np.zeros_like(first_frame)
# Sets image saturation to maximum
mask[..., 1] = 255
total_mask[..., 1] = 255

while(vc.isOpened()):
    ret, frame = vc.read()
    
    # Convert new frame format`s to gray scale and resize gray frame obtained
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, None, fx=scale, fy=scale)

    # Calculate dense optical flow by Farneback method
    flow = cv2.calcOpticalFlowFarneback(prev_gray, gray, None, pyr_scale = 0.5, levels = 5, winsize = 11, iterations = 5, poly_n = 5, poly_sigma = 1.1, flags = 0)

    # Compute the magnitude and angle of the 2D vectors
    magnitude, angle = cv2.cartToPolar(flow[..., 0], flow[..., 1])

    # Set image hue according to the optical flow direction
    mask[..., 0] = angle * 180 / np.pi / 2

    # Set image value according to the optical flow magnitude (normalized)
    mask[..., 2] = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX)

    # Making the accumulator mask

    mask_angle_temp = mask[..., 0]
    mask_angle_temp = np.where(total_mask[..., 2] < 100, mask_angle_temp, 0)

    mask_magnitude_temp = mask[..., 2]
    mask_magnitude_temp = np.where(total_mask[..., 2] < 100, mask_magnitude_temp, 0)

    total_mask[..., 0] = np.add(total_mask[..., 0], mask_angle_temp)
    total_mask[..., 2] = np.add(total_mask[..., 2], mask_magnitude_temp)

    print(total_mask[..., 2])

    # Convert HSV to RGB (BGR) color representation
    rgb = cv2.cvtColor(total_mask, cv2.COLOR_HSV2BGR)   
    
    # Resize frame size to match dimensions
    frame = cv2.resize(frame, None, fx=scale, fy=scale)
    
    # Open a new window and displays the output frame
    dense_flow = cv2.addWeighted(frame, 1,rgb, 2, 0)
    cv2.imshow("Dense optical flow", dense_flow)
    # Update previous frame
    prev_gray = gray
    
    key = cv2.waitKey(30) & 0xff
    if key == 27:
        break

vc.release()
cv2.destroyAllWindows()