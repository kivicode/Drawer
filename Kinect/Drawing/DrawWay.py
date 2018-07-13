import numpy as np
import math
import cv2
import BasicFunctions as bf
f = 0
b = 180
l = 270
r = 90

cx = 250
cy = 500
ca = 270

img = np.zeros((500,500,3), np.uint8)


def drawWayPart(part):
	cmd = part.split("(")[0]
	params = int(part.split("(")[1].split(")")[0].split(",")[0].split(".")[0])
	if cmd == 'f' or cmd == 'b':
		params = bf.map(params, 0, 3000, 0, 500)
		drawLine(ca, params)
	else:
		newDir(part)

def drawLine(angle, len):
	global cx, cy, img
	ca = angle
	angle = 360-angle
	endy = cy-int(len * math.sin(math.radians(angle)))
	endx = cx+int(len * math.cos(math.radians(angle)))
	print(endx,endy)
	cv2.line(img, (cx, cy),(endx, endy),(255,0,0),2)
	cx = endx
	cy = endy
	cv2.imshow("Line", img);

def newDir(angle):
	global ca
	cmd = angle.split("(")[0]
	param = int(angle.split("(")[1].split(")")[0].split(",")[0].split(".")[0])
	if cmd == "l":
		ca -= param
	if cmd == "r":
		ca += param
	ca = ca%360