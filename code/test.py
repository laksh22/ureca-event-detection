class Tester:
    # Constructor
    def __init__(self, video_path, data_path, tracks_path=None):
        self.video_path = video_path
        self.data_path = data_path
        if(tracks_path is None):
            self.tracks_path = self.track()
        else:
            self.tracks_path = tracks_path
        print(self.video_path)
        print(self.data_path)
        print(self.tracks_path)

    # Test the video in comparison to the normal data of the scene
    def test(self):
        # Step 1: Convert self.tracks_path to CSV format
        # Step 2: Apply inverse perspective mapping to the CSV
        # Step 3: Assign each object to one of the clusters from data_path
        # Step 4: Calculate direction and speed of each car
        # Step 5: Compare direction and speed of car to median of cluster using robust Z-score method
        # Step 6: For each frame, calculate number of cars for each cluster and use robust Z-score to see if traffic jam
        # Step 7: Extract background plate of video at every frame and export as video
        # Step 8: Pass background plate video through tracker to identify stalled cars
        pass

    # Pass video through tracker to get tracking data
    def track(self):
        return "tracks"
