This is the repository for my undergraduate research project **"Traffic Event Detection Via Object Tracking"** under the URECA program at NTU.

## Objectives

The objective of the project is to identify the following named events in traffic surveillance videos:

1. Stalled Cars
2. Over Speeding
3. Wrong Direction Driving
4. High Traffic Density

## Procedure

### Training

1. A video will be passed through a tracker like Deep SORT to **get tracking information** of the cars
2. The tracker output will be converted to **CSV format**
3. The CSV data will be taken and **Inverse Perspective Mapping** will be applied to the data and saved as a CSV
4. The mapped CSV data will be used to cluster the moving objects into **common trajectories**
5. Once the common trajectories are determined, the mapped data will again be used to find the **median speed**, **median direction**, and **median traffic density** of the video.
6. For each video, the data will be:

| S. No. | Trajectory ID |     Trajectory Points      | Median Speed | Median Direction | Median Traffic Density |
| :----: | :-----------: | :------------------------: | ------------ | ---------------- | ---------------------- |
|   1    |       1       |    (1,2), (2,4), (3, 6)    | 0.5          | 2.1              | 12                     |
|   2    |       2       | (11,12), (12,19), (13, 26) | 0.9          | -0.3             | 7                      |

### Testing

1. A video will be passed through a tracker like Deep SORT to **get tracking information** of the cars
2. The tracker output will be converted to **CSV format**
3. The CSV data will be taken and **Inverse Perspective Mapping** will be applied to the data and saved as a CSV
4. The mapped CSV data will be used to **assign one of the pre-determined trajectory clusters** to the object
5. For each frame, the **speed and direction** of each object will be matched to that of its corresponding track
6. The **Robust Z-Score Method** will be used to check if the object is anomalous
7. For each frame, the **number of cars** for each track will be calculated and anomalous cars will be identified using the **Robust Z-Score Method**
8. The background plate version of the video will be exported and passed through tracker to **identify stalled cars**

## Helpful Links

1. [Inverse Perspective Mapping](https://zbigatron.com/mapping-camera-coordinates-to-a-2d-floor-plan/)
2. [Robust Z-Score Method](http://colingorrie.github.io/outlier-detection.html#modified-z-score-method)
