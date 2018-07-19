from BasicFunctions import *
import cv2
import math
def detectContours(name, frame):
	imgray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
	ret,thresh = cv2.threshold(imgray,127,255,0)
	im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	min_area = 400
	maxArea = 100
	maxCnt = contours[0]
	for cnt in contours:
		if cv2.contourArea(cnt) > min_area and cv2.contourArea(cnt) > maxArea:
			maxCnt = cnt#cv2.drawContours(frame,[cnt],-1,(0,0,255),3)
	cv2.drawContours(frame,[maxCnt],-1,(0,0,255),3)
	M = cv2.moments(maxCnt)
	cX = int(M["m10"] / M["m00"])
	cY = int(M["m01"] / M["m00"])
	center = [cX,cY]
	cv2.circle(frame, (cX, cY), 3, (0,0,255),2)
	dist = 170
	A = getAngleFromDepth(cX, cY, dist, 640)
	B = getAngleFromDepth(cX, cY, dist, 480)
	#-10D 1mm
	try:
		Ypad = (dist/math.tan(math.radians(A)))/100
		Xpad = (dist/math.tan(math.radians(B)))/100
		pads = ["Backward " + str(int(abs(Xpad))) if Ypad < 0 else  "Forward " + str(int(abs(Xpad))) + "mm", "Right " + str(int(abs(Ypad))) if Ypad < 0 else  "Left " + str(int(abs(Ypad))) + "mm"]
		print(pads)
		cv2.putText(frame,"center",(cX, cY), cv2.FONT_HERSHEY_PLAIN, 1,(0,0,255),2,cv2.LINE_AA)
		cv2.imshow(name, frame)
	except:
		a=0