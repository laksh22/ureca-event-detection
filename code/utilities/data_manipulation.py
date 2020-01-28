import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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
    df['x'] = df.apply(lambda row: round(row.left + row.width/2, 2), axis=1)
    df['y'] = df.apply(lambda row: round(row.top + row.height/2, 2), axis=1)
    df = df.drop(["top", "left", "width", "height"], axis=1)
    return df

def to_txt(df, name):

    win_len = 15

    f = open(name, "w+")

    objects = df.object_id.unique()

    for object in objects:
        locations = df.loc[df['object_id'] == object].head(100)
        locations["smooth_x"] = locations["x"].rolling(win_len, win_type="hamming").mean()
        locations["smooth_y"] = locations["y"].rolling(win_len, win_type="hamming").mean()
        locations = locations.iloc[win_len:]
        
        plt.plot(locations["frame"], locations["smooth_x"])
        plt.plot(locations["frame"], locations["x"], color="black")
        plt.show()
        

        idx = 0
        for index, row in locations.iterrows():
            f.write(f'{locations.iloc[idx]["smooth_x"]} {locations.iloc[idx]["smooth_y"]}  ')
            idx += 1
        f.write("\r\n")

    f.close()