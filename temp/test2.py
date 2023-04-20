import cv2

# Load the MobileNet model
net = cv2.dnn.readNetFromCaffe('MobileNetSSD_deploy.prototxt.txt', 'MobileNetSSD_deploy.caffemodel')

# Define the classes of objects that the model can detect
classes = ["background", "aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow", "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]

# Open a connection to the webcam
cap = cv2.VideoCapture(0)

while True:
    # Capture a frame from the webcam
    ret, frame = cap.read()

    # Prepare the input image for the MobileNet model
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), (127.5, 127.5, 127.5), False)

    # Pass the input image through the MobileNet model to perform object detection
    net.setInput(blob)
    detections = net.forward()

    # Loop over the detections and draw boxes around the objects that were detected
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]

        # If the confidence score is above a certain threshold, draw a box around the object
        if confidence > 0.5:
            class_id = int(detections[0, 0, i, 1])
            class_name = classes[class_id]
            box = detections[0, 0, i, 3:7] * np.array([frame.shape[1], frame.shape[0], frame.shape[1], frame.shape[0]])
            (startX, startY, endX, endY) = box.astype("int")
            cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
            text = "{}: {:.2f}%".format(class_name, confidence * 100)
            cv2.putText(frame, text, (startX, startY - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Display the output frame
    cv2.imshow('Object Detection using MobileNet', frame)

    # Exit the loop if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all windows
cap.release()
cv2.destroyAllWindows()
