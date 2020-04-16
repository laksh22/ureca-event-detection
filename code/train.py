class Trainer:
    # Constructor
    def __init__(self, video_path, output_path, tracks_path=None):
        self.video_path = video_path
        self.output_path = output_path
        if(tracks_path is None):
            self.tracks_path = self.track()
        else:
            self.tracks_path = tracks_path
        print(self.video_path)
        print(self.output_path)
        print(self.tracks_path)

    # Train data for normal behavior of the scene
    def train(self):
        # Step 1: Convert self.tracks_path to CSV format
        # Step 2: Apply inverse perspective mapping to the CSV
        # Step 3: Cluster the CSV data into common trajectories
        # Step 4: Iterate through mapped data and generate trained data for each clustered trajectory
        # Step 5: Save the data in CSV format
        pass

    # Pass video through tracker to get tracking data
    def track(self):
        return "tracks"
