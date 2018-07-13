import math
import numpy as np
import cv2
import main
import Functions
class Line:
 
	def __init__(self, f, t):
		self.A = f
		self.B = t
		self.points = self.get()
		self.canDraw = True

	def dist(self, p1, p2):
		dist = math.sqrt( (p2[0] - p1[0])**2 + (p2[1] - p1[1])**2 )
		return dist

	def get(self):
		f = self.A
		to = self.B
		pts = []
		count = int(self.dist(f, to))
		if count != 0:
			angle = math.atan2((to[1] - f[1]), (to[0] - f[0]));
			lineLength = self.dist([f[0], f[1]], [to[0], to[1]]);
			segmentLength = lineLength / count;
			for i in range(0, count+1):                
				distFromStart = segmentLength * i;
				px = f[0] + distFromStart * math.cos(angle)
				py = f[1] + distFromStart * math.sin(angle)
				pts.append([px, py])
			global points
			points = pts
		return points

	def AND(A):
		points = Functions.AND(self, A)

	def draw(self, color = (255,255,255)):
		pts = np.array(self.points, np.int32)
		cv2.polylines(main.frame,[pts],True,color)

	# def __call__(self):
	# 	return self.points