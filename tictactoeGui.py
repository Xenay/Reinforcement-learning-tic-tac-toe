import numpy as np
import pickle
import tkinter as tk
from tkinter import messagebox

BOARD_ROWS = 3
BOARD_COLS = 3

class TicTacToeGUI:
    def __init__(self, master, player):
        self.master = master
        self.player = player
        self.board_buttons = [[None]*BOARD_COLS for _ in range(BOARD_ROWS)]

        for i in range(BOARD_ROWS):
            for j in range(BOARD_COLS):
                btn = tk.Button(master, text="", font=('normal', 20), width=5, height=2,
                                command=lambda row=i, col=j: self.on_button_click(row, col))
                btn.grid(row=i, column=j)
                self.board_buttons[i][j] = btn

    def on_button_click(self, row, col):
        action = (row, col)
        self.player.addState(self.player.getHash(self.get_board_state()))
        self.player.feedReward(0.1)  # Reward for the current move (you can adjust this)
        self.update_board(action)

    def update_board(self, action):
        if action in self.available_positions():
            self.master.event_generate("<<PlayMove>>", when="tail")
            self.board_buttons[action[0]][action[1]].config(text='X', state='disabled')
            if self.check_winner():
                messagebox.showinfo("Game Over", "You win!")
                self.reset_board()
            else:
                self.master.after(1000, self.computer_move)
        else:
            messagebox.showwarning("Invalid Move", "Invalid move. Please try again.")

    def computer_move(self):
        positions = self.available_positions()
        if positions:
            p2_action = self.player.chooseAction(positions)
            self.player.addState(self.player.getHash(self.get_board_state()))
            self.update_board(p2_action)
            if self.check_winner():
                messagebox.showinfo("Game Over", "Computer wins!")
                self.reset_board()
        else:
            messagebox.showinfo("Game Over", "It's a tie!")
            self.reset_board()

    def available_positions(self):
        positions = []
        for i in range(BOARD_ROWS):
            for j in range(BOARD_COLS):
                if self.board_buttons[i][j]['text'] == "":
                    positions.append((i, j))
        return positions

    def check_winner(self):
        # Check for a winner (you can implement this based on your existing code)
        return False

    def get_board_state(self):
        return np.array([[1 if self.board_buttons[i][j]['text'] == 'X' else 0 for j in range(BOARD_COLS)] for i in range(BOARD_ROWS)])

    def reset_board(self):
        for i in range(BOARD_ROWS):
            for j in range(BOARD_COLS):
                self.board_buttons[i][j].config(text='', state='normal')


if __name__ == "__main__":
    # Load trained model
    p1 = Player("computer", exp_rate=0)
    p1.loadPolicy("policy_p1")

    # Create the GUI
    root = tk.Tk()
    root.title("Tic Tac Toe")

    gui = TicTacToeGUI(root, p1)

    # Start the main loop
    root.mainloop()