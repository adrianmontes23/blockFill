from tkinter import *

class Block():
    def __init__(self, canvas, x1, y1, x2, y2):
        self.canvas = canvas
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill = "Blue")
        self.movable = True

    def inRange(self, x, y):
        if self.x1 < x < self.x2:
            if self.y1 < y < self.y2:
                return True
        return False