import tensorflow as tf
import numpy as np
import cv2

# Path to the checkpoint directory
PATH_TO_CHECKPOINT = r'C:\Everything\Trash\efficientdet_d0_coco17_tpu-32\checkpoint'

# Load the saved model using the TensorFlow SavedModel API
detect_fn = tf.saved_model.load(PATH_TO_CHECKPOINT)

# Path to the input image
IMAGE_PATH = r"C:\Users\parth\OneDrive\Pictures\61G0WaxlojL._SX679_.jpg"

# Load the image using OpenCV
image_np = cv2.imread(IMAGE_PATH)

# Convert the image to a tensor
input_tensor = tf.convert_to_tensor(np.expand_dims(image_np, 0), dtype=tf.float32)

# Perform object detection on the input tensor
detections = detect_fn(input_tensor)

# Extract the detected boxes, scores, and classes
boxes = detections['detection_boxes'][0].numpy()
scores = detections['detection_scores'][0].numpy()
classes = detections['detection_classes'][0].numpy().astype(np.int32)

# Draw the bounding boxes on the image
for i in range(len(boxes)):
    if scores[i] > 0.5:
        ymin, xmin, ymax, xmax = boxes[i]
        xmin = int(xmin * image_np.shape[1])
        xmax = int(xmax * image_np.shape[1])
        ymin = int(ymin * image_np.shape[0])
        ymax = int(ymax * image_np.shape[0])
        cv2.rectangle(image_np, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)

# Display the image
cv2.imshow('Object Detection', image_np)
cv2.waitKey(0)
cv2.destroyAllWindows()
