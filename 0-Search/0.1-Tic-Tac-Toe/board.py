from math import inf
import numpy as np

X = 1
O = -1
START = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])


class Board:
    def __init__(self, state=START):
        self.state = state
        self.player_turn = (-1) ** np.sum(self.state)

    def print(self):
        print()
        for i in range(3):
            for j in range(3):
                if self.state[i, j] == X:
                    print(" X ", end="")
                elif self.state[i, j] == O:
                    print(" O ", end="")
                else:
                    print("   ", end="")
                if j < 2:
                    print("┃", end="")
            print()
            if i < 2:
                print("━━━┼━━━┼━━━")
        print()

    def play_move(self, cell):
        i, j = cell
        self.state[i, j] = self.player_turn
        self.player_turn = -self.player_turn

    def apply_move(self, cell):
        i, j = cell
        new_state = self.state.copy()
        new_state[i, j] = self.player_turn
        return Board(state=new_state)

    def moves(self):
        return [(i, j) for i in range(3) for j in range(3) if self.state[i, j] == 0]

    def winner(self):
        rows, cols, diag1, diag2 = (
            np.sum(self.state, 1),
            np.sum(self.state, 0),
            np.trace(self.state),
            np.trace(np.fliplr(self.state)),
        )
        if any(rows == 3) or any(cols == 3) or diag1 == 3 or diag2 == 3:
            return X
        elif any(rows == -3) or any(cols == -3) or diag1 == -3 or diag2 == -3:
            return O
        elif not self.moves():
            return 0
        else:
            return None
