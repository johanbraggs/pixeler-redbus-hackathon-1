import numpy as np
import imutils
import time
import cv2
import socket_code
import firebase_push

CLASSES = ['person', 'bicycle', 'car', 'motorbike', 'aeroplane', 'bus', 'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'sofa', 'pottedplant', 'bed', 'diningtable', 'toilet', 'tvmonitor', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush']


COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))
net = cv2.dnn.readNetFromCaffe("server\MobileNetSSD_deploy.prototxt.txt","server\MobileNetSSD_deploy.caffemodel")
cam_link=input()
cap = cv2.VideoCapture("https://"+cam_link+"/video")

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
				try:
					cv2.imwrite("temp_image.jpg",resized_image)
					# socket_code.push("temp_image.jpg",CLASSES[idx])
					firebase_push.push(CLASSES[idx])
				except:
					print("error")
				
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

