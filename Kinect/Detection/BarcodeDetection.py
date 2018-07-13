from BasicFunctions import get_video
import argparse
import glob
import os
import numpy as np
import cv2

def drawBarcode(name, image):
  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

  gradX = cv2.Sobel(gray, ddepth = cv2.CV_32F, dx = 1, dy = 0, ksize = -1)
  gradY = cv2.Sobel(gray, ddepth = cv2.CV_32F, dx = 0, dy = 1, ksize = -1)

  gradient = cv2.subtract(gradX, gradY)
  gradient = cv2.convertScaleAbs(gradient)

     # blur and threshold the image
  blurred = cv2.blur(gradient, (3, 3))
  (_, thresh) = cv2.threshold(blurred, 210, 250, cv2.THRESH_BINARY)

     # construct a closing kernel and apply it to the thresholded image
  kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 7))
  closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

     # perform a series of erosions and dilations
  closed = cv2.erode(closed, None, iterations = 7)
  closed = cv2.dilate(closed, None, iterations = 2)

  _, cnts, hierarchy = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL,
  cv2.CHAIN_APPROX_SIMPLE)

  c = sorted(cnts, key = cv2.contourArea, reverse = True)[0]
  x,y,w,h = cv2.boundingRect(c)
  cv2.rectangle(image,(x-10,y-5),(x+w+15,y+h+5),(255,255,0),2)
  cv2.imshow(name, image)