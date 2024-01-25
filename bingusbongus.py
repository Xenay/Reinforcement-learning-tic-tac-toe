import numpy as np
import pickle
from tictactoeAlgo import TicTacToe

from tictactoefinalRein import Player

# Assuming both classes and necessary functions are imported or defined here...


class TicTacToeAIvsAI:
    def __init__(self):
        self.board = np.zeros((3, 3), dtype=int)
        self.p1 = Player("p1")
        print(self.p1)
        self.p2 = TicTacToe()
        print(self.p2)
        # AIPlayer is the class from the algorithm-based approach
        self.p1.loadPolicy(
            "policy_p1"
        )  # Load the policy for the reinforcement learning player
        self.isEnd = False

    def check_winner(self, board=None):
        if board is None:
            board = self.board

        # Check for a win for each player
        for player in [1, 2]:
            # Check rows and columns
            for i in range(3):
                if all(board[i, j] == player for j in range(3)) or all(
                    board[j, i] == player for j in range(3)
                ):
                    return player
            # Check diagonals
            if all(board[i, i] == player for i in range(3)) or all(
                board[i, 2 - i] == player for i in range(3)
            ):
                return player

        # Check for a draw (board is full and no winner)
        if np.all(board != 0):
            return 0

        # Continue the game if no winner or draw
        return None

    def play(self):
        turn = 0  # To track the number of turns
        while not self.isEnd:
            if turn % 2 == 0:
                # Player 1's turn (symbol 1)
                print("Player 1's turn")
                positions = self.availablePositions()
                p1_action = self.p1.chooseAction(positions, self.board, 1)
                print(p1_action)
                self.board[p1_action] = 1
            else:
                # Player 2's turn (symbol -1)
                print("Player 2's turn")
                p2_action = self.ai_move()
                print(p2_action)
                self.board[p2_action] = -1

            # Check for a winner or a draw
            winner = self.check_winner()
            if winner is not None:
                if winner == 1:
                    print("Game Over. Winner: Player 1")
                    break
                elif winner == 0:
                    print("Game Over. Winner: Player 2")
                    break
                else:
                    print("Game Over. It's a draw.")
                break

            turn += 1
            # If all turns are played and no winner, it's a draw
            if turn == 9 and winner is None:
                print("Game Over. It's a draw.")
                break

    def availablePositions(self):
        print("available positions called")
        positions = []
        for i in range(3):
            for j in range(3):
                if self.board[i, j] == 0:
                    positions.append((i, j))
        return positions

    def ai_move(self):
        best_move = self.minimax(self.board, 1)
        return [best_move[0], best_move[1]]

    def minimax(self, board, player):
        empty_cells = np.argwhere(board == 0)
        if self.check_winnerSelf(board) == 1:
            return -1, -1, 1
        elif self.check_winnerSelf(board) == 2:
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
                    f"Move {move[0]}, {move[1]}: Probability of winning = {move_percentage}%"
                )
        else:
            best_move = min(moves, key=lambda x: x[2])

        return best_move

    def check_winnerSelf(self, board=None):
        if board is None:
            board = self.board

        for i in range(3):
            if all(board[i, j] == 2 for j in range(3)) or all(
                board[j, i] == 2 for j in range(3)
            ):
                return 2

        if all(board[i, i] == 2 for i in range(3)) or all(
            board[i, 2 - i] == 2 for i in range(3)
        ):
            return 2

        for i in range(3):
            if all(board[i, j] == 1 for j in range(3)) or all(
                board[j, i] == 1 for j in range(3)
            ):
                return 1

        if all(board[i, i] == 1 for i in range(3)) or all(
            board[i, 2 - i] == 1 for i in range(3)
        ):
            return 1

        if np.all(board != 0):
            return 0

        return -1


# Main execution
if __name__ == "__main__":
    game = TicTacToeAIvsAI()
    game.play()
