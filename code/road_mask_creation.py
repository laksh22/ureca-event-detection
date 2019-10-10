# Create road mask based on moving vehicles
# TODO: Too much noise in black and white output
import cv2
import numpy as np


def process_frame(frame):
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    blurred_frame = cv2.GaussianBlur(gray_frame, (5, 5), 0)
    opening = cv2.morphologyEx(blurred_frame, cv2.MORPH_OPEN,
                               np.ones((5, 5), np.uint8))
    return opening


def get_road_mask(video, count):
    i = 0
    capture = cv2.VideoCapture(video)
    subtractor = cv2.createBackgroundSubtractorMOG2()

    _, frame = capture.read()
    opening = process_frame(frame)

    mask = subtractor.apply(opening)
    _, mask = cv2.threshold(mask, 5, 255, cv2.THRESH_BINARY)
    mask = cv2.bitwise_not(mask)

    while True:
        _, frame = capture.read()
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        blurred_frame = cv2.GaussianBlur(gray_frame, (5, 5), 0)
        opening = cv2.morphologyEx(
            blurred_frame, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))

        foreground = subtractor.apply(opening)
        _, foreground = cv2.threshold(foreground, 5, 255, cv2.THRESH_BINARY)

        mask = cv2.add(mask, foreground)

        masked = cv2.bitwise_and(mask, gray_frame)

        i += 1
        if i == count:
            break

    capture.release()
    return mask


'''
capture = cv2.VideoCapture('../data/aic19-track3-train-data/3.mp4')
subtractor = cv2.createBackgroundSubtractorMOG2()

_, frame = capture.read()
opening = process_frame(frame)

mask = subtractor.apply(opening)
_, mask = cv2.threshold(mask, 5, 255, cv2.THRESH_BINARY)
mask = cv2.bitwise_not(mask)

while True:
    _, frame = capture.read()
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    blurred_frame = cv2.GaussianBlur(gray_frame, (5, 5), 0)
    opening = cv2.morphologyEx(
        blurred_frame, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))

    foreground = subtractor.apply(opening)
    _, foreground = cv2.threshold(foreground, 5, 255, cv2.THRESH_BINARY)

    mask = cv2.add(mask, foreground)

    print(mask.shape, frame.shape, foreground.shape)

    masked = cv2.bitwise_and(mask, gray_frame)

    cv2.imshow("Original", frame)
    cv2.imshow("Masked", masked)
    cv2.imshow("Road Mask", mask)
    cv2.imshow("Mask", foreground)

    key = cv2.waitKey(30) & 0xff
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
'''
