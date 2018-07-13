import serial

arduinoData = serial.Serial('/dev/tty.wchusbserial1410', 9600)


def forward(dist):
     arduinoData.write(('forward(' + str(dist) + ')').encode())
def backward(dist):
     arduinoData.write('backward(' + dist + ')'.encode());
def left():
     arduinoData.write('left'.encode());
def right():
     arduinoData.write('right'.encode());

def parseTxt(filename):
	str = open(filename, 'r').read()
	arduinoData.write('f(100)'encode())