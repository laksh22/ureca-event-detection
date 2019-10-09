import cv2
import numpy as np

# Load YOLO
net = cv2.dnn.readNet("../data/yolov3-tiny.weights", "../data/yolov3-tiny.cfg")
classes = []

with open("../data/coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]


def yolo_detect(frame):
    # Load the image
    #img = cv2.imread("../data/dog.jpg")
    img = frame
    height, width, channels = img.shape

    # Detecting objects
    blob = cv2.dnn.blobFromImage(
        img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

    net.setInput(blob)

    outs = net.forward(output_layers)

    # Showing information on the screen

    class_ids = []
    confidences = []
    boxes = []

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                # Object detected
                center_x = int(detection[0]*width)
                center_y = int(detection[1]*height)
                w = int(detection[2]*width)
                h = int(detection[3]*height)

                # Rectangle coordinates
                x = int(center_x - w/2)
                y = int(center_y - h/2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.3, 0.4)
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
            print(str(classes[class_ids[i]]))

    return img
