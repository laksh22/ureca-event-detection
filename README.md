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

> Example (training): `python main.py train ../data/main/video.mp4 ../data/main ../data/main/tracks.txt`
> or
> `python main.py train ../data/short/NoStall.avi ../data/short ../data/short`

> Example (testing): `python main.py test ../data/main/video.mp4 ../data/main/video_data.csv ../data/main/tracks.txt --anomalies=../data/main`
> or
> `python main.py test ../data/short/NoStall.avi ../data/short ../data/short --anomalies=../data/main`

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
4. The road masks will be used to generate 2D maps of each road through **inverse perspective mapping**✔️
5. The tracking data is again used to find the **median speed**, **median direction**, and **median traffic density** of each of the 2D maps of the roads of the video.✔️
6. For each video, the trained data will be saved as a CSV file with the following format:✔️

| Road ID | Bound 0 | Bound 1 | Bound 2 | Bound 3 | Speed Median | Speed SD | Direction Median | Direction SD | Traffic Median | Traffic SD |
| :-----: | :-----: | :-----: | :-----: | :-----: | :----------: | :------: | :--------------: | :----------: | :------------: | :--------: |
|    1    | [0, 0]  | [0, 0]  | [0, 0]  | [0, 0]  |     1.0      |   1.0    |       1.0        |     1.0      |      1.0       |    1.0     |

### Testing

1. The video is passed through a tracker like Deep SORT to **get tracking information** of the cars✔️
2. The tracker output is converted to a **Pandas DataFrame**✔️
3. The training data CSV will be used to reconstruct the 2D mapped roads✔️
4. For each frame, the **Robust Z-Score Method** will be used to check if there are any anomalous speeds, or traffic levels (for direction, it is checked whether the magnitude of the value is more than 90 degrees as compared to the median). The object is marked as anomalous only if it is anomalous for all the roads in the scene.✔️
5. The background plate version of the video will be exported and passed through a tracker to **identify stalled cars**
6. The anomalous data will be saved as a CSV file with the following format:✔️

| S. No. | Frame |     Type      | X   | Y   | Value | Road |
| :----: | :---: | :-----------: | --- | --- | :---: | :--: |
|   1    |  174  |  Stalled Car  | 23  | 58  |  -1   |  0   |
|   2    |  208  | Over-Speeding | 526 | 127 |  2.7  |  1   |
|   2    |  208  |    Traffic    | 0   | 0   |   4   |  0   |

## Helpful Links

1. [Inverse Perspective Mapping](https://zbigatron.com/mapping-camera-coordinates-to-a-2d-floor-plan/)
2. [Robust Z-Score Method](http://colingorrie.github.io/outlier-detection.html#modified-z-score-method)
