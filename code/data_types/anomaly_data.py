import pandas as pd


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
        self.anomalies.to_csv(f'{self.output_path}/{video_name}_anomalies.csv')

    def debug(self, frame, anomaly_type, x, y, value, road):
        print(
            f'Frame: {frame} | Type : {anomaly_type} | X: {x} | Y: {y} | Value: {value} | Road: {road}')
