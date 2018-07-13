import serial
from time import sleep as delay
from Drawing.DrawWay import *
import BasicFunctions as bf

arduinoData = serial.Serial('/dev/tty.wchusbserial1410', 9600)
# delay(1000)
way = []

def forward(dist):
     arduinoData.write(('f(' + dist + ')').encode())
def backward(dist):
     arduinoData.write('b(' + dist + ')'.encode());
def left():
     arduinoData.write('left'.encode());
def right():
     arduinoData.write('right'.encode());

def parseTxt(filename):
	str = open(filename, 'r').read()
	for cmd in str.split(";"):
		print(cmd)
		arduinoData.write(cmd.encode())
		time.sleep(1)

def readString():
	count = 1
	seq = []
	for c in arduinoData.read():
		seq.append(chr(c))
		joined_seq = ''.join(str(v) for v in seq)

		if chr(c) == '\n':
			print("Line " + str(count) + ': ' + joined_seq)
			seq = []
			count += 1
			break

def waitFor(char):
	while readString() == "":
		print("waiting")
	print(readString())

def goHome():
	for str in way:
		arduinoData.write(str.encode())
		delay(1)

def eval(str):
	print(str)
	# bf.writeToFile("Commands", str)
	# drawWayPart(str)
	arduinoData.write(str.encode())
	delay(.5)
	# cmd = str.split("(")[0]
	# if cmd == "f":
	# 	way.append(str.replace("f", "b"))
	# if cmd == "b":
	# 	way.append(str.replace("b", "f"))
	# if cmd == "r":
	# 	way.append(str.replace("r", "l"))
	# if cmd == "l":
	# 	way.append(str.replace("l", "r"))

	# if cmd == "f" or cmd == "b":
	# 	delay(0.008*float(str.split("(")[1].split(")")[0]))
	# elif cmd == "l" or cmd == "r":
	# 	delay(0.055*float(str.split("(")[1].split(")")[0]))