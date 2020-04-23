import cv2
import numpy as np


class BackgroundExtractor:
    # Constructor
    def __init__(self, first_frame, output_path):
        self.average = np.float32(first_frame)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.output_video = cv2.VideoWriter(
            output_path, fourcc, 20.0, (first_frame.shape[:2][1], first_frame.shape[:2][0]))
        self.output_video.write(cv2.convertScaleAbs(self.average))

    # Moving average to extract static background plate of a video
    def extract_background(self, frame):
        cv2.accumulateWeighted(frame, self.average, 0.01)
        self.output_video.write(cv2.convertScaleAbs(self.average))

    # Stop writing to the video
    def stop_extraction(self):
        self.output_video.release()
