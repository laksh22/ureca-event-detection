import subprocess
import cv2

from utilities.track_data import TrackData
from utilities.perspective import Perspective
from utilities.draw_tool import DrawTool


class Trainer:
    # Constructor
    def __init__(self, video_path, output_path, tracks_path):
        self.video_path = video_path
        self.output_path = output_path
        if ".txt" not in tracks_path:
            self.tracks_path = self.track(self.video_path, tracks_path)
        else:
            self.tracks_path = tracks_path

        # Step 1: Convert self.tracks_path to CSV format
        self.tracks_data = TrackData(self.tracks_path)
        self.draw_tool = DrawTool()

        self.coordinates = self.tracks_data.get_coordinates()
        self.capture = cv2.VideoCapture(video_path)
        self.frame_number = 1

    # Train data for normal behavior of the scene
    def train(self):

        # Step 2: Cluster the CSV data into common trajectories
        # Step 3: Iterate through mapped data and generate trained data for each clustered trajectory
        while(True):
            playing, frame = self.capture.read()
            if not playing:
                print("---The training for this video is complete---")
                break

            self.draw_image(frame, coordinates=True)

            key = cv2.waitKey(30) & 0xff
            if key == 27:
                break

            self.frame_number += 1

        # Step 4: Save the data in CSV format

    # Show the frame of the video with additional information if needed
    def draw_image(self, frame, coordinates=False):
        mask = None
        if coordinates == True:
            same = self.coordinates.loc[self.coordinates['frame']
                                        == self.frame_number]

            coordinate_frame = self.draw_tool.draw_coordinates(frame, same)
            cv2.addWeighted(coordinate_frame, 0.5, frame, 0.5, 0, frame)
        cv2.imshow("Video", frame)

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

    # Pass scene to map it into a 2D plane
    def map_perspective(self):
        capture = cv2.VideoCapture(self.video_path)
        _, image = capture.read()

        src = self.draw_tool.get_perspective_src(image)
        self.perspective = Perspective(image, src)
        mapped = self.perspective.transform_img(image)

        while(True):
            cv2.imshow("Mapped", mapped)

            k = cv2.waitKey(1) & 0xFF
            if k == 27:  # Escape KEY
                return
