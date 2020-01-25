import matplotlib.pyplot as plt

win_len = 15

def to_txt(df, name):
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