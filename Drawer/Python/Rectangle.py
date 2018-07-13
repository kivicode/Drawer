from Line import Line
import Functions
import main
class Rect:
 
	def __init__(self, cornA, cornB, w, h, color=(255,255,255), points=None):
		self.corner = [cornA, cornB]
		self.width = w
		self.height = h
		self.color = color
		if points == None:
			self.points = self.get()
		else:
			self.points = points
		self.canDraw = True

	def dist(self, p1, p2):
		dist = math.sqrt( (p2[0] - p1[0])**2 + (p2[1] - p1[1])**2 )
		return dist

	def get(self):
		l1 = Line(self.corner,[self.corner[0]+self.width, self.corner[1]]).get()
		l2 = Line([self.corner[0]+self.width, self.corner[1]], [self.corner[0]+self.width, self.corner[1]+self.height]).get()
		l3 = Line([self.corner[0]+self.width, self.corner[1]+self.height], [self.corner[0], self.corner[1]+self.height]).get()
		l4 = Line([self.corner[0], self.corner[1]+self.height], self.corner).get()
		pts = l1+l2+l3+l4
		self.points = pts
		return pts

	def setPoints(self, npts):
		self.points = npts

	def nd(self, arg):
		self.canDraw = arg

	def draw(self, color = (255,255,255)):
		pts = np.array(self.points, np.int32)
		cv2.polylines(main.frame,[pts],True,color)

	def AND(self, A):
		self.points = Functions.AND(self, A)
		return self.points

	def CONCAT(self, *A):
		for i in A:
			self.points = Functions.CONCAT(self, i)
		self.canDraw = False
		return self.points

	def CUTA(self, A):
		self.points = Functions.CUTA(self, A)

	def CUTB(self, A):
		self.points = Functions.CUTB(self, A)