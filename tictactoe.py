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
        self.board_buttons = [[None] * BOARD_COLS for _ in range(BOARD_ROWS)]

        for i in range(BOARD_ROWS):
            for j in range(BOARD_COLS):
                btn = tk.Button(master, text="", font=('normal', 20), width=5, height=2,
                                command=lambda row=i, col=j: self.on_button_click(row, col))
                btn.grid(row=i, column=j)
                self.board_buttons[i][j] = btn

        # Start the game with the computer's move
        self.computer_move()

    def on_button_click(self, row, col):
        if self.board_buttons[row][col]['text'] == '':
            action = (row, col)
            self.player.addState(self.player.getHash(self.get_board_state()))
            self.player.feedReward(0.1)  # Reward for the current move (you can adjust this)
            self.update_board(action, is_player=True)

            # Check for a winner or tie after player's move
            if self.check_winner():
                messagebox.showinfo("Game Over", "You win!")
                self.reset_board()
            elif not self.available_positions():
                messagebox.showinfo("Game Over", "It's a tie!")
                self.reset_board()
            else:
                # After the player's move, let the computer make its move
                self.master.after(1000, self.computer_move)

    def computer_move(self):
        positions = self.available_positions()
        if positions:
            current_board = self.get_board_state()
            p2_action = self.player.chooseAction(positions, current_board, -1)  # Assuming computer plays with symbol -1
            self.player.addState(self.player.getHash(current_board))
            self.update_board(p2_action, is_player=False)

            # Check for a winner or tie after computer's move
            if self.check_winner():
                messagebox.showinfo("Game Over", "Computer wins!")
                self.reset_board()
            elif not self.available_positions():
                messagebox.showinfo("Game Over", "It's a tie!")
                self.reset_board()
        else:
            messagebox.showinfo("Game Over", "It's a tie!")
            self.reset_board()

    def update_board(self, action, is_player=True):
        symbol = 'O' if is_player else 'X'
        if self.board_buttons[action[0]][action[1]]['text'] == '':
            self.board_buttons[action[0]][action[1]].config(text=symbol, state='disabled')

    def available_positions(self):
        positions = []
        for i in range(BOARD_ROWS):
            for j in range(BOARD_COLS):
                if self.board_buttons[i][j]['text'] == '':
                    positions.append((i, j))
        return positions

    def check_winner(self):
        # Check for a winner (you need to implement your own logic)
        for i in range(BOARD_ROWS):
            if self.board_buttons[i][0]['text'] == self.board_buttons[i][1]['text'] == self.board_buttons[i][2]['text'] != '':
                return True  # Horizontal win
            if self.board_buttons[0][i]['text'] == self.board_buttons[1][i]['text'] == self.board_buttons[2][i]['text'] != '':
                return True  # Vertical win

        if self.board_buttons[0][0]['text'] == self.board_buttons[1][1]['text'] == self.board_buttons[2][2]['text'] != '':
            return True  # Diagonal win
        if self.board_buttons[0][2]['text'] == self.board_buttons[1][1]['text'] == self.board_buttons[2][0]['text'] != '':
            return True  # Diagonal win

        return False

    def get_board_state(self):
        return np.array([[-1 if self.board_buttons[i][j]['text'] == 'X' else 0 for j in range(BOARD_COLS)] for i in range(BOARD_ROWS)])

    def reset_board(self):
        for i in range(BOARD_ROWS):
            for j in range(BOARD_COLS):
                self.board_buttons[i][j].config(text='', state='normal')
class State:
    def __init__(self, p1, p2):
        self.board = np.zeros((BOARD_ROWS, BOARD_COLS))
        self.p1 = p1
        self.p2 = p2
        self.isEnd = False
        self.boardHash = None
        # init p1 plays first
        self.playerSymbol = 1

    # get unique hash of current board state
    def getHash(self):
        self.boardHash = str(self.board.reshape(BOARD_COLS * BOARD_ROWS))
        return self.boardHash

    def winner(self):
        # row
        for i in range(BOARD_ROWS):
            if sum(self.board[i, :]) == 3:
                self.isEnd = True
                return 1
            if sum(self.board[i, :]) == -3:
                self.isEnd = True
                return -1
        # col
        for i in range(BOARD_COLS):
            if sum(self.board[:, i]) == 3:
                self.isEnd = True
                return 1
            if sum(self.board[:, i]) == -3:
                self.isEnd = True
                return -1
        # diagonal
        diag_sum1 = sum([self.board[i, i] for i in range(BOARD_COLS)])
        diag_sum2 = sum([self.board[i, BOARD_COLS - i - 1] for i in range(BOARD_COLS)])
        diag_sum = max(abs(diag_sum1), abs(diag_sum2))
        if diag_sum == 3:
            self.isEnd = True
            if diag_sum1 == 3 or diag_sum2 == 3:
                return 1
            else:
                return -1

        # tie
        # no available positions
        if len(self.availablePositions()) == 0:
            self.isEnd = True
            return 0
        # not end
        self.isEnd = False
        return None

    def availablePositions(self):
        positions = []
        for i in range(BOARD_ROWS):
            for j in range(BOARD_COLS):
                if self.board[i, j] == 0:
                    positions.append((i, j))  # need to be tuple
        return positions

    def updateState(self, position):
        self.board[position] = self.playerSymbol
        # switch to another player
        self.playerSymbol = -1 if self.playerSymbol == 1 else 1

    # only when game ends
    def giveReward(self):
        result = self.winner()
        # backpropagate reward
        if result == 1:
            self.p1.feedReward(1)
            self.p2.feedReward(0)
        elif result == -1:
            self.p1.feedReward(0)
            self.p2.feedReward(1)
        else:
            self.p1.feedReward(0.1)
            self.p2.feedReward(0.5)

    # board reset
    def reset(self):
        self.board = np.zeros((BOARD_ROWS, BOARD_COLS))
        self.boardHash = None
        self.isEnd = False
        self.playerSymbol = 1

    def play(self, rounds=100):
        for i in range(rounds):
            if i % 1000 == 0:
                print("Rounds {}".format(i))
            while not self.isEnd:
                # Player 1
                positions = self.availablePositions()
                p1_action = self.p1.chooseAction(positions, self.board, self.playerSymbol)
                # take action and upate board state
                self.updateState(p1_action)
                board_hash = self.getHash()
                self.p1.addState(board_hash)
                # check board status if it is end

                win = self.winner()
                if win is not None:
                    # self.showBoard()
                    # ended with p1 either win or draw
                    self.giveReward()
                    self.p1.reset()
                    self.p2.reset()
                    self.reset()
                    break

                else:
                    # Player 2
                    positions = self.availablePositions()
                    p2_action = self.p2.chooseAction(positions, self.board, self.playerSymbol)
                    self.updateState(p2_action)
                    board_hash = self.getHash()
                    self.p2.addState(board_hash)

                    win = self.winner()
                    if win is not None:
                        # self.showBoard()
                        # ended with p2 either win or draw
                        self.giveReward()
                        self.p1.reset()
                        self.p2.reset()
                        self.reset()
                        break

    # play with human
    def play2(self):
        while not self.isEnd:
            # Player 1
            positions = self.availablePositions()
            p1_action = self.p1.chooseAction(positions, self.board, self.playerSymbol)
            # take action and upate board state
            self.updateState(p1_action)
            self.showBoard()
            # check board status if it is end
            win = self.winner()
            if win is not None:
                if win == 1:
                    print(self.p1.name, "wins!")
                else:
                    print("tie!")
                self.reset()
                break

            else:
                # Player 2
                positions = self.availablePositions()
                p2_action = self.p2.chooseAction(positions)

                self.updateState(p2_action)
                self.showBoard()
                win = self.winner()
                if win is not None:
                    if win == -1:
                        print(self.p2.name, "wins!")
                    else:
                        print("tie!")
                    self.reset()
                    break

    def showBoard(self):
        # p1: x  p2: o
        for i in range(0, BOARD_ROWS):
            print('-------------')
            out = '| '
            for j in range(0, BOARD_COLS):
                if self.board[i, j] == 1:
                    token = 'x'
                if self.board[i, j] == -1:
                    token = 'o'
                if self.board[i, j] == 0:
                    token = ' '
                out += token + ' | '
            print(out)
        print('-------------')


class Player:
    def __init__(self, name, exp_rate=0.3):
        self.name = name
        self.states = []  # record all positions taken
        self.lr = 0.2
        self.exp_rate = exp_rate
        self.decay_gamma = 0.9
        self.states_value = {}  # state -> value

    def getHash(self, board):
        boardHash = str(board.reshape(BOARD_COLS * BOARD_ROWS))
        return boardHash

    def chooseAction(self, positions, current_board, symbol):
        if np.random.uniform(0, 1) <= self.exp_rate:
            # take random action
            idx = np.random.choice(len(positions))
            action = positions[idx]
        else:
            value_max = -999
            for p in positions:
                next_board = current_board.copy()
                next_board[p] = symbol
                next_boardHash = self.getHash(next_board)
                value = 0 if self.states_value.get(next_boardHash) is None else self.states_value.get(next_boardHash)
                # print("value", value)
                if value >= value_max:
                    value_max = value
                    action = p
        # print("{} takes action {}".format(self.name, action))
        return action

    # append a hash state
    def addState(self, state):
        self.states.append(state)

    # at the end of game, backpropagate and update states value
    def feedReward(self, reward):
        for st in reversed(self.states):
            if self.states_value.get(st) is None:
                self.states_value[st] = 0
            self.states_value[st] += self.lr * (self.decay_gamma * reward - self.states_value[st])
            reward = self.states_value[st]

    def reset(self):
        self.states = []

    def savePolicy(self):
        fw = open('policy_' + str(self.name), 'wb')
        pickle.dump(self.states_value, fw)
        fw.close()

    def loadPolicy(self, file):
        fr = open(file, 'rb')
        self.states_value = pickle.load(fr)
        fr.close()


class HumanPlayer:
    def __init__(self, name):
        self.name = name

    def chooseAction(self, positions):
        while True:
            row = int(input("Input your action row:"))
            col = int(input("Input your action col:"))
            action = (row, col)
            if action in positions:
                return action

    # append a hash state
    def addState(self, state):
        pass

    # at the end of game, backpropagate and update states value
    def feedReward(self, reward):
        pass

    def reset(self):
        pass


if __name__ == "__main__":
    # Training
    p1 = Player("p1")
    p2 = Player("p2")

    st = State(p1, p2)
    print("Training...")
    st.play(100000)
    
    # Save the trained policy
    p1.savePolicy()

    # Play with GUI
    p1 = Player("computer", exp_rate=0)
    p1.loadPolicy("policy_p1")

    # Create the GUI
    root = tk.Tk()
    root.title("Tic Tac Toe")
    p2 = HumanPlayer("human")
    gui = TicTacToeGUI(root, p1)

    # Start the main loop
    root.mainloop()