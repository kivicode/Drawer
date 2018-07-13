import Functions
import math
import main
class Circle:
	def __init__(self, c, r):
		self.center = c
		self.radius = r/2
		self.points = self.get()
		self.canDraw = True

	def get(self):
		out = [];
		for i in range(0, 360):
			angle = math.degrees(360-i);
			x = self.center[0]+math.cos(angle)*self.radius;
			y = self.center[1]+math.sin(angle)*self.radius;
			out.append([x, y]);
			
		self.points = Functions.sort(out)
		return self.points;

	def draw(self, color = (255,255,255)):
		pts = np.array(self.points, np.int32)
		cv2.polylines(main.frame,[pts],True,color)