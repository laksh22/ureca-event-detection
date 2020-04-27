import cv2
import pandas as pd
import numpy as np

scene_num = 1
video_name = f'{scene_num}_test'
video_path = f'../data/traffic_test/{video_name}.mp4'
det_path = f'../data/traffic_test/{video_name}_Det.txt'


def draw_image(frame, coordinates):
    mask = np.zeros(
        (frame.shape[:2][0], frame.shape[:2][1], 3), np.uint8)
    coordinate_frame = draw_coordinates(frame, coordinates)
    mask = cv2.bitwise_or(mask, coordinate_frame)
    cv2.addWeighted(mask, 0.5, frame, 0.5, 0, frame)

    scale_percent = 60  # percent of original size
    width = int(frame.shape[1] * scale_percent / 100)
    height = int(frame.shape[0] * scale_percent / 100)
    dim = (width, height)
    # resize image
    resized = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)

    cv2.imshow("Video", resized)


def draw_coordinates(frame, frame_objects, color=(0, 0, 255)):
    coordinate_frame = np.zeros(
        (frame.shape[:2][0], frame.shape[:2][1], 3), np.uint8)
    for index, row in frame_objects.iterrows():
        start_point = (int(row.left), int(row.top))
        end_point = (int(row.left+row.width), int(row.top+row.height))
        cv2.rectangle(coordinate_frame, start_point, end_point, color, 2)
    return coordinate_frame


def get_detections(data_path):
    df = pd.read_csv(data_path, index_col=0, header=None)
    if(len(df.columns) == 7):
        df = df.drop([6, 7], axis=1)
    else:
        df = df.drop([6], axis=1)
    df.columns = ["obj_id", "left", "top", "width", "height"]
    df["frame"] = df.index
    df["index"] = np.arange(len(df))
    df.set_index("index", inplace=True)
    return df


capture = cv2.VideoCapture(video_path)
detections = get_detections(det_path)
frame_num = 1

while(True):
    playing, frame = capture.read()
    if not playing:
        print("---Video finished---")
        break

    frame_objects = detections.loc[detections['frame']
                                   == frame_num]

    draw_image(frame, frame_objects)
    key = cv2.waitKey(30) & 0xff
    if key == 27:
        break

    frame_num += 1
