import cv2
import numpy as np
from tensorflow.keras.applications.efficientnet import preprocess_input, decode_predictions
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications.efficientnet import EfficientNetB0

# Load the pre-trained model
model = EfficientNetB0(weights='imagenet')

# Initialize the camera
cap = cv2.VideoCapture(0)

while True:
    # Read the frame from the camera
    ret, frame = cap.read()

    # Resize the frame to the input size of the model
    resized_frame = cv2.resize(frame, (224, 224))


    # Preprocess the input image
    x = img_to_array(resized_frame)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)

    # Make a prediction
    predictions = model.predict(x)
    decoded_predictions = decode_predictions(predictions)

    # Get the predicted class label and display it on the frame
    label = decoded_predictions[0][0][1]
    cv2.putText(frame, label, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Display the frame
    cv2.imshow('Real-time Image Recognition', frame)

    # Exit if the user presses the 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close the window
cap.release()
cv2.destroyAllWindows()
