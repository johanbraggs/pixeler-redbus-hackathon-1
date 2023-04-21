import cv2
import numpy as np
from tensorflow.keras.applications.efficientnet import preprocess_input, decode_predictions
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications.efficientnet import EfficientNetB2
from tensorflow.keras.applications import EfficientNetB2, EfficientNetB4
from tensorflow.keras.applications.efficientnet import preprocess_input, decode_predictions
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications.efficientnet import EfficientNetB2
from tensorflow.keras.applications.efficientnet import preprocess_input, decode_predictions
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications.efficientnet import EfficientNetB2
from tensorflow.keras.applications import EfficientNetB2, EfficientNetB4, EfficientNetB7
from tensorflow.keras.applications.efficientnet import preprocess_input, decode_predictions
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications.efficientnet import EfficientNetB2, EfficientNetB4, EfficientNetB7
from tensorflow.keras.applications.efficientnet import EfficientNetB2, preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications.efficientnet import EfficientNetB2
from tensorflow.keras.utils import get_file
from tensorflow.keras.models import load_model

# Load the pre-trained model
# model_path = get_file(
#     # "efficientdet_d0_coco17_tpu-32/saved_model.pb", 
#     # "http://download.tensorflow.org/models/object_detection/tf2/20200711/efficientdet_d0_coco17_tpu-32/saved_model.pb")
model_path = r"C:\Everything\Trash\efficientdet_d0_coco17_tpu-32\saved_model\saved_model.pb"
model = load_model(model_path, compile=False)

# Initialize the camera
cap = cv2.VideoCapture(0)

while True:
    # Read the frame from the camera
    ret, frame = cap.read()

    # Resize the frame to the input size of the model
    input_size = 512
    resized_frame = cv2.resize(frame, (input_size, input_size))

    # Preprocess the input image
    x = img_to_array(resized_frame)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)

    # Make a prediction
    boxes, scores, classes, num_detections = model.predict(x)

    # Draw the detected objects on the frame
    for i in range(num_detections):
        if scores[0][i] > 0.5:
            left = boxes[0][i][1] * frame.shape[1]
            top = boxes[0][i][0] * frame.shape[0]
            right = boxes[0][i][3] * frame.shape[1]
            bottom = boxes[0][i][2] * frame.shape[0]
            cv2.rectangle(frame, (int(left), int(top)), (int(right), int(bottom)), (0, 255, 0), thickness=2)
    
    # Display the frame
    cv2.imshow('Real-time Object Detection', frame)

    # Exit if the user presses the 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close the window
cap.release()
cv2.destroyAllWindows()
