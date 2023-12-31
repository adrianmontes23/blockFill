from tkinter import *
from tkinter import messagebox
from random import randint
import time
import Block
import os

class BlockFill():

    def __init__(self):
        # Creates TK Window and Frame
        self.tk = Tk()
        self.tk.resizable(0, 0)
        self.tk.title("Block Fill")
        self.tk.iconbitmap("icon.ico")
        self.tk.attributes('-topmost', True)
        self.tk.attributes('-topmost', False)
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
        with open("highScore.txt", "r") as highScoreFile:
            self.highScore = highScoreFile.readline()
        self.highScoreDisplay = self.canvas.create_text(100, 25, text = f"High Score: {self.highScore}", font = ("Helvanica", 15))
        self.giveUpDisplay = self.canvas.create_rectangle(455, 15, 545, 50)
        self.giveUpText = self.canvas.create_text(500, 32, text = "Give Up?", font = ("Helvanica", 15))
        for i in range(11):
            self.canvas.create_line(40, i * 50 + 75, 540, i * 50 + 75)
        for i in range(11):
            self.canvas.create_line(i * 50 + 40, 75, i * 50 + 40, 575)
        
        # Initializes Variables
        ## Int Variables
        self.score = 0
        ## Bool Variables
        self.pressed = False
        self.end = False
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
        structs = ["single", "TwoRight", "TwoUp", "2by2", "3by3", "cornerUpRight",
                    "TUp", "TDown", "TLeft", "TRight", "plus", "heroVert", "heroHori",
                    "cornerUpLeft", "cornerDownRight", "cornerDownLeft", "emptyCornerLeft", 
                    "emptyCornerRight", "LRight", "LLeft", "LUp", "LDown"]
        randomNum = randint(0, len(structs)-1)
        struct = structs[randomNum]
        if struct == "single":
            block = Block.ParentBlock(self.canvas, (pieceNumber+1) * 140, 700, (pieceNumber+1) * 140 + 50, 750)
            self.blockList.append(block)
        if struct == "TwoRight":
            father = Block.ParentBlock(self.canvas, (pieceNumber+1) * 140, 700, (pieceNumber+1) * 140 + 50, 750)
            self.blockList.append(father)
            block = Block.ChildBlock(self.canvas, parent = father, side = "right")
            self.blockList.append(block)
            father.children.append(block)
        if struct == "TwoUp":
            father = Block.ParentBlock(self.canvas, (pieceNumber+1) * 140, 700, (pieceNumber+1) * 140 + 50, 750)
            self.blockList.append(father)
            block = Block.ChildBlock(self.canvas, parent = father, side = "up")
            self.blockList.append(block)
            father.children.append(block)
        if struct == "2by2":
            father = Block.ParentBlock(self.canvas, (pieceNumber+1) * 140, 700, (pieceNumber+1) * 140 + 50, 750)
            self.blockList.append(father)
            block = Block.ChildBlock(self.canvas, parent = father, side = "right")
            self.blockList.append(block)
            father.children.append(block)
            block = Block.ChildBlock(self.canvas, parent = father, side = "up")
            self.blockList.append(block)
            father.children.append(block)
            block = Block.ChildBlock(self.canvas, parent = father, side = "upRight")
            self.blockList.append(block)
            father.children.append(block)
        if struct == "3by3":
            father = Block.ParentBlock(self.canvas, (pieceNumber+1) * 140, 700, (pieceNumber+1) * 140 + 50, 750)
            self.blockList.append(father)
            block = Block.ChildBlock(self.canvas, parent = father, side = "right")
            self.blockList.append(block)
            father.children.append(block)
            block = Block.ChildBlock(self.canvas, parent = father, side = "up")
            self.blockList.append(block)
            father.children.append(block)
            block = Block.ChildBlock(self.canvas, parent = father, side = "left")
            self.blockList.append(block)
            father.children.append(block)
            block = Block.ChildBlock(self.canvas, parent = father, side = "down")
            self.blockList.append(block)
            father.children.append(block)
            block = Block.ChildBlock(self.canvas, parent = father, side = "upRight")
            self.blockList.append(block)
            father.children.append(block)
            block = Block.ChildBlock(self.canvas, parent = father, side = "upLeft")
            self.blockList.append(block)
            father.children.append(block)
            block = Block.ChildBlock(self.canvas, parent = father, side = "downRight")
            self.blockList.append(block)
            father.children.append(block)
            block = Block.ChildBlock(self.canvas, parent = father, side = "downLeft")
            self.blockList.append(block)
            father.children.append(block)
        if struct == "cornerUpRight":
            father = Block.ParentBlock(self.canvas, (pieceNumber+1) * 140, 700, (pieceNumber+1) * 140 + 50, 750)
            self.blockList.append(father)
            block = Block.ChildBlock(self.canvas, parent = father, side = "right")
            self.blockList.append(block)
            father.children.append(block)
            block = Block.ChildBlock(self.canvas, parent = father, side = "up")
            self.blockList.append(block)
            father.children.append(block)
        if struct == "TUp":
            father = Block.ParentBlock(self.canvas, (pieceNumber+1) * 140, 700, (pieceNumber+1) * 140 + 50, 750)
            self.blockList.append(father)
            block = Block.ChildBlock(self.canvas, parent = father, side = "right")
            self.blockList.append(block)
            father.children.append(block)
            block = Block.ChildBlock(self.canvas, parent = father, side = "left")
            self.blockList.append(block)
            father.children.append(block)
            block = Block.ChildBlock(self.canvas, parent = father, side = "up")
            self.blockList.append(block)
            father.children.append(block)
        if struct == "TDown":
            father = Block.ParentBlock(self.canvas, (pieceNumber+1) * 140, 700, (pieceNumber+1) * 140 + 50, 750)
            self.blockList.append(father)
            block = Block.ChildBlock(self.canvas, parent = father, side = "right")
            self.blockList.append(block)
            father.children.append(block)
            block = Block.ChildBlock(self.canvas, parent = father, side = "left")
            self.blockList.append(block)
            father.children.append(block)
            block = Block.ChildBlock(self.canvas, parent = father, side = "down")
            self.blockList.append(block)
            father.children.append(block)
        if struct == "TLeft":
            father = Block.ParentBlock(self.canvas, (pieceNumber+1) * 140, 700, (pieceNumber+1) * 140 + 50, 750)
            self.blockList.append(father)
            block = Block.ChildBlock(self.canvas, parent = father, side = "down")
            self.blockList.append(block)
            father.children.append(block)
            block = Block.ChildBlock(self.canvas, parent = father, side = "left")
            self.blockList.append(block)
            father.children.append(block)
            block = Block.ChildBlock(self.canvas, parent = father, side = "up")
            self.blockList.append(block)
            father.children.append(block)
        if struct == "TRight":
            father = Block.ParentBlock(self.canvas, (pieceNumber+1) * 140, 700, (pieceNumber+1) * 140 + 50, 750)
            self.blockList.append(father)
            block = Block.ChildBlock(self.canvas, parent = father, side = "right")
            self.blockList.append(block)
            father.children.append(block)
            block = Block.ChildBlock(self.canvas, parent = father, side = "up")
            self.blockList.append(block)
            father.children.append(block)
            block = Block.ChildBlock(self.canvas, parent = father, side = "down")
            self.blockList.append(block)
            father.children.append(block)
        if struct == "plus":
            father = Block.ParentBlock(self.canvas, (pieceNumber+1) * 140, 700, (pieceNumber+1) * 140 + 50, 750)
            self.blockList.append(father)
            block = Block.ChildBlock(self.canvas, parent = father, side = "right")
            self.blockList.append(block)
            father.children.append(block)
            block = Block.ChildBlock(self.canvas, parent = father, side = "up")
            self.blockList.append(block)
            father.children.append(block)
            block = Block.ChildBlock(self.canvas, parent = father, side = "left")
            self.blockList.append(block)
            father.children.append(block)
            block = Block.ChildBlock(self.canvas, parent = father, side = "down")
            self.blockList.append(block)
            father.children.append(block)
        if struct == "heroVert":
            father = Block.ParentBlock(self.canvas, (pieceNumber+1) * 140, 700, (pieceNumber+1) * 140 + 50, 750)
            self.blockList.append(father)
            block = Block.ChildBlock(self.canvas, parent = father, side = "doubleUp")
            self.blockList.append(block)
            father.children.append(block)
            block = Block.ChildBlock(self.canvas, parent = father, side = "up")
            self.blockList.append(block)
            father.children.append(block)
            block = Block.ChildBlock(self.canvas, parent = father, side = "down")
            self.blockList.append(block)
            father.children.append(block)
        if struct == "heroHori":
            father = Block.ParentBlock(self.canvas, (pieceNumber+1) * 140, 700, (pieceNumber+1) * 140 + 50, 750)
            self.blockList.append(father)
            block = Block.ChildBlock(self.canvas, parent = father, side = "right")
            self.blockList.append(block)
            father.children.append(block)
            block = Block.ChildBlock(self.canvas, parent = father, side = "left")
            self.blockList.append(block)
            father.children.append(block)
            block = Block.ChildBlock(self.canvas, parent = father, side = "doubleRight")
            self.blockList.append(block)
            father.children.append(block)
        if struct == "cornerUpLeft":
            father = Block.ParentBlock(self.canvas, (pieceNumber+1) * 140, 700, (pieceNumber+1) * 140 + 50, 750)
            self.blockList.append(father)
            block = Block.ChildBlock(self.canvas, parent = father, side = "left")
            self.blockList.append(block)
            father.children.append(block)
            block = Block.ChildBlock(self.canvas, parent = father, side = "up")
            self.blockList.append(block)
            father.children.append(block)
        if struct == "cornerDownLeft":
            father = Block.ParentBlock(self.canvas, (pieceNumber+1) * 140, 700, (pieceNumber+1) * 140 + 50, 750)
            self.blockList.append(father)
            block = Block.ChildBlock(self.canvas, parent = father, side = "left")
            self.blockList.append(block)
            father.children.append(block)
            block = Block.ChildBlock(self.canvas, parent = father, side = "down")
            self.blockList.append(block)
            father.children.append(block)
        if struct == "cornerDownRight":
            father = Block.ParentBlock(self.canvas, (pieceNumber+1) * 140, 700, (pieceNumber+1) * 140 + 50, 750)
            self.blockList.append(father)
            block = Block.ChildBlock(self.canvas, parent = father, side = "right")
            self.blockList.append(block)
            father.children.append(block)
            block = Block.ChildBlock(self.canvas, parent = father, side = "down")
            self.blockList.append(block)
            father.children.append(block)
        if struct == "emptyCornerRight":
            father = Block.ParentBlock(self.canvas, (pieceNumber+1) * 140, 700, (pieceNumber+1) * 140 + 50, 750)
            self.blockList.append(father)
            block = Block.ChildBlock(self.canvas, parent = father, side = "upRight")
            self.blockList.append(block)
            father.children.append(block)
        if struct == "emptyCornerLeft":
            father = Block.ParentBlock(self.canvas, (pieceNumber+1) * 140, 700, (pieceNumber+1) * 140 + 50, 750)
            self.blockList.append(father)
            block = Block.ChildBlock(self.canvas, parent = father, side = "upLeft")
            self.blockList.append(block)
            father.children.append(block)
        if struct == "LRight":
            father = Block.ParentBlock(self.canvas, (pieceNumber+1) * 140, 700, (pieceNumber+1) * 140 + 50, 750)
            self.blockList.append(father)
            block = Block.ChildBlock(self.canvas, parent = father, side = "right")
            self.blockList.append(block)
            father.children.append(block)
            block = Block.ChildBlock(self.canvas, parent = father, side = "up")
            self.blockList.append(block)
            father.children.append(block)
            block = Block.ChildBlock(self.canvas, parent = father, side = "doubleUp")
            self.blockList.append(block)
            father.children.append(block)
        if struct == "LLeft":
            father = Block.ParentBlock(self.canvas, (pieceNumber+1) * 140, 700, (pieceNumber+1) * 140 + 50, 750)
            self.blockList.append(father)
            block = Block.ChildBlock(self.canvas, parent = father, side = "upLeft")
            self.blockList.append(block)
            father.children.append(block)
            block = Block.ChildBlock(self.canvas, parent = father, side = "down")
            self.blockList.append(block)
            father.children.append(block)
            block = Block.ChildBlock(self.canvas, parent = father, side = "up")
            self.blockList.append(block)
            father.children.append(block)
        if struct == "LUp":
            father = Block.ParentBlock(self.canvas, (pieceNumber+1) * 140, 700, (pieceNumber+1) * 140 + 50, 750)
            self.blockList.append(father)
            block = Block.ChildBlock(self.canvas, parent = father, side = "up")
            self.blockList.append(block)
            father.children.append(block)
            block = Block.ChildBlock(self.canvas, parent = father, side = "left")
            self.blockList.append(block)
            father.children.append(block)
            block = Block.ChildBlock(self.canvas, parent = father, side = "doubleLeft")
            self.blockList.append(block)
            father.children.append(block)
        if struct == "LDown":
            father = Block.ParentBlock(self.canvas, (pieceNumber+1) * 140, 700, (pieceNumber+1) * 140 + 50, 750)
            self.blockList.append(father)
            block = Block.ChildBlock(self.canvas, parent = father, side = "down")
            self.blockList.append(block)
            father.children.append(block)
            block = Block.ChildBlock(self.canvas, parent = father, side = "right")
            self.blockList.append(block)
            father.children.append(block)
            block = Block.ChildBlock(self.canvas, parent = father, side = "doubleRight")
            self.blockList.append(block)
            father.children.append(block)

    def clearSpace(self, rows, columns):
        """For Each Row and Column Destroy Blocks and Award Points"""
        combo = 1
        for row in rows:
            self.score += 50 * combo
            combo += 1
            for block in self.blockList:
                if block.row == row:
                    block.destroyBlock(self.board)
        for column in columns:
            self.score += 50 * combo
            combo += 1
            for block in self.blockList:
                if block.column == column:
                    block.destroyBlock(self.board)

    def snapBoard(self):
        for block in self.movingBlocks:
            snappable = False
            for i in range(len(self.xCenter)):
                for j in range(len(self.yCenter)):
                    if block.inRange(self.xCenter[i], self.yCenter[j]) and self.board[i][j] == 0:
                        snappable = True
            if not snappable:
                return False
        for block in self.movingBlocks:
            for i in range(len(self.xCenter)):
                for j in range(len(self.yCenter)):
                    if block.inRange(self.xCenter[i], self.yCenter[j]):
                        block.snap(self.xCenter[i], self.yCenter[j])
                        self.board[i][j] = 1
                        block.placeOnBoard(i, j)
                        self.score += 5
        return True
                    
    def undoBlocks(self):
        for block in self.movingBlocks:
            block.undoMove()

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
        if 455 < e.x < 545:
            if 15 < e.y < 50:
                self.endGame()
                return
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
                break
    
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
                self.undoBlocks()
            else:
                self.checkBoard()
            self.createStructures()
            self.movingBlocks = []

    def endGame(self, killed = False):
        self.end = True
        if int(self.highScore) < self.score:
            os.system("attrib -h highScore.txt")
            with open("highScore.txt", "w") as highScoreFile:
                highScoreFile.writelines(f"{self.score}")
            os.system("attrib +h highScore.txt")
            if messagebox.askyesno(title = f"NEW HIGH SCORE: {self.score}", message = "Would You Like To Play Again?"):
                if not killed:
                    self.tk.destroy()
                BlockFill().main()
        else:
            if messagebox.askyesno(title = "Good Game", message = "Would You Like To Play Again?"):
                if not killed:
                    self.tk.destroy()
                BlockFill().main()

    def main(self):
        """
        Main Function\n
        Continuosly Updates Score Board\n
        Continuosly Updates Canvas\n
        return -> None
        """
        while True:
            if self.end:
                break
            try:
                time.sleep(.01)
                self.canvas.itemconfig(self.scoreDisplay, text = f"Score: {self.score}")
                self.tk.update()
                self.tk.update_idletasks()
            except:
                self.endGame(True)

BlockFill().main()