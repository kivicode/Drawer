import pygame as pg
import os,sys
import cv2
from Node import *

nodes = []

def addNode(base):
	nodes.append(Node((pg.mouse.get_pos()[0], pg.mouse.get_pos()[1], 50, 50)))

def clearNodes():
	nodes = []

def main(Surface,Player):
    game_event_loop(Player)
    Surface.fill(0)
    Player.update(Surface)

def mouseX():
	return pg.mouse.get_pos()[0]

def mouseY():
	return pg.mouse.get_pos()[1]


def game_event_loop(Player):
	for event in pg.event.get():
		if event.type == pg.MOUSEBUTTONDOWN:
			if Player.base.collidepoint(event.pos):
				Player.click = True
		elif event.type == pg.MOUSEBUTTONUP:
			Player.click = False
		elif event.type == pg.QUIT:
			pg.quit(); sys.exit()
		if event.type == pg.KEYDOWN:
			print(event.key)
			if event.key == pg.K_LEFT:
				print("l")
			if event.key == pg.K_RIGHT:
				print("r")
			if event.key == pg.K_a:
				addNode((mouseX(), mouseY(), 50, 50))


if __name__ == "__main__":

	os.environ['SDL_VIDEO_CENTERED'] = '1'
	pg.init()
	Screen = pg.display.set_mode((1000,600))

	addNode((mouseX(), mouseY(), 50, 50))

	while 1:
		for node in nodes:
			main(Screen,node)
		pg.display.update()
		