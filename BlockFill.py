from tkinter import *
from random import randint
import time
import Block

class BlockFill():

    def __init__(self):
        # Creates TK Window and Frame
        self.tk = Tk()
        self.tk.resizable(0, 0)
        self.tk.title("Block Fill")
        frame = Frame(self.tk)
        frame.grid()

        # Creates Canvas and Grids it
        self.canvas = Canvas(frame, width= 580, height=800)
        self.canvas.grid(row=0, column = 0)
        
        # Binds Mouse Clicks to Functions
        self.canvas.bind_all("<Motion>", self.mousePointer)
        self.canvas.bind_all("<ButtonPress-1>", self.mouseClick)
        self.canvas.bind_all("<ButtonRelease-1>", self.mouseRelease)
    
        # Creates Display for Score and Board 
        self.scoreDisplay = self.canvas.create_text(290, 50, text = "Score: 0", font = ("Helvanica", 25))
        for i in range(11):
            self.canvas.create_line(40, i * 50 + 75, 540, i * 50 + 75)
        for i in range(11):
            self.canvas.create_line(i * 50 + 40, 75, i * 50 + 40, 575)
        
        # Initializes Variables
        ## Int Variables
        self.score = 0
        ## Bool Variables
        self.pressed = False
        ## Object Variables
        ## List Variables
        self.movingBlocks = []
        self.blockList = []
        self.xCenter = [ 65, 115, 165, 215, 265, 315, 365, 415, 465, 515]
        self.yCenter = [100, 150, 200, 250, 300, 350, 400, 450, 500, 550]
        self.board = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        
        # Creates Structures to Start Game
        self.createStructures()

    def createStructures(self):
        """
        Creates Structres if No Blocks Left Availible\n
        return -> None
        """
        usableCount = 0
        for block in self.blockList:
            if block.usable:
                usableCount += 1
        if usableCount == 0:
            for i in range(3):
                self.createRandomStruct(i)

    def createRandomStruct(self, pieceNumber):
        """
        Creates Random Stucture based off Presets\n
        return -> None
        """
        randomNum = randint(0, 1)
        structs = ["single", "TwoRight", "2by2", "3by3", "T", "Z", "4Line"]
        struct = structs[randomNum]
        if struct == "single":
            block = Block.ParentBlock(self.canvas, (pieceNumber+1) * 140, 700, (pieceNumber+1) * 140 + 50, 750)
            self.blockList.append(block)
        if struct == "TwoRight":
            father = Block.ParentBlock(self.canvas, (pieceNumber+1) * 140, 700, (pieceNumber+1) * 140 + 50, 750)
            self.blockList.append(father)
            block = Block.ChildBlock(self.canvas, parent = father, side =  "right")
            self.blockList.append(block)
            father.children.append(block)

    def clearSpace(self, rows, columns):
        """For Each Row and Column Destroy Blocks and Award Points"""
        for row in rows:
            self.score += 10
            for block in self.blockList:
                if block.row == row:
                    block.destroyBlock(self.board)
                    #self.blockList.remove(block)
        for column in columns:
            self.score += 10
            for block in self.blockList:
                if block.column == column:
                    block.destroyBlock(self.board)
                    #self.blockList.remove(block)

    def snapBoard(self):
        for block in self.movingBlocks:
            for i in range(len(self.xCenter)):
                for j in range(len(self.yCenter)):
                    if block.inRange(self.xCenter[i], self.yCenter[j]) and self.board[i][j] == 0:
                        try:
                            block = block.parent
                        except:
                            pass
                        for block in self.movingBlocks:
                            blockSnappable = False
                            for i in range(len(self.xCenter)):
                                for j in range(len(self.yCenter)):
                                    if block.inRange(self.xCenter[i], self.yCenter[j]) and self.board[i][j] == 0:
                                        blockSnappable = True
                        if not blockSnappable:
                            return False
                        for i in range(len(self.xCenter)):
                            for j in range(len(self.yCenter)):
                                for block in self.movingBlocks:
                                    if block.inRange(self.xCenter[i], self.yCenter[j]):
                                        block.snap(self.xCenter[i], self.yCenter[j])
                                        self.board[i][j] = 1
                                        block.placeOnBoard(i, j)
                                        self.score += 5
                                        return True

    def checkBoard(self):
        """For Each Row and Column See if Each is Filled Then Clear"""
        filledColumns = []
        filledRows = []
        for i in range(len(self.board)):
            columnFilled = True
            rowFilled = True
            for j in range(len(self.board[i])):
                if self.board[i][j] != 1:
                    columnFilled = False
                if self.board[j][i] != 1:
                    rowFilled = False
            if columnFilled:
                filledColumns.append(i)
            if rowFilled:
                filledRows.append(i)
        if len(filledRows) > 0 or len(filledColumns) > 0:
            self.clearSpace(filledColumns, filledRows)
        
    def mousePointer(self, e):
        """Transfers Mouse Movement to Block Movement"""
        if not self.pressed or not self.movingBlocks:
            return
        if e.x < 25:
            e.x = 25
        if e.x > 555:
            e.x = 555
        if e.y < 25:
            e.y = 25
        if e.y > 775:
            e.y = 775
        for block in self.movingBlocks:
            block.move(e.x, e.y)

    def mouseClick(self, e):
        """Upon Left Click, Find Out What Block Was Clicked, Set to Moving, Lighten Color"""
        self.pressed = True
        for block in self.blockList:
            if block.inRange(e.x, e.y):
                try:
                    block = block.parent
                except:
                    pass
                self.movingBlocks.append(block)
                self.movingBlocks.extend(block.children)
                for block in self.movingBlocks:
                    block.moving = True
                    self.canvas.itemconfig(block.block, fill = "Cyan")
    
    def mouseRelease(self, e):
        """
        Upon Left Click Release, Set Moving Block to False, Undo Color Change,\n
        If Snaped Check Board Else Undo Move\n
        Creates Structures
        """
        self.pressed = False
        if self.movingBlocks:
            for block in self.movingBlocks:
                block.moving = False
                self.canvas.itemconfig(block.block, fill = "Blue")
                if not self.snapBoard():
                    block.undoMove()
                else:
                    self.checkBoard()
                self.createStructures()
            self.movingBlocks = []

    def main(self):
        """
        Main Function\n
        Continuosly Updates Score Board\n
        Continuosly Updates Canvas\n
        return -> None
        """
        try:
            while True:
                time.sleep(.01)
                self.canvas.itemconfig(self.scoreDisplay, text = f"Score: {self.score}")
                self.tk.update()
                self.tk.update_idletasks()
        except:
            pass

# Starts Game
BlockFill().main()