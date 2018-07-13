from BasicFunctions import *
import cv2
import numpy as np
import scipy.ndimage

def surfDetection(name, frame):
	frame = get_depth_changed(308, 1244)

	(minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(frame)
	cv2.circle(frame, (int((minLoc[0]+maxLoc[0])/2), int((minLoc[1]+maxLoc[1])/2)), 3, (255, 0, 0), 2)
	cv2.imshow(name, frame)