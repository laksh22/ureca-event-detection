import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.path as mPath
from collections import defaultdict
import math
from time import sleep


class DataWriter:
    # Convert text file of detected objects to a pandas dataframe
    def to_df(self, path):
        df = pd.read_csv(path, index_col=0, header=None)
        df = df.drop([6], axis=1)
        df.columns = ["object_id", "left", "top", "width", "height"]
        df["frame"] = df.index
        df["index"] = np.arange(len(df))
        df.set_index("index", inplace=True)
        return df

    # Convert default top, left, height, width to locations of centroids
    def to_coordinates(self, path):
        df = to_df(path)
        df['x'] = df.apply(lambda row: round(
            row.left + row.width/2, 2), axis=1)
        df['y'] = df.apply(lambda row: round(
            row.top + row.height/2, 2), axis=1)
        df = df.drop(["top", "left", "width", "height"], axis=1)
        return df
