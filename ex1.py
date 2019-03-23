from tkinter import *
from random import randint
import time
import sys

def initMatrix(width, height):
    matrix = []
    for x in range(width):
        temp = []
        for y in range(height):
            b = Block()
            b.x = x*b.size
            b.y = y*b.size
            temp.append(b)
        matrix.append(temp)
    return matrix
def clamp(value, min, max):
    if value < min:
        return min
    if value > max:
        return max
    return value
def keyListener(event):
    global tetris
    
    key = event.keysym
    
    if key == 'Right':
        tetris.movePiece(1)
    elif key == 'Left':
        tetris.movePiece(-1)
    elif key == 'Down':
        tetris.movePiece()
    elif key == 'R':
        tetris.rotatePiece()
    elif key == 'Escape':
        sys.exit(0)

class Tetris:

    def __init__(self, window, width, height):
        self.canvas = Canvas(window, width=width, height=height, bg='gray')
        self.canvas.bind("<Key>", keyListener)
        self.canvas.focus_set()
        self.canvas.pack(side='left')
        self.speed = 1
        self.__matrix = initMatrix(10, 18)
        self.currentPiece = None
        self.nextPiece = None
    
    def tick(self):
        self.__drawMatrix()
        if self.currentPiece != None:
            self.currentPiece.tick(self.canvas, self)
        else:
            self.currentPiece = Piece()
        if self.nextPiece == None:
            self.__chooseNextPiece()
    
    def spawnNextPiece(self):
        self.currentPiece =  self.nextPiece
        self.nextPiece = None
    
    def movePiece(self, dir=0):
        if dir == 1:
            self.currentPiece.moveRight()
        elif dir == -1:
            self.currentPiece.moveLeft()
        else:
            self.currentPiece.gravity()

    def rotatePiece(self):
        self.currentPiece.rotate()

    def getMatrix(self):
        return self.__matrix

    def getSpeed(self):
        return self.speed

    def addDifficulty(self):
        self.speed = clamp(self.speed - 0.25, 0.1, 1)

    def __drawMatrix(self):
        for row in self.__matrix:
            for block in row:
                if block != None:
                    block.draw(self.canvas)

    def __chooseNextPiece(self):
        self.nextPiece = Piece()

class Block:

    def __init__(self):
        self.x = 0
        self.y = 0
        self.size = 30
        self.color = 'white'
    
    def draw(self, canvas, color='white'):
        canvas.create_rectangle(self.x, self.y, self.x+self.size, self.y+self.size, fill=color)
    
class Piece:

    def __init__(self):
        self.x = 0
        self.y = 0
        self.color = 'green'
        self.matrix = initMatrix(3, 3)
        self.matrix[0][0] = None
        self.matrix[1][0] = None
        self.matrix[2][0] = None
        self.matrix[0][1] = None
        self.matrix[2][1] = None

    def tick(self, canvas, tetris):
        self.__draw(canvas)
        if not(self.__isColliding(tetris.getMatrix())):
            self.gravity()
    
    def __draw(self, canvas):
        for row in self.matrix:
            for block in row:
                if block != None:
                    block.draw(canvas, self.color)
    
    def gravity(self):
        for row in self.matrix:
            for block in row:
                if block != None:
                    block.y += 30
        self.y += 30

    def moveRight(self):
        for row in self.matrix:
            for block in row:
                if block != None:
                    block.x += 30
        self.x += 30

    def moveLeft(self):
        for row in self.matrix:
            for block in row:
                if block != None:
                    block.x -= 30
        self.x -= 30

    def rotate(self):
        tempMatrix = initMatrix(3, 3)
        tempMatrix[1][1] = self.matrix[1][1]
        temp = []

        for value in self.matrix[2:][0]:
            temp.append(value)
        for y in range(3):
            tempMatrix[0][y] = temp[y]
        
        self.matrix = tempMatrix        


    def __isColliding(self, matrix):
        return False
        
def loop():
    tetris.tick()
    window.after(tetris.getSpeed()*1000, loop)

width = 300
height = 540

window = Tk()
window.resizable(False, False)
ws = window.winfo_screenwidth()
hs = window.winfo_screenheight()
x = (ws / 2) - (width / 2)
y = (hs / 2) - (height / 2)
window.geometry('%dx%d+%d+%d' % (width + 300, height, x, y))

tetris = Tetris(window, width, height)

window.after(tetris.getSpeed()*1000, loop)
window.mainloop()
