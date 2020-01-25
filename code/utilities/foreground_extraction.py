# MOG moving object detection
import cv2
import numpy as np


def get_foreground(frame, subtractor):
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Noise reduction
    blurred_frame = cv2.GaussianBlur(gray_frame, (5, 5), 0)
    denoised_frame = cv2.morphologyEx(
        blurred_frame, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))

    # Foreground extraction
    foreground = subtractor.apply(denoised_frame)
    _, foreground = cv2.threshold(foreground, 5, 255, cv2.THRESH_BINARY)

    return foreground