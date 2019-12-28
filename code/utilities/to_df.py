import pandas as pd
import numpy as np

# Convert text file of detected objects to a pandas dataframe
def to_df(path):
    df = pd.read_csv(path, index_col=0, header=None)
    df = df.drop([6], axis=1)
    df.columns = ["object_id", "left", "top", "width", "height"]
    df["frame"] = df.index
    df["index"] = np.arange(len(df))
    df.set_index("index", inplace=True)
    return df

# Convert default top, left, height, width to locations of centroids
def to_coordinates(path):
    df = to_df(path)
    df['x'] = df.apply(lambda row: row.left + row.width/2, axis=1)
    df['y'] = df.apply(lambda row: row.top + row.height/2, axis=1)
    df = df.drop(["top", "left", "width", "height"], axis=1)
    print(df)
    return df