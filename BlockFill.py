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
        self.canvas = Canvas(frame, width= 580, height=960)
        self.canvas.grid(row=0, column = 0)
        
        self.canvas.bind_all("<Motion>", self.mousePointer)
        self.canvas.bind_all("<ButtonPress-1>", self.mouseClick)
        self.canvas.bind_all("<ButtonRelease-1>", self.mouseRelease)

        for i in range(11):
            self.canvas.create_line(40, i * 50 + 100, 540, i * 50 + 100)
        for i in range(11):
            self.canvas.create_line(i * 50 + 40, 100, i * 50 + 40, 600)

        self.pressed = False
        self.blockList = []

        for i in range(3):
            self.blockList.append(Block.Block(self.canvas, (i+1) * 140, 700, (i+1) * 140 + 50, 750))
        
    def mousePointer(self, e):
        if not self.pressed:
            return
        for block in self.blockList:
            print(block.inRange(e.x, e.y))

    def mouseClick(self, e):
        self.pressed = True

    def mouseRelease(self, e):
        self.pressed = False

    def main(self):
        while True:
            time.sleep(.1)
            self.tk.update()
            self.tk.update_idletasks()

BlockFill().main()