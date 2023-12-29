from tkinter import *

class Block():
    def __init__(self):
        self.moving = False
        self.usable = True
        self.row  =  None
        self.column = None

    def placeOnBoard(self, row, column):
        """Gets Row and Column and Makes Block Unmovable"""
        self.row = row
        self.column = column
        self.usable = False

    def inRange(self, x, y):
        """
        If the Block is Usable, Check If in Range of Coordinates Returns if Unsuable\n
        Returns True if Within Range\n
        Returns False if Not Within Range
        """
        if not self.usable:
            return
        if self.x1 < x < self.x2:
            if self.y1 < y < self.y2:
                return True
        return False
    
    def getCoordsSq(self):
        """
        Returns Codinates of Block\n
        Returns x1, y1, x2, y2
        """
        return self.canvas.coords(self.block)
    
    def resetCoords(self):
        """Resets x and y Coordinates to current Coordinates"""
        coords = self.getCoordsSq()
        self.x1 = coords[0]
        self.y1 = coords[1]
        self.x2 = coords[2]
        self.y2 = coords[3]
    
    def undoMove(self):
        """Resets Blocks Position to Position of Creation"""
        self.canvas.moveto(self.block, self.originalCoords[0], self.originalCoords[1])
        self.resetCoords()

    def destroyBlock(self, board):
        """
        Removes Block From Canvas\n
        Resets Board Position to Default
        """
        self.canvas.delete(self.block)
        board[self.row][self.column] = 0
        self.block

    def snap(self, x, y):
        if not self.usable:
            return 
        self.canvas.moveto(self.block, x - 25, y - 25)

class ParentBlock(Block):
    def __init__(self, canvas, x1, y1, x2, y2):
        self.canvas = canvas
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.children = []
        self.buildBlock()
        super().__init__()
        self.originalCoords = self.getCoordsSq()

    def move(self, x, y):
        """Moves Block to Coordinates Then Resets Coordinates if Movable and Usable"""
        if self.moving and self.usable:
            self.canvas.moveto(self.block, x - 25, y - 25)
            for child in self.children:
                child.move(0, 0)
            super().resetCoords()
    
    def buildBlock(self):
        """Creates Block on Canvas"""
        self.block = self.canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill = "Blue")

class ChildBlock(Block):
    def __init__(self, canvas, parent=None, side=None):
        super().__init__()
        self.x1 = 0
        self.y1 = 0
        self.x2 = 0
        self.y2 = 0
        self.canvas = canvas
        self.parent = parent
        self.side = side
        self.buildBlock()
        self.originalCoords = self.getCoordsSq()

    def move(self, x, y):
        """If Parent is Moving, Follow Parent"""
        if not self.parent.moving:
            return
        x1, y1, x2, y2 = self.parent.getCoordsSq()
        if self.side == "right":
            self.canvas.moveto(self.block, x1 + 50, y1)
            self.resetCoords()

    
    def buildBlock(self):
        """Creates Block on Corresponding Side to Parent, Then Resets Coordinates"""
        x1, y1, x2, y2 = self.parent.getCoordsSq()
        if self.side == "right":
            self.block = self.canvas.create_rectangle(x1 + 50, y1, x2 + 50, y2, fill = "Blue")
            self.resetCoords()