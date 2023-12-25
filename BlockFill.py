from tkinter import *
import time
import Block

class BlockFill():

    def __init__(self):
        self.tk = Tk()
        self.tk.resizable(0, 0)
        frame = Frame(self.tk)
        frame.grid()
        
        #960 × 540
        self.canvas = Canvas(frame, width= 580, height=800)
        self.canvas.grid(row=0, column = 0)
        
        self.canvas.bind_all("<Motion>", self.mousePointer)
        self.canvas.bind_all("<ButtonPress-1>", self.mouseClick)
        self.canvas.bind_all("<ButtonRelease-1>", self.mouseRelease)

        for i in range(11):
            self.canvas.create_line(40, i * 50 + 75, 540, i * 50 + 75)
        for i in range(11):
            self.canvas.create_line(i * 50 + 40, 75, i * 50 + 40, 575)

        self.pressed = False
        self.blockList = []
        self.movingBlock = None

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
        self.xCenter = [ 65, 115, 165, 215, 265, 315, 365, 415, 465, 515]
        self.yCenter = [100, 150, 200, 250, 300, 350, 400, 450, 500, 550]

        for i in range(3):
            self.blockList.append(Block.Block(self.canvas, (i+1) * 140, 700, (i+1) * 140 + 50, 750))

    def snapBoard(self):
        for block in self.blockList:
            for i in range(len(self.xCenter)):
                for j in range(len(self.xCenter)):
                    if block.inRange(self.xCenter[i], self.yCenter[j]):
                        block.snap(self.xCenter[i], self.yCenter[j])
                    
        
    def mousePointer(self, e):
        if not self.pressed or self.movingBlock == None:
            return
        if e.x < 25:
            e.x = 25
        if e.x > 555:
            e.x = 555
        if e.y < 25:
            e.y = 25
        if e.y > 775:
            e.y = 775
        self.movingBlock.move(e.x, e.y)

    def mouseClick(self, e):
        self.pressed = True
        for block in self.blockList:
            if block.inRange(e.x, e.y):
                self.movingBlock = block
                self.movingBlock.movable = True
                self.canvas.itemconfig(self.movingBlock.block, fill = "Cyan")

    def mouseRelease(self, e):
        self.pressed = False
        if self.movingBlock:
            self.movingBlock.movable = False
            self.canvas.itemconfig(self.movingBlock.block, fill = "Blue")
            self.snapBoard()

    def main(self):
        while True:
            time.sleep(.01)
            self.tk.update()
            self.tk.update_idletasks()

BlockFill().main()