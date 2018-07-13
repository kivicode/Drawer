from main import *
import cv2

def rect(x,y,w,h, center = False):
	global frame
	print("rect")
	fillMode = 0
	if doFill:
		fillMode = cv2.FILLED
	cv2.rectangle(frame, (int(x), int(y)), (int(x+w), int(y+h)), fill, fillMode)