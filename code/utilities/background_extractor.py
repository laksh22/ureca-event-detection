import cv2


class BackgroundExtractor:
    # Constructor
    def __init__(self, first_frame):
        self.average = first_frame

    # Moving average to extract static background plate of a video
    def extract_background(self, frame):
        cv2.accumulateWeighted(frame, self.average, 0.01)
        self.average = cv2.convertScaleAbs(self.average)
        return self.average
