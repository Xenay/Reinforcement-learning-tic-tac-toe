# Import functions or classes from tictactoeAlgo.py
from tictactoeAlgo import State, Player

# Import functions or classes from tictactoefinalRein.py
from tictactoefinalRein import TicTacToe
import numpy as np
import pickle
import tkinter as tk

def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tic Tac Toe")
        self.board = np.zeros((3, 3), dtype=int)
        self.buttons = [[None for _ in range(3)] for _ in range(3)]

        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(self.window, text="", font=('normal', 20), height=2, width=5,
                                               command=lambda row=i, col=j: self.make_move(row, col))
                self.buttons[i][j].grid(row=i, column=j)



if __name__ == "__main__":
    #reinforcement
    p1 = Player("computer", exp_rate=0)
    p1.loadPolicy("policy_p1")
    
    
    
    
    