import subprocess

from utilities.track_data import TrackData


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

    # Train data for normal behavior of the scene
    def train(self):

        # Step 2: Apply inverse perspective mapping to the CSV
        # Step 3: Cluster the CSV data into common trajectories
        # Step 4: Iterate through mapped data and generate trained data for each clustered trajectory
        # Step 5: Save the data in CSV format
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
