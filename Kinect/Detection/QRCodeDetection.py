from BasicFunctions import *
import pyzbar.pyzbar as pyzbar
import numpy as np
import cv2

font = cv2.FONT_HERSHEY_PLAIN
 
def decode(im) :
  decodedObjects = pyzbar.decode(im)   
    
  return decodedObjects
 
 
def display(name, frame, im, decodedObjects):
 
  for decodedObject in decodedObjects: 
    points = decodedObject.polygon
 
    if len(points) > 4 : 
      hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
      hull = list(map(tuple, np.squeeze(hull)))
    else : 
      hull = points;
     
    n = len(hull)

 
    for j in range(0,n):
      cv2.line(frame, hull[j], hull[ (j+1) % n], (255,0,0), 2)

    midx = 0
    midy = 0
    for point in hull:
      midx += point.x
      midy += point.y

    midx /= n
    midy /= n

    midx -= (len(decodedObject.data)-1)*5
    midy += 10
    cv2.putText(frame,decodedObject.data,(int(midx),int(midy)), font, 1,(255,0,255),1,cv2.LINE_AA)
 
  cv2.imshow(name, frame);
 

def drawDecodedQRcode(name, frame):
  im = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)   
  decodedObjects = decode(im)
  display(name, frame, im, decodedObjects)