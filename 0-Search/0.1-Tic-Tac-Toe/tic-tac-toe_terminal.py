from time import sleep
from board import *
from minimax import *

MOVES = ((0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2))
KEY = {"X": 1, "O": -1}


def move_grid(moves):
    print("Move key:")
    print()
    for i in range(3):
        for j in range(3):
            if (i, j) in moves:
                print(f" {MOVES.index((i, j)) + 1} ", end="")
            else:
                print("   ", end="")
        print()
    print()


def moves_string(moves):
    return [str(MOVES.index(move) + 1) for move in moves]


def user_play(board: Board, user, game_round):
    # Lets the user play a move or quit.
    moves = board.moves()
    if len(moves) == 1:
        print(
            f"Your only move left is: {MOVES.index(moves[0]) + 1}. Let me play that for you..."
        )
        sleep(1)
        board.play_move(moves[0])
        return True
    move_grid(moves)
    move = ""
    while move not in moves_string(moves) and not move.lower().startswith("q"):
        if game_round == 1:
            move = input(
                f"Choose the cell in which you want to place your first {user}, or respond with 'q' to quit: "
            )
        else:
            move = input(
                f"Choose the cell in which you want to place your next {user}, or respond with 'q' to quit: "
            )

    if move.lower().startswith("q"):
        return False

    board.play_move(MOVES[int(move) - 1])
    return True


def game_over(board: Board, user, bot):
    if board.winner() == KEY[bot]:
        print()
        print("Final board:")
        board.print()
        print("Kneel before my superior intellect, loser...")
        print()
        return True
    elif board.winner() == 0:
        print()
        print("Final board:")
        board.print()
        print("Naturally, you cannot beat a master like myself...")
        print()
        return True

    return False


def tictactoe_terminal():
    board = Board()
    print()
    print(
        "Let's play a game of Tic-Tac-Toe! Choose your player (X or O). X goes first."
    )
    user = ""
    while True:
        print("Respond with one of X or O.")
        user = input().capitalize()
        if user == "X":
            bot = "O"
            print("Fine, I will be O. Let's begin.")
            sleep(1)
            break
        elif user == "O":
            bot = "X"
            print("Fine, I will be X. Let's begin.")
            sleep(1)
            break
    game_round = 1
    while True:
        if user == "X":
            print()
            print(f"Round {game_round}:")
            board.print()
            play_on = user_play(board, user, game_round)
            if game_over(board, user, bot) or not play_on:
                break
            board.play_move(optimal_move(board))
            if game_over(board, user, bot):
                break
            game_round = game_round + 1
        else:
            print()
            print(f"Round {game_round}:")
            board.play_move(optimal_move(board))
            board.print()
            if game_over(board, user, bot):
                break
            play_on = user_play(board, user, game_round)
            if game_over(board, user, bot) or not play_on:
                break
            game_round = game_round + 1


if __name__ == "__main__":
    tictactoe_terminal()
