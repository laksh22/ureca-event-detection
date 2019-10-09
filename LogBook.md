# Week 0 - 1st August to 4th August

1. Started Udacity course on Deep Learning
2. Created a conda environment
   1. `conda create -n ureca python=3.6 anaconda`
   2. `conda install pytorch-cpu torchvision-cpu -c pytorch`
   3. `conda install nb_conda`

# Week 1 - 5th August to 11th August

1. Continued Udacity course till Introduction to PyTorch

# Week 2 - 12th August to 18th August

1. Continued Udacity course. Studied CNNs.
2. Studied Kalman filters.
3. Met with Dr. Tan Cheen Hau and discussed project details on 13th August.
4. Thought of implementing accident detection using Kalman Filters via CCTV footage.

# Week 3 - 19th August to 25th August

1. Completed CNN on Udacity.
2. Decided that project should detect road events using pre-existing techniques.
3. Learnt object detection algorithms - R-CNN(Selective Search, etc.), Fast R-CNN, Faster R-CNN, SSD, and YOLO.
4. Ideas - Detect weather conditions, use capsule network for object detection. Detect only changing pixels for foreground extraction. Begin by detecting lanes. Then detect paths. Then detect anomalies. Use C3D to detect overall anomaly then when detected, play back some footage to localize. Find average speed for lane. Flag anyone going too fast. Detect lanes and when anomaly detected, check if any car switching lanes too much. If stopping in traffic, detect how long stopped. If not stopped too long, normal. Segment moving objects first to extract cars. Detect cars in background plate as stalled cars if first moving and then not moving. Find a way to segment out the road. Try using Mask-RCNN since its good in high density cases. Use DeepSORT or SORT for tracking. Try creating average paths for cars on the road and detect anomalies if a path deviates from it.
5. Current Methods:
   1. Tracking based - Use luminance contrast for background and foreground segmentation. Track between frames using matching matrices algorithm. Centroid of blob is used to plot trajectory. Use movements characteristics of blobs to guess events.
   2. Lane detection + Kalman Filter - Vanishing point prediction for lane detection. Gaussian background subtraction for motion detection. Kalman filter between frames for tracking. Trajectories are clustered to find lanes.
   3. Motion Interaction Field - Optical flow algorithm used on video. Kernel function is used to measure interaction between flows.
   4. MIL-based - Multiple Instance Learning is used to categorize videos as anomalous or not. Rank videos from most anomalous to least anomalous. Use _C3D_ to extract feature from videos.
   5. Crashed car detection - Use 3 SVMs to classify damaged and non-damaged cars. The 2 detectors are: Undamaged car detector, damage texture detector, and car parts detector.
   6. Traffic Accident and Anomaly Detection - Horn-Schunck algorithm and frame differencing used to track cars. Velocity, lane change rate, and distance between cars are calculated using optical flow vectors. Parzen Probablistic Neural Network is used to detect if anomaly.
   7. Topic-based analysis - Topic analysis of clips. Visual words formed containing spatial location, HOG-HOF cluster, and parent blob size. Find documents containing anomalous words???
   8. Unsupervised Anomaly Detection - Find stationary cars by comparing multiple frames. Use this background image for tracking other cars. Use this as candidate. Generate road mask to reduce false detection.

# Week 4 - 26th August to 1st September

1. Continued reading current methods
2. Possible problems - Congested situations.
3. Object tracking overview:
   1. Trajectory Extraction - Optical flow[good for crowd but short tracks], dense trajectory, feature tracking(KLT algorithm)[may produce multiple tracks of single object, use multi-object tracking], feature tracking, multi-object tracking[may fail in dense scenes].
   2. Trajectory representation - bounding box, flow lines(in 2D and 3D space)
   3. Trajectory clustering - sequence similarity distance, dynamic time warping, etc.
   4. Event Detection - Hidden Markov Model, Bayesian Framework, Dirichlet process

# Week 5 - 2nd September to 8th September

1. Read more research papers (mainly from AI CITY CHALLENGE)
2. Events to detect:
   1. Car stalling
   2. Car accident
   3. Excessive lane jumping
   4. Slow car in fast lane
   5. Over-speeding
3. Proposed system plan:
   1. Stabilise video using OpenCV (try making methods more robust to shaky videos)✔
   2. Background extraction to detect stalled cars ✔
   3. Foreground extraction (✔) to select driveable areas
   4. Lane detection to detect different lanes
   5. Car detection and tracking(SORT or DeepSORT)
   6. Extract average car speed for each lane
   7. Car path anomaly detection
   8. Car Stalling:
      1. Foreground - Check how long stopped(if stopping is more than average)
      2. Background - Check how long stopped vehicle has been there and if other cars are also there
   9. Lane Jumping:
      1. If anomaly detected, check if path of anomalous car switches lanes a lot
   10. Slow car in fast lane:
       1. If car speed lower than 10% of average lane speed, slow car
   11. Over-speeding:
       1. If speed of car 10% greater than highest average speed of all lanes, over-speeding
   12. Car accident:
       1. If anomalous path and then car stops or slows down to upto 5% of its speed, accident. Abrupt speed change. (For stalling, gradual speed change).

# Week 6 - 9th September to 15th September

1. Created video stabilization script
2. Downloaded AI City Challenge data
3. Problems:
   1. Video Stabilization is mediocre
   2. In foreground extraction, shadow detected, cars not detected as single blob

# Week 6 - 16th September to 22nd September

1. Met with Dr. Tan Cheen Hau and got ideas approved.
2. Improved foreground extraction technique by using Opening and Gaussian blur for the mask.
3. Researched on Deep SORT and got Deep SORT running on local machine.

# Week 7 - 23rd September to 29th September

1. Deep SORT is too heavy and required GPU for efficient running(0.5 FPS on CPU). Researched on other algorithms instead.
2. Implemented YOLO Lite(https://arxiv.org/pdf/1811.05588.pdf) in PyTorch for car detection and centroid tracking for object tracking in OpenCV. Using this since it is the most accurate and fastest object detection algorithm available as of now.
3. Plan on creating custom CNN which improves upon YOLO Lite to make it more accurate and faster.

# Week 8 - 30th September to 6th October

1. Implemented YOLOv3 in PyTorch.

# Week 9 - 7th October to 13th October
1. Developed tracking scripts using Haar Cascade, YOLO, and Blob Detection.