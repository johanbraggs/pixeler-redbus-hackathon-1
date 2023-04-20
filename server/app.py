import numpy as np
import imutils
import time
import cv2

CLASSES = ["aeroplane", "background", "bicycle", "bird", "boat",
           "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
           "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
           "sofa", "train", "tvmonitor","pencil",    "Desk",    "computer",    "monitor",    "keyboard",    "mouse",    "printer",    "scanner",    "faxmachine",    "telephone",    "calculator",    "Notepad",    "Pen",    "Pencil",    "Highlighter",    "Stapler",    "Paperclip",    "Tape",    "Glue",    "Envelopes",    "Folders",    "File cabinet",    "Whiteboard",    "Markers",    "Post-it notes",    "Push pins",    "Ruler",    "Scissors",    "Paper",    "Binder clips",    "Rubber bands",    "Trash can",    "Desk lamp",    "Wall clock",    "Calendar",    "Name plate",    "Coat rack"]


COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))
net = cv2.dnn.readNetFromCaffe("server\MobileNetSSD_deploy.prototxt.txt","server\MobileNetSSD_deploy.caffemodel")

cap = cv2.VideoCapture(0)

time.sleep(2.0)
xx=""
while True:
	# grab the frame from the video capture and resize it to have a maximum width of 400 pixels
	_, frame = cap.read()
	frame = imutils.resize(frame, width=400)
	(h, w) = frame.shape[:2]

	resized_image = cv2.resize(frame, (300, 300))

	blob = cv2.dnn.blobFromImage(resized_image, (1/127.5), (300, 300), 127.5, swapRB=True)

	net.setInput(blob)

	predictions = net.forward()

	# loop over the predictions
	for i in np.arange(0, predictions.shape[2]):
		confidence = predictions[0, 0, i, 2]
		
		if confidence > 0.8:
			idx = int(predictions[0, 0, i, 1])

			box = predictions[0, 0, i, 3:7] * np.array([w, h, w, h])
			(startX, startY, endX, endY) = box.astype("int")

			# Get the label with the confidence score
			label = "{}: {:.2f}%".format(CLASSES[idx], confidence * 100)
			if CLASSES[idx]==xx:
				print("Same")
			else:
				xx=CLASSES[idx]
				print(label)

			cv2.rectangle(frame, (startX, startY), (endX, endY),
				COLORS[idx], 2)
			y = startY - 15 if startY - 15 > 15 else startY + 15

			cv2.putText(frame, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)

	# show the output frame
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF

	if key == ord("q"):
		break

