import main
from BasicFunctions import *
from Drawing.ParseArduino import eval
import numpy as np
import imutils
import cv2

rows = open("NNDataset/synset_words.txt").read().strip().split("\n")
	

CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
	"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
	"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
	"sofa", "train", "tvmonitor"]

COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

# load our serialized model from disk
net = cv2.dnn.readNetFromCaffe("NNDataset/MobileNetSSD_deploy.prototxt.txt",
	"NNDataset/MobileNetSSD_deploy.caffemodel")

shift = 10
fr = 60
runId = 0
firstRun = True

dists = 0

def reset():
	runId = 0

def drawObjects(name, frame, filter = "all", return_bottle_imgs = False):
	global fr, shift, runId, dists, firstRun

	img = None	

	frame = imutils.resize(frame, width=400)

	(h, w) = frame.shape[:2]
	frame = cv2.resize(frame, (300, 300))
	blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843,
	(300, 300), 127.5)
	net.setInput(blob)
	detections = net.forward()


	for i in np.arange(0, detections.shape[2]):
		confidence = detections[0, 0, i, 2]
		img=None

		idx = int(detections[0, 0, i, 1])
		box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
		(startX, startY, endX, endY) = box.astype("int")
		centerX = (startX+endX)/2
		centerY = (startY+endY)/2

		if confidence * 100 >= fr and (filter == "all" or CLASSES[idx] == filter):
			label = "{}".format(CLASSES[idx],
				confidence * 100)
		if return_bottle_imgs:
			startX += shift
			endX -= shift
			startY += shift+20
			endY -= shift
			img = frame[startY:endY, startX:endX]
			color = compute_average_image_color(img)
			i += 1

			#cv2.rectangle(frame, (startX, startY), (endX, endY),
			#	COLORS[idx], 2)
			y = startY - 15 if startY - 15 > 15 else startY + 15
			if filter == "bottle":
				text = ""
				#writeToFile("Commands.txt", "", clear = True)
				color = compute_average_image_color(img)
				real_color = get_real_color(color)
				dist = getDist(map(centerX-5, 0, w, 0, 300), map(centerY, 0, h, 0, 300))
				if int(dist) != 0:
					angle = getAngleFromDepth(centerX, centerY, dist, w)

					#print("Angle = " + str(np.floor(angle)), dist)
					#angle = angleToArduino(angle)
					#if firstRun:
					side = 'right'
					if angle < 0:
						side = 'left'
					if firstRun:
						print("Set angle from bottle")
						eval(side + '('+str((abs(angle))*1.78)+');')
				main.distToObject = dist
				dist = int(dist)# * 0.66
				dists += dist
				if firstRun:
					main.calibrateByMarker = True
					# dist = dists/10
					print("Set dist from bottle")
					eval(text + 'f('+str((dist))+');')
				runId += 1
				firstRun = False
				cv2.rectangle(frame, (startX, startY), (endX, endY),
				COLORS[idx], 2)
				cv2.putText(frame, real_color + str(dist), (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255, 2)
			else:
				cv2.putText(frame, label, (startX, y),
				cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
				cv2.rectangle(frame, (startX, startY), (endX, endY),
				COLORS[idx], 2)
	cv2.imshow(name, frame)