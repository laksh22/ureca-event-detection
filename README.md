This is the repository for my undergraduate research project __"Traffic Event Detection Via Object Tracking"__ under the URECA program at NTU.

## Objectives
The objective of the project is to identify the following named events in traffic surveillance videos:
1. Stalled Cars
2. Over Speeding
3. Wrong Direction Driving
4. High Traffic Density

## Procedure

### Training
1. A video will be passed through a tracker like Deep SORT to __get tracking information__ of the cars
2. The tracker output will be converted to __CSV format__
3. The CSV data will be taken and __Inverse Perspective Mapping__ will be applied to the data and saved as a CSV
4. The mapped CSV data will be used to cluster the moving objects into __common trajectories__
5. Once the common trajectories are determined, the mapped data will again be used to find the __median speed__, __median direction__, and __median traffic density__ of the video.
6. For each video, the data will be:

| S. No. | Trajectory ID |     Trajectory Points      | Median Speed | Median Direction | Median Traffic Density |
| :----: | :-----------: | :------------------------: | ------------ | ---------------- | ---------------------- |
|   1    |       1       |    (1,2), (2,4), (3, 6)    | 0.5          | 2.1              | 12                     |
|   2    |       2       | (11,12), (12,19), (13, 26) | 0.9          | -0.3             | 7                      |

### Testing
1. A video will be passed through a tracker like Deep SORT to __get tracking information__ of the cars
2. The tracker output will be converted to __CSV format__
3. The CSV data will be taken and __Inverse Perspective Mapping__ will be applied to the data and saved as a CSV
4.  The mapped CSV data will be used to __assign one of the pre-determined trajectory clusters__ to the object
5.  For each frame, the __speed and direction__ of each object will be matched to that of its corresponding track
6.  The __Robust Z-Score Method__ will be used to check if the object is anomalous
7.  For each frame, the __number of cars__ for each track will be calculated and anomalous cars will be identified using the __Robust Z-Score Method__
8.  In each frame, background extraction will be done to __identify stalled cars__

## Helpful Links
1. [Inverse Perspective Mapping](https://zbigatron.com/mapping-camera-coordinates-to-a-2d-floor-plan/)
2. [Robust Z-Score Method](http://colingorrie.github.io/outlier-detection.html#modified-z-score-method)