import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.path as mPath
from collections import defaultdict
import math
from time import sleep

from utilities.event_detection import detect_event

# To return speed and angle of points in an allocation dictionary
'''
Structure:
roadDetails: {
    road_id : {
        speed: [s1, s2, ..., sn],
        angle: [a1, a2, ..., an],
        centroid: (x, y)
    }
}
'''
def find_road_specs(oldAllocations, newAllocations, roadDetails):
    for key in newAllocations:
        if key in oldAllocations.keys():
            road = newAllocations[key]
            for objKey in road.keys():
                if objKey in oldAllocations[key].keys():
                    oldPoint = oldAllocations[key][objKey]
                    newPoint = newAllocations[key][objKey]
                    distance = get_distance(oldPoint, newPoint)
                    angle = get_angle(oldPoint, newPoint)
                    roadDetails[key]["speed"].append(distance)
                    roadDetails[key]["angle"].append(angle)
    for key in roadDetails.keys():
        roadDetails[key]["median_speed"] = get_median(roadDetails[key]["speed"])
        roadDetails[key]["median_angle"] = get_median(roadDetails[key]["angle"])
        roadDetails[key]["speed_deviation"] = get_mad(roadDetails[key]["speed"])
        roadDetails[key]["angle_deviation"] = get_mad(roadDetails[key]["angle"])

    return roadDetails

def find_background_specs(allocations, background_details):
    for key in allocations:
        road = allocations[key]
        objectCount = 0
        for objKey in road.keys():
            objectCount += 1
        # If the new object count is greater than the maximum, update the count
        if(background_details[key]["density"]["count"] < objectCount):
            background_details[key]["density"]["count"] = objectCount
            background_details[key]["density"]["time"] = 0
        # If it is the same, update the time
        if(background_details[key]["density"]["count"] == objectCount):
            background_details[key]["density"]["time"] = background_details[key]["density"]["time"] + 1

    return background_details

def find_events(oldAllocations, newAllocations, roadDetails, eventDetails):
    for key in newAllocations:
        if key in oldAllocations.keys():
            road = newAllocations[key]
            for objKey in road.keys():
                if objKey in oldAllocations[key].keys():
                    oldPoint = oldAllocations[key][objKey]
                    newPoint = newAllocations[key][objKey]
                    distance = get_distance(oldPoint, newPoint)
                    angle = get_angle(oldPoint, newPoint)
                    if(detect_event(angle, roadDetails[key]["median_angle"], get_mad(roadDetails[key]["angle"]))):
                        print(key, "WRONG SIDE")
                    if(detect_event(distance, roadDetails[key]["median_speed"], get_mad(roadDetails[key]["speed"]))):
                        print(key, "WRONG SPEED")



# To allocate object to a polygon
'''
Structure:
allocations: {
    road_id : {
        object_id: [x, y]
    }
}
'''
def allocate_polygon(polygons, points):
    #polygons_list = [[]]
    allocations=defaultdict(dict)
    for index, row in points.iterrows():
        for i in range(len(polygons)):
            path = mPath.Path(polygons[i])
            if(path.contains_point([row["x"], row["y"]])):
                allocations[i][row["object_id"]] = [row["x"], row["y"]]
                #polygons_list[len(polygons_list)-1].append(i)
        #polygons_list.append([])
    #polygons_list = polygons_list[:-1]
    #points["road_id"] = polygons_list
    return allocations
            

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

def get_distance(p1, p2):
        return math.sqrt( ((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2) )

def get_angle(p1, p2):
    return math.atan2(p2[1]-p1[1], p2[0]-p1[0])

# Using robust Z-Score
def get_mad(arr):
    median = get_median(arr)
    arr = np.asarray(arr)
    arr = np.abs(arr - median)
    mad = get_median(arr)
    return mad

def get_median(xs):
        mid = len(xs) // 2  # Take the mid of the list
        if len(xs) % 2 == 1: # check if the len of list is odd
            return sorted(xs)[mid] #if true then mid will be median after sorting
        else:
            #return 0.5 * sum(sorted(xs)[mid - 1:mid + 1])
            return 0.5 * np.sum(sorted(xs)[mid - 1:mid + 1]) #if false take the avg of mid

def get_max(data, m=2):
    data = sorted(np.array(data))

    no_outliers = remove_outliers(data)
    max_val = np.percentile(no_outliers, 90) 

    return max_val

def remove_outliers(x, outlierConstant=2):
    a = np.array(x)
    upper_quartile = np.percentile(a, 75)
    lower_quartile = np.percentile(a, 25)
    IQR = (upper_quartile - lower_quartile) * outlierConstant
    quartileSet = (lower_quartile - IQR, upper_quartile + IQR)
    resultList = []
    for y in a.tolist():
        if y >= quartileSet[0] and y <= quartileSet[1]:
            resultList.append(y)
    return resultList