This is the repository for my undergraduate research project **"Traffic Event Detection Via Object Tracking"** under the URECA program at NTU.

## How to use

First run `cd code` to navigate to the correct folder

```
usage: main.py [-h] mode video data tracks

positional arguments:
  mode        Pass either 'train' or 'test'
  video       Path to the video file
  data        Path where training data is stored or should be stored
  tracks      Path where tracking data is stored or should be stored
```

> Example: `python main.py train ../data/main/video.mp4 ../data/main ../data/main/tracks.txt`
> or
> `python main.py train ../data/short/NoStall.avi ../data/short ../data/short`
> ``

## Objectives

The objective of the project is to identify the following named events in traffic surveillance videos:

1. Stalled Cars
2. Over Speeding
3. Wrong Direction Driving
4. High Traffic Density

## Procedure

### Training

1. The video is passed through a tracker like Deep SORT to **get tracking information** of the cars✔️
2. The tracker output is converted to a **Pandas DataFrame**✔️
3. The user is asked to draw the **road masks** for the scene✔️
4. The road masks will be used to generate 2D maps of each road through **inverse perspective mapping**
5. The tracking data is again used to find the **median speed**, **median direction**, and **median traffic density** of each of the 2D maps of the roads of the video.✔️
6. For each video, the trained data will be saved as a CSV file with the following format:✔️

| S. No. | Road ID |         Road Boundary Points         | Median Speed | Median Direction | Median Traffic Density |
| :----: | :-----: | :----------------------------------: | ------------ | ---------------- | ---------------------- |
|   1    |    1    |     (1,2), (2,4), (3, 6), (5,8)      | 0.5          | 2.1              | 12                     |
|   2    |    2    | (11,12), (12,19), (13, 26), (15, 29) | 0.9          | -0.3             | 7                      |

### Testing

1. The video is passed through a tracker like Deep SORT to **get tracking information** of the cars✔️
2. The tracker output is converted to a **Pandas DataFrame**✔️
3. The CSV data will be used to **assign one of the pre-determined 2D mapped roads** to the object
4. For each frame, the **speed and direction** of each object will be matched to that of its corresponding track
5. The **Robust Z-Score Method** will be used to check if the object is anomalous
6. For each frame, the **number of cars** for each track will be calculated and anomalous cars will be identified using the **Robust Z-Score Method**
7. The background plate version of the video will be exported and passed through tracker to **identify stalled cars**

## Helpful Links

1. [Inverse Perspective Mapping](https://zbigatron.com/mapping-camera-coordinates-to-a-2d-floor-plan/)
2. [Robust Z-Score Method](http://colingorrie.github.io/outlier-detection.html#modified-z-score-method)
