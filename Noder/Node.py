import pygame as pg

class Node:
    def __init__(self,base):
        self.base = pg.Rect(base)
        self.base.center = (base[0], base[1])
        self.click = False
        self.image = pg.Surface(self.base.size).convert()
        self.image.fill((255,0,0))
    def update(self,surface):
        if self.click:
            self.base.center = pg.mouse.get_pos()
        surface.blit(self.image,self.base)