import pandas as pd

def draw(frame_id, frame, df):
    same = df.loc[df['frame'] == frame_id]
    for index, row in same.iterrows():
        cv2.circle(frame, (int(row.x), int(row.y)), 2, (0, 0, 255), 2)
    return frame