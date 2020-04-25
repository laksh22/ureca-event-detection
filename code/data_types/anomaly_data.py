import pandas as pd
import cv2
import numpy as np

from utilities.draw_tool import DrawTool


class AnomalyData:
    # Constructor
    def __init__(self, output_path):
        self.output_path = output_path
        self.anomalies = []
        self.speed_anomaly = 0
        self.direction_anomaly = 0

    def set_speed_anomaly(self, frame=-1, x=None, y=None, value=None, road=None):
        if frame == -1:
            self.speed_anomaly = 0
        else:
            self.speed_anomaly = {
                "frame": frame,
                "type": "speed",
                "x": x,
                "y": y,
                "value": value,
                "road": road
            }

    def set_direction_anomaly(self, frame=-1, x=None, y=None, value=None, road=None):
        if frame == -1:
            self.direction_anomaly = 0
        else:
            self.direction_anomaly = {
                "frame": frame,
                "type": "direction",
                "x": x,
                "y": y,
                "value": value,
                "road": road
            }

    def insert_anomalies(self, anomalies):
        for index, row in anomalies.iterrows():
            anomaly = {
                "frame": row.frame,
                "type": "stall",
                "x": row.x,
                "y": row.y,
                "value": -1,
                "road": -1
            }
            self.anomalies.append(anomaly)

    def add_anomalies(self):
        if self.speed_anomaly != 0:
            print(self.speed_anomaly)
            self.anomalies.append(self.speed_anomaly)
            self.speed_anomaly = 0
        if self.direction_anomaly != 0:
            print(self.direction_anomaly)
            self.anomalies.append(self.direction_anomaly)
            self.direction_anomaly = 0

    def save_anomalies(self, video_name):
        self.anomalies = pd.DataFrame(self.anomalies)
        if not self.anomalies.empty:
            self.anomalies = self.anomalies.sort_values(by=['frame'])
            self.anomalies.to_csv(
                f'{self.output_path}/{video_name}_anomalies.csv')
            return True
        else:
            print("No anomalies")
            return False

    def show_anomalies(self, video_path, video_name):
        self.draw_tool = DrawTool()
        final_anomalies = pd.read_csv(
            f'{self.output_path}/{video_name}_anomalies.csv')
        capture = cv2.VideoCapture(video_path)

        frame_number = 1

        while(True):
            playing, frame = capture.read()
            if not playing:
                print("---All anomalies for this video have been shown---")
                break

            frame_objects = final_anomalies.loc[final_anomalies['frame']
                                                == frame_number]
            self.draw_image(frame, frame_objects)

            frame_number += 1

            key = cv2.waitKey(30) & 0xff
            if key == 27:
                break

        capture.release()

    # Show the frame of the video with additional information if needed
    def draw_image(self, frame, frame_objects):
        mask = np.zeros(
            (frame.shape[:2][0], frame.shape[:2][1], 3), np.uint8)
        coordinate_frame = self.draw_tool.draw_anomalies(
            frame, frame_objects)
        mask = cv2.bitwise_or(mask, coordinate_frame)
        cv2.addWeighted(mask, 0.5, frame, 0.5, 0, frame)
        cv2.imshow("Video", frame)

    def debug(self, frame, anomaly_type, x, y, value, road):
        print(
            f'Frame: {frame} | Type : {anomaly_type} | X: {x} | Y: {y} | Value: {value} | Road: {road}')
