'''
This is my senior project in which I'll be building a mjinlieff game with an AI
 Current flow:
    game->players->board/pieces->rules->check->win
                ↳AI->MCTS->move->wait->check->continue if need

Work this week 8/27/2018 finish basic game.
'''
from tkinter import *
from tkinter import messagebox


class Piece:

    def __init__(self, piece, x, y):
        self.piece = piece
        self.x = x
        self.y = y

class Game:
    def __init__(self, parent):
        parent.title("Mjinlieff")
        self.parent = parent
        self.root = Tk()
        self.canvas = Canvas(self.root, width = 700, height= 700)
        self.canvas.pack()
        self.menubar = Menu(self.root)


    def runGame(self):

    def players(self, aiCheck):
        if aiCheck == 1:
            pass
        else:
            pass

    def createGhostBoard(self, width, height):
        pass

    def selectBoardPiece(self):
        pass

    def createTopBoard(self):
        pass

    def rules(self):
        pass

    def checkRules(self):
        pass

    def checkWin(self):
        pass

    def changeAvailableSpaces(self):
        pass



print()