from PIL import Image
from Drawing.DrawWay import *
import kinect_lib.freenect as freenect
# from Drawing.ParseArduino import eval as evl
import cv2
import numpy as np
import math
import time
import serial
import time
# arduinoData = serial.Serial('/dev/tty.wchusbserial1420', 9600)

threshold = 0
current_depth = 0


mov_x = 0.08
mov_y = 0.06

cam = cv2.VideoCapture(0)
cam.set(3 , 640  ) # width        
cam.set(4 , 480  ) # height       
cam.set(10, 120  ) # brightness     min: 0   , max: 255 , increment:1  
cam.set(11, 50   ) # contrast       min: 0   , max: 255 , increment:1     
cam.set(12, 70   ) # saturation     min: 0   , max: 255 , increment:1
cam.set(13, 13   ) # hue         
cam.set(14, 50   ) # gain           min: 0   , max: 127 , increment:1
cam.set(15, -3   ) # exposure       min: -7  , max: -1  , increment:1
cam.set(17, 5000 ) # white_balance  min: 4000, max: 7000, increment:1
cam.set(28, 0    ) # focus          min: 0   , max: 255 , increment:5

def auto_canny(image, sigma=0.33):
    # compute the median of the single channel pixel intensities
    v = np.median(image)
 
    # apply automatic Canny edge detection using the computed median
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, lower, upper)
 
    # return the edged image
    return edged

def fixPoint(x,y):
    x = x - x*mov_x
    y = y + y*mov_y
    return (int(x),int(y))

def getCamVideo():
    rval, camFrame = cam.read()
    return camFrame

def change_threshold(value):
    global threshold
    threshold = value

def followPoint(point):
    dist = int(getDist(point[0],point[1]))-100
    angle = getAngleFromDepth(point[0], point[1],dist,640)
    side = 'right'
    if angle < 0:
        side = 'left'
    rot = side + '('+str(int((abs(angle))*1.78 / 2.5))+');'
    evl(rot)
    evl('f('+str(int(dist))+');')


def change_contrast(img, level):
    img = Image.fromarray(img.astype('uint8'))
    factor = (259 * (level + 255)) / (255 * (259 - level))
    def contrast(c):
        return 128 + factor * (c - 128)
    return img.point(contrast)

def getBrightest(img, thr):
    poss = []
    (h, w) = img.shape[:2]
    blank = np.zeros((h,w,3), np.uint8)
    for x in range(0,w):
        for y in range(0,h):
            pixel = img[y,x]
            if pixel <= thr:
                blank[y, x] = pixel
    cv2.imshow("Thres", blank)


def map(value, leftMin, leftMax, rightMin, rightMax):
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    valueScaled = float(value - leftMin) / float(leftSpan)

    return rightMin + (valueScaled * rightSpan)

def change_depth(value):
    global current_depth
    current_depth = value

def get_depth_changed(thresh, dep):
    change_depth(dep)
    change_threshold(thresh)
    global threshold
    global current_depth

    depth, timestamp = freenect.sync_get_depth()
    depth = 255 * np.logical_and(depth >= current_depth - threshold,
                                 depth <= current_depth + threshold)
    depth = depth.astype(np.uint8)
    return depth

def get_video():
    array,_ = freenect.sync_get_video()
    array = cv2.cvtColor(array,cv2.COLOR_RGB2BGR)
    return array
 
def get_depth():
    array,_ = freenect.sync_get_depth()
    array = array.astype(np.uint8)
    return array
    
def getDepthMap():  
    depth, timestamp = freenect.sync_get_depth()
 
    np.clip(depth, 0, 2**10 - 1, depth)
    depth >>= 2
    depth = depth.astype(np.uint8)
 
    return depth

def compute_average_image_color(img):
    height, width, _ = img.shape

    r_total = 0
    g_total = 0
    b_total = 0

    count = 0
    for x in range(0, width):
        for y in range(0, height):
            r, g, b = img[y,x]
            r_total += r
            g_total += g
            b_total += b
            count += 1
    if count == 0:
        return (0,0,0)
    return (r_total/count, g_total/count, b_total/count)


def inRange(input, min, max):
    if input <= max and input >= min:
        return True
    else:
        return False

def get_real_color(color):
    out = "white"
    params = str(color).split("(")[1].split(")")[0].split(",")
    r = int(str(params[2]).split(".")[0])
    g = int(str(params[1]).split(".")[0])
    b = int(str(params[0]).split(".")[0])
    if r < 80 and g < 80 and b < 80:
        out = "pepsi"
    elif r > 140 and b < 50 and g < 120:
        out = "orange"
    elif r < 100 and g > 130 and inRange(b,80,110):
        out = "sprite"
    return out

def getDist(x, y):
    color = 0
    x+=10
    frame = getDepthMap()
    color = frame[int(y),int(x)] 
    cv2.circle(frame, (int(x), int(y)), 5, (255,0,0), 2) 
    cv2.imshow("Test", frame)      
    color = int(map(color,0,255,0,1024))+60
    color *= 1.19
    color -= 20
    return str(int(color))

def getAngleFromDepth(x, y, dist, width):
	angle = 0
	if int(dist) > 0:
		a = 0.00173667
		realX = int(int((x-(width/2)))*a*int(dist))*10
		angle = math.degrees(math.atan(realX/int(dist)))
		angle *= 0.16*1.57
	return angle

def angleToArduino(angle):
    angle *= 3.3
    angle *= 1.5
    angle -= 10
    return angle

def writeToFile(file, text, clear = False):
	read = open(file, "r")
	contents = read.read()
	raw = open(file, "w+")
	if not clear:
		raw.write(contents)
	raw.write(text)

def millis():
    return lambda: int(round(time.time() * 1000))