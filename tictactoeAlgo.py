import tkinter as tk
from tkinter import messagebox
import numpy as np
import random


class TicTacToe:
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

    def make_move(self, row, col):
        if self.board[row, col] == 0:
            self.board[row, col] = 2
            self.buttons[row][col].config(text="X", state=tk.DISABLED)
            self.check_winner()
            self.ai_move()

    def ai_move(self):
        best_move = self.minimax(self.board, 1)
        self.board[best_move[0], best_move[1]] = 1
        self.buttons[best_move[0]][best_move[1]].config(
            text="O", state=tk.DISABLED)
        self.check_winner()

    def minimax(self, board, player):
        empty_cells = np.argwhere(board == 0)
        if self.check_winner(board) == 1:
            return -1, -1, 1
        elif self.check_winner(board) == 2:
            return -1, -1, -1
        elif len(empty_cells) == 0:
            return -1, -1, 0

        moves = []
        total_moves = len(empty_cells)
        for cell in empty_cells:
            board[cell[0], cell[1]] = player
            score = self.minimax(board, 3 - player)[2]
            board[cell[0], cell[1]] = 0
            moves.append((cell[0], cell[1], score))

        if player == 1:
            best_move = max(moves, key=lambda x: x[2])
            for move in moves:
                move_prob = (move[2] + 1) / 2
                move_percentage = round((move_prob / total_moves) * 100, 2)
                print(
                    f"Move {move[0]}, {move[1]}: Probability of winning = {move_percentage}%")
        else:
            best_move = min(moves, key=lambda x: x[2])

        return best_move

    def check_winner(self, board=None):
        if board is None:
            board = self.board

        for i in range(3):
            if all(board[i, j] == 2 for j in range(3)) or all(board[j, i] == 2 for j in range(3)):
                return 2

        if all(board[i, i] == 2 for i in range(3)) or all(board[i, 2 - i] == 2 for i in range(3)):
            return 2

        for i in range(3):
            if all(board[i, j] == 1 for j in range(3)) or all(board[j, i] == 1 for j in range(3)):
                return 1

        if all(board[i, i] == 1 for i in range(3)) or all(board[i, 2 - i] == 1 for i in range(3)):
            return 1

        if np.all(board != 0):
            return 0

        return -1

    def end_game(self, message):
        messagebox.showinfo("Game Over", message)
        self.window.destroy()

    def start(self):
        player_choice = input("Do you want to go first? (y/n): ").lower()
        if player_choice == 'y':
            print("You go first.")
        elif player_choice == 'n':
            print("AI goes first.")
            self.ai_move()
        else:
            print("Invalid choice. AI goes first by default.")
            self.ai_move()

        self.window.mainloop()


if __name__ == "__main__":
    game = TicTacToe()
    game.start()
