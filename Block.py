from tkinter import *

class Block():
    def __init__(self, canvas, x1, y1, x2, y2):
        self.canvas = canvas
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.block = self.canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill = "Blue")
        self.originalCoords = self.canvas.coords(self.block)
        self.moving = False
        self.usable = True

    def inRange(self, x, y):
        if not self.usable:
            return
        if self.x1 < x < self.x2:
            if self.y1 < y < self.y2:
                return True
        self.moving = False
        return False
    
    def inBoard(self, x, y):
        if not self.usable:
            return
        if self.x1 < x < self.x2:
            if self.y1 < y < self.y2:
                return True
        return False
    
    def getCoordsSq(self):
        return self.x1, self.y1, self.x2, self.y2
    
    def getCoords(self):
        return self.canvas.coords(self.block)
    
    def resetCoords(self):
        coords = self.getCoords()
        self.x1 = coords[0]
        self.y1 = coords[1]
        self.x2 = coords[0] + 50
        self.y2 = coords[1] + 50 
    
    def undoMove(self):
        self.canvas.moveto(self.block, self.originalCoords[0], self.originalCoords[1])
        self.resetCoords()

    def snap(self, x, y):
        if not self.usable:
            return
        self.canvas.moveto(self.block, x - 25, y - 25)

    def move(self, x, y):
        if self.moving and self.usable:
            self.canvas.moveto(self.block, x - 25, y - 25)
            self.resetCoords()           