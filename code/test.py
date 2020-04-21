import subprocess

from data_types.track_data import TrackData


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

    # Test the video in comparison to the normal data of the scene
    def test(self):
        # Step 1: Convert self.tracks_path to CSV format
        # Step 2: Assign each object to one of the roads from data_path
        # Step 3: Calculate direction and speed of each car
        # Step 4: Compare direction and speed of car to median of cluster using robust Z-score method
        # Step 5: For each frame, calculate number of cars for each road and use robust Z-score to see if traffic jam
        # Step 6: Extract background plate of video at every frame and export as video
        # Step 7: Pass background plate video through tracker to identify stalled cars
        pass

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
