from Drawing.ParseArduino import eval

path = ["f(500)", "r(90)"]


def follow(way):
	for cmd in way:
		eval(cmd)