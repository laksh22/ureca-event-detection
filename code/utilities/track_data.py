import pandas as pd
import numpy as np


class TrackData:
    # Constructor
    def __init__(self, data_path):
        self.data_path = data_path
        self.__boxes = self.csv_to_df()
        self.__coordinates = self.df_to_coordinates()

    # Import the CSV from the specified path and store as a DataFrame
    def csv_to_df(self):
        df = pd.read_csv(self.data_path, index_col=0, header=None)
        df = df.drop([6, 7], axis=1)
        df.columns = ["object_id", "left", "top", "width", "height"]
        df["frame"] = df.index
        df["index"] = np.arange(len(df))
        df.set_index("index", inplace=True)
        return df

    # Convert bounding boxes DataFrame to centroid co-ordinates DataFrame
    def df_to_coordinates(self):
        df = self.__boxes.copy()
        df['x'] = df.apply(lambda row: round(
            row.left + row.width/2, 2), axis=1)
        df['y'] = df.apply(lambda row: round(
            row.top + row.height/2, 2), axis=1)
        df = df.drop(["top", "left", "width", "height"], axis=1)
        return df

    # Get bounding boxes DataFrame
    def get_boxes(self):
        return self.__boxes

    # Get co-ordinates DataFrame
    def get_coordinates(self):
        return self.__coordinates
