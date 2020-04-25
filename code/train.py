import subprocess
import cv2
import pandas as pd
import numpy as np

from data_types.track_data import TrackData
from data_types.scene_data import SceneData
from data_types.road_data import RoadData
from utilities.draw_tool import DrawTool


class Trainer:
    # Constructor
    def __init__(self, video_path, output_path, tracks_path):
        # Initialise path variables
        self.video_name = (video_path.split("/")[-1]).split(".")[0]
        self.video_path = video_path
        self.output_path = output_path
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

    # Train data for normal behavior of the scene
    def train(self):

        # Step 2: Get the road masks from the user
        roads = self.get_roads()
        # Step 3: For each road mask, do inverse Inverse Perspective Mapping
        self.scene = SceneData()
        self.scene.make_training_scene_data(roads)

        while(True):
            playing, frame = self.capture.read()
            if not playing:
                print("---The training for this video is complete---")
                break

            # Step 4: Iterate through mapped data and generate trained data for each 2D road map
            self.frame_objects = self.coordinates.loc[self.coordinates['frame']
                                                      == self.frame_number]
            self.scene.update_scene(self.frame_objects)

            self.draw_image(frame, coordinates=True)
            key = cv2.waitKey(30) & 0xff
            if key == 27:
                break

            self.frame_number += 1

        # Step 5: Save the scene data in CSV format
        self.scene.save(self.output_path, self.video_name)

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

    # Pass video through tracker to get tracking data
    def track(self, video_path, tracks_path):
        subprocess.run(["python", "evaluate.py",
                        "--input", f'../{video_path}',
                        "--detection_model_path", "./models/resnet18_detrac_nodem",
                        "--detection_threshold", "0.7",
                        "--output_dir", f'../{tracks_path}'], cwd="../external_code/multisot_c")
        return f'{tracks_path.replace("../../", "../")}/{self.video_name}_track.txt'

    # Get the road boundaries for this scene
    def get_roads(self):
        _, frame = self.capture.read()
        road_boundaries = self.draw_tool.get_road_boundaries(frame)
        self.refresh_video()
        return road_boundaries

    # Release current video capture and restart
    def refresh_video(self):
        self.capture.release()
        self.capture = cv2.VideoCapture(self.video_path)
