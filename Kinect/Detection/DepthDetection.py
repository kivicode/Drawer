from BasicFunctions import *
import cv2
import numpy as np

def getCenter(frame, min_area):
    img = get_depth_changed(200, 700)
    _, contours, hierarchy = cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        if cv2.contourArea(cnt) >= min_area:
            x,y,w,h = cv2.boundingRect(cnt)
            cv2.rectangle(frame,fixPoint(x,y),fixPoint(x+w+7,y+h+12),(0,255,0),2)
            cv2.circle(frame,fixPoint((x+x+w+7)/2,(y+y+h+12)/2),3,(0,255,0),2)
            # box = cv2.boxPoints(cv2.minAreaRect(cnt))
            # j = 0
            # for i in box:
            #     box[j] = fixPoint(box[j][0], box[j][1])
            #     j += 1
            # box = np.int0(box)
            # cv2.drawContours(frame,[box],-1,(0,0,255),3)
    return frame

def drawContours(name, img, min_area, drm):

    cv2.imshow(name,getCenter(img, min_area))