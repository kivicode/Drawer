import math
import numpy as np
from main import *
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import inspect

pts = []
refvec = [0, 1]
origin = [100,100]

def readFile(name):
	with open(name + '.py', 'r') as myfile:
		data=myfile.read()
		return data

def dist(p1, p2):
	dist = math.sqrt( (p2[0] - p1[0])**2 + (p2[1] - p1[1])**2 )
	return dist

def mysort(points):
	if len(points):
		global origin, pts
		midx = 0
		midy = 0
		for i in points:
			midx += i[0]
			midy += i[1]
		midx /= len(points)
		midy /= len(points)
		origin = [int(midx)+1,int(midy)]
		pts = points
		return sorted(points, key=clockwiseangle_and_distance)
	return []

def sin(angle):
	return math.sin(math.radians(angle))

def cos(angle):
	return math.cos(math.radians(angle))

def tan(angle):
	return math.tan(math.radians(angle))

def asin(angle):
	return math.asin(angle)

def acos(angle):
	return math.acos(angle)

def atan(angle):
	return math.atan(angle)



def sort(points):
	newPath = [points[0]]
	for i in range(0, len(points)):
		p = points[i]
		minDist = 9999
		minId = 0
		for j in range(0, len(points)):
			fin = points[j]
			if j != i:
				if dist(p,fin) < minDist:
					minId = j
					minDist = dist(p,fin)
		newPath.append(points[minId])
	return mysort(newPath)


def cart2pol(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return(rho, phi)

def pol2cart(rho, phi):
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return(x, y)

def clockwiseangle_and_distance(point):
    vector = [point[0]-origin[0], point[1]-origin[1]]
    lenvector = math.hypot(vector[0], vector[1])
    if lenvector == 0:
        return -math.pi, 0
    normalized = [vector[0]/lenvector, vector[1]/lenvector]
    dotprod  = normalized[0]*refvec[0] + normalized[1]*refvec[1]
    diffprod = refvec[1]*normalized[0] - refvec[0]*normalized[1]
    angle = math.atan2(diffprod, dotprod)
    if angle < 0:
        return 2*math.pi+angle, lenvector
    return angle, lenvector

def varName(var):
    lcls = inspect.stack()[2][0].f_locals
    for name in lcls:
        if id(var) == id(lcls[name]):
            return name
    return None

def AND(A, B):
	if not isinstance(A,list):
		A = A.points
	if not isinstance(B,list):
		B = B.points
	points = A+B
	newPoints = []
	for point in points:
		if (onLine(B,point) and partOfPoly(A,point)) or (onLine(A,point) and partOfPoly(B,point)) or (onLine(A,point) and onLine(B,point)):# or partOfPoly(B, point):
			newPoints.append(point)
	return sort(newPoints)

def CONCAT(A, B):
	if not isinstance(A,list):
		A = A.points
	if not isinstance(B,list):
		B = B.points
	points = A+B

	newPoints = []
	for point in points:
		if not ((onLine(B,point) and partOfPoly(A,point)) or (onLine(A,point) and partOfPoly(B,point))):# or partOfPoly(B, point):
			newPoints.append(point)
	return sort(newPoints)

def CUTA(A,B):
	if not isinstance(A,list):
		A = A.points
	if not isinstance(B,list):
		B = B.points
	points = A+B
	newPoints = []
	p1 = []
	p2 = []
	for point in points:
		if onLine(A, point) and not partOfPoly(B, point):
			newPoints.append(point)
	for point in points:
		if onLine(B, point) and partOfPoly(A, point):
			newPoints.append(point)

	return sort(newPoints)

def CUTB(a,b):
	if not isinstance(A,list):
		A = A.points
	if not isinstance(B,list):
		B = B.points
	points = A+B
	newPoints = []
	for point in points:
		if onLine(A, point) and not partOfPoly(B, point):
			newPoints.append(point)
	for point in points:
		if onLine(B, point) and partOfPoly(A, point):
			newPoints.append(point)

	return sort(newPoints)


def onLine(poly, point):
	return point in poly

def partOfPoly(poly, test):
	point = Point(test[0],test[1])
	polygon = Polygon(poly)
	return polygon.contains(point)

def polyINpoly(polyA, polyB):
	for i in polyA:
		if not (partOfPoly(polyB, i) or onLine(polyB, i)):
			return False
	return True
