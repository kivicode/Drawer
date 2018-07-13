import Functions
from Circle import Circle
from Line import Line
from Rectangle import Rect
import numpy as np
import cv2
import os
import subprocess
import texteditor as te

width = 1080
height = 720
frame = np.zeros((height, width,3), np.uint8)
RED = 255
GREEN = 255
BLUE = 255
nodes = []
CLASSES = ["Line", "Rect", "Circle"]
OPERATORS = ["AND", "CONCAT", "CUTA", "CUTB"]
text = ""
ptext = ""

FILENAME = "Rect_Demo"
winName = "Vizualizator"
def setup():
	a=0
	# cv2.namedwindow("Drawer")
	global frame, width, height
	cv2.namedWindow(winName, cv2.WND_PROP_FULLSCREEN)
	cv2.resizeWindow(winName, width, height)
	cv2.imshow(winName,frame)
	te.start()

	# r1 = Rect([100,100],100,100)
	# r2 = Rect([150,150],100,100)
	# c1 = Circle([250,250],100)
	# r2.CONCAT(r1, c1)
	# draw(r2)
	# draw(r2)
	# draw(c1)



def loop(text, vars):
	global frame, nodes
	nodes = vars
	evalFile(text)
	frame = create_blank()
	for i in nodes:
		drawP(eval(i+".points"), color=(255,255,255))
	cv2.imshow(winName, frame)
	


def evalFile(input):
	global nodes, frame
	frame = create_blank(rgb_color=(0,0,0))
	try:
		exec(input, globals())
	except Exception as err:
		print("Script error:",err)
	cv2.imshow(winName, frame)


def addClass(name):
	CLASSES.append(name)

def create_blank(rgb_color=(0, 0, 0)):
	global width, height
	image = np.zeros((height, width, 3), np.uint8)
	color = tuple(reversed(rgb_color))
	image[:] = color
	return image

def background():
	global frame
	frame = create_blank(rgb_color=(255,0,0))#np.zeros((height, width,3), np.uint8)

def stroke(r, g, b):
	RED = r
	GREEN = g
	BLUE = b

def line(x1, y1, x2, y2, color):
	cv2.line(frame,(int(x1),int(y1)),(int(x2),int(y2)),color,1)

def draw(obj, color=(255,255,255)):
	if obj.canDraw:
		pts = np.array(obj.points, np.int32)
		cv2.polylines(frame,[pts],True,color, 2)

def drawP(obj, fill=False,color=(255,255,255)):
	# obj.append(opj[0])
	pts = np.array(obj, np.int32)
	if fill:
		cv2.fillPoly(frame,[pts],color)
	else:
		cv2.polylines(frame,[pts],True,color)

if __name__ == "__main__":
	setup()