from vidstab.VidStab import VidStab
import cv2

stabilizer = VidStab()
capture = cv2.VideoCapture('../data/aic19-track3-train-data/1.mp4')

i = 0
while True:
    _, frame = capture.read()

    stabilized_frame = stabilizer.stabilize_frame(input_frame=frame,
                                                  smoothing_window=30)

    cv2.imshow("Original", frame)
    cv2.imshow("Stabilised", stabilized_frame)

    print(i)
    i += 1

    key = cv2.waitKey(30) & 0xff
    if key == 27:
        break

capture.release()
cv2.destroyAllWindows()
