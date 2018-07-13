class Node:
 
    def __init__(self, x, y, name):
       self.x = x
       self.y = y
       self.name = name
       self.code = open(name + '.txt', 'r').read()

    def update