import subprocess
import cv2
import pandas as pd
import numpy as np

from data_types.track_data import TrackData
from data_types.scene_data import SceneData
from data_types.road_data import RoadData
from utilities.draw_tool import DrawTool


class Tester:
    # Constructor
    def __init__(self, video_path, data_path, tracks_path=None):
        self.video_path = video_path
        self.data_path = data_path
        if ".txt" not in tracks_path:
            self.tracks_path = self.track(self.video_path, tracks_path)
        else:
            self.tracks_path = tracks_path

        # Step 1: Convert self.tracks_path to CSV format
        self.tracks_data = TrackData(self.tracks_path)
        self.coordinates = self.tracks_data.get_coordinates()

        # Initialise helper variables
        self.draw_tool = DrawTool()
        self.capture = cv2.VideoCapture(video_path)
        self.frame_number = 1

    # Test the video in comparison to the normal data of the scene
    def test(self):
        # Step 2: Convert trained data to 2D mapped SceneData
        self.scene = SceneData()
        self.scene.make_testing_scene_data(self.data_path)

        while(True):
            playing, frame = self.capture.read()
            if not playing:
                print("---The testing for this video is complete---")
                break

            # Step 3: For each frame, find anomalous data
            self.frame_objects = self.coordinates.loc[self.coordinates['frame']
                                                      == self.frame_number]
            self.scene.find_anomalies(self.frame_objects)

            # Step 4: Extract background plate of video at every frame and export as video

            self.draw_image(frame, coordinates=True)
            key = cv2.waitKey(30) & 0xff
            if key == 27:
                break

            self.frame_number += 1

        # Step 5: Pass background plate video through tracker to identify stalled cars

    # Pass video through tracker to get tracking data

    def track(self, video_path, tracks_path):
        video_name = (video_path.split("/")[-1]).split(".")[0]
        # TODO: Make values changeable
        subprocess.run(["python", "evaluate.py",
                        "--input", video_path,
                        "--detection_model_path", "./models/resnet18_detrac_nodem",
                        "--detection_threshold", "0.3",
                        "--output_dir", tracks_path], cwd="../external_code/multisot_c")
        return f'{tracks_path.replace("../../", "../")}/{video_name}_track.txt'

    # Show the frame of the video with additional information if needed
    def draw_image(self, frame, coordinates=False):
        mask = np.zeros(
            (frame.shape[:2][0], frame.shape[:2][1], 3), np.uint8)
        if coordinates == True:
            coordinate_frame = self.draw_tool.draw_coordinates(
                frame, self.frame_objects)
            mask = cv2.bitwise_or(mask, coordinate_frame)
        cv2.addWeighted(mask, 0.5, frame, 0.5, 0, frame)
        cv2.imshow("Video", frame)
