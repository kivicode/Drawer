import numpy as np
import cv2

width = 640
height = 480
frame = np.zeros((height, width, 3), np.uint8)

turn_left  = -90
turn_right = 90

up    = 0
down  = 180
left  = 270
right = 90

direction = up

px = 10
py = 10

x = 10
y = 10

#path_map = ['forward:100', 'right:200', 'point', 'forward:50']

def getNewDir(cur_dir, event):
	new_dir = (cur_dir + event)	% 360
	return new_dir

def move(dist, angle):
	global x, y, up, down, right, left

	if angle == up:
		y += dist
	elif angle == right:
		x += dist
	elif angle == down:
		y -= dist
	elif angle == left:
		x -= dist

def drawPos(x, y, d, size):
	global frame, px, py
	cv2.rectangle(frame, (x-size,y-size), (x+size, y+size), (0, 255, 0), 1)
	cv2.line(frame, (px,py) , (x, y), (0, 0, 255), 1)
	px = x
	py = y

def drawPoint(x, y, size):
	global frame, px, py
	cv2.circle(frame, (x, y), size, (255, 0, 255), 1)

def drawWay(name, frame, map):
	global x, y, direction, turn_left, turn_right
	drawPos(x, y, direction, 5)
	for cmd in map:
		if cmd == "point":
			drawPoint(x, y, 5)
		else:
			dir = int(cmd.split(':')[0].replace("forward", str(0)).replace("backward", str(-180)).replace("left", str(turn_left)).replace("right", str(turn_right)))
			dist = int(cmd.split(':')[1])
			direction = getNewDir(direction, dir)
			move(dist, direction)
			drawPos(x, y, direction, 5)
	cv2.imshow(name, frame)