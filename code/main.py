import cv2
import numpy as np
from yolo_detector import yolo_detect
from haar_cascade_detector import haar_detect
from blob_detection import blob_detect

from background_extraction import extract_background
from foreground_extraction import get_foreground
from road_mask_creation import *

capture = cv2.VideoCapture('../data/aic19-track3-train-data/2.mp4')

subtractor = cv2.createBackgroundSubtractorMOG2()

params = cv2.SimpleBlobDetector_Params()
params.filterByArea = True
params.minArea = 10
params.maxArea = 1000000
params.filterByColor = True
params.blobColor = 255
blob_detector = cv2.SimpleBlobDetector_create(params)

_, frame = capture.read()
average = np.float32(frame)

# First we create the road mask
mask = get_road_mask('../data/aic19-track3-train-data/3.mp4', 1000)
mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

while True:
    _, frame = capture.read()

    # Background Extraction
    #background, average = extract_background(frame, average)
    #cv2.imshow("Background", background)
    # Foreground Extraction
    # TODO: Overlay onto actual frame
    #foreground = get_foreground(frame, subtractor)
    #cv2.imshow("Foreground", foreground)
    # Road Mask
    #driveable_area = cv2.bitwise_and(mask, frame)
    #cv2.imshow("Driveable Area", driveable_area)

    #=== DETECTION METHODS ===#
    # Detection using YOLO
    yolo_detections = yolo_detect(frame)
    cv2.imshow("YOLO Detections", yolo_detections)
    # Detecting using Haar Cascade
    #haar_detections = haar_detect(frame)
    #cv2.imshow("Haar Detections", haar_detections)
    # Detection using Blob Detector
    #blob_detections = blob_detect(frame, foreground, blob_detector)
    #cv2.imshow("Blob Detections", blob_detections)

    key = cv2.waitKey(30) & 0xff
    if key == 27:
        break

capture.release()
cv2.destroyAllWindows()
