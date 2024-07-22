from tkinter import *

class Block():
    def __init__(self):
        self.moving = False
        self.usable = True
        self.placeable = False
        self.row  =  None
        self.column = None
        
    # def __repr__(self) -> str:
    #     """
    #     Returns the position of the block"""
    #     return f"({str(self.row)}, {str(self.column)})"

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
            return False
        x1, y1, x2, y2 = self.getCoordsSq()
        if x1 < x < x2:
            if y1 < y < y2:
                return True
        return False

    def getCoordsSq(self):
        """
        Returns Codinates of Block\n
        Returns x1, y1, x2, y2
        """
        return self.canvas.coords(self.block)
    
    def undoMove(self):
        """Resets Blocks Position to Position of Creation"""
        self.canvas.moveto(self.block, self.originalCoords[0], self.originalCoords[1])

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
        super().__init__()
        self.canvas = canvas
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.children = []
        self.buildBlock()
        self.originalCoords = self.getCoordsSq()

    def __repr__(self) -> str:
        return "Parent " + super().__repr__()

    def move(self, x, y):
        """Moves Block to Coordinates Then Resets Coordinates if Movable and Usable"""
        if self.moving and self.usable:
            self.canvas.moveto(self.block, x - 25, y - 25)
    
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
        self.rowDisplace = 0
        self.columnDisplace = 0
        self.canvas = canvas
        self.parent = parent
        self.side = side
        self.buildBlock()
        self.originalCoords = self.getCoordsSq()
    
    def __repr__(self) -> str:
        return f"Chlid: {self.side} " + super().__repr__()

    def move(self, x, y):
        """If Parent is Moving, Follow Parent"""
        if not self.usable:
            return
        if self.side == "right":
            self.canvas.moveto(self.block, x + 25, y - 25)
        if self.side == "doubleRight":
            self.canvas.moveto(self.block, x + 75, y - 25)
        if self.side == "left":
            self.canvas.moveto(self.block, x - 75, y - 25)
        if self.side == "doubleLeft":
            self.canvas.moveto(self.block, x - 125, y - 25)
        if self.side == "down":
            self.canvas.moveto(self.block, x - 25, y + 25)
        if self.side == "doubleDown":
            self.canvas.moveto(self.block, x - 25, y + 75)
        if self.side == "up":
            self.canvas.moveto(self.block, x - 25, y - 75)
        if self.side == "doubleUp":
            self.canvas.moveto(self.block, x - 25, y - 125)
        if self.side == "upRight":
            self.canvas.moveto(self.block, x + 25, y - 75)
        if self.side == "upLeft":
            self.canvas.moveto(self.block, x - 75, y - 75)
        if self.side == "downRight":
            self.canvas.moveto(self.block, x + 25, y + 25)
        if self.side == "downLeft":
            self.canvas.moveto(self.block, x - 75, y + 25)
        
    def buildBlock(self):
        """Creates Block on Corresponding Side to Parent"""
        x1, y1, x2, y2 = self.parent.getCoordsSq()
        if self.side == "right":
            self.block = self.canvas.create_rectangle(x1 + 50, y1, x2 + 50, y2, fill = "Blue")
            self.columnDisplace = 1
        if self.side == "doubleRight":
            self.block = self.canvas.create_rectangle(x1 + 100, y1, x2 + 100, y2, fill = "Blue")
            self.columnDisplace = 2
        if self.side == "left":
            self.block = self.canvas.create_rectangle(x1 - 50, y1, x2 - 50, y2, fill = "Blue")
            self.columnDisplace = -1
        if self.side == "doubleLeft":
            self.block = self.canvas.create_rectangle(x1 - 100, y1, x2 - 100, y2, fill = "Blue")
            self.columnDisplace = -2
        if self.side == "down":
            self.block = self.canvas.create_rectangle(x1, y1 + 50, x2, y2 + 50, fill = "Blue")
            self.rowDisplace = 1
        if self.side == "doubleDown":
            self.block = self.canvas.create_rectangle(x1, y1 + 100, x2, y2 + 100, fill = "Blue")
            self.rowDisplace = 2
        if self.side == "up":
            self.block = self.canvas.create_rectangle(x1, y1 - 50, x2, y2 - 50, fill = "Blue")
            self.rowDisplace = -1
        if self.side == "doubleUp":
            self.block = self.canvas.create_rectangle(x1, y1 - 100, x2, y2 - 100, fill = "Blue")
            self.rowDisplace = -2
        if self.side == "upRight":
            self.block = self.canvas.create_rectangle(x1 + 50, y1 - 50, x2 + 50, y2 - 50, fill = "Blue")
            self.rowDisplace = -1
            self.columnDisplace = 1
        if self.side == "upLeft":
            self.block = self.canvas.create_rectangle(x1 - 50, y1 - 50, x2 - 50, y2 - 50, fill = "Blue")
            self.rowDisplace = -1
            self.columnDisplace = -1
        if self.side == "downRight":
            self.block = self.canvas.create_rectangle(x1 + 50, y1 + 50, x2 + 50, y2 + 50, fill = "Blue")
            self.rowDisplace = 1
            self.columnDisplace = 1
        if self.side == "downLeft":
            self.block = self.canvas.create_rectangle(x1 - 50, y1 + 50, x2 - 50, y2 + 50, fill = "Blue")
            self.rowDisplace = 1
            self.columnDisplace = -1