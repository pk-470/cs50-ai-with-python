from board import *
import random as rd


def optimal_move(board: Board):
    moves, move_evals, target = minimax_alpha_beta(board)
    optimal_moves = [move for move in moves if move_evals[move] == target]
    return rd.choice(optimal_moves)


def minimax_alpha_beta(board: Board):
    # Returns an evaluation of each possible move given the state of the board,
    # as well as the min/max evaluation depending on whose player turn it is.
    moves = board.moves()
    a = -inf
    b = inf
    if len(moves) == 9:
        return moves, {move: 0 for move in moves}, 0
    if board.player_turn == X:
        values = [min_value(board, move, a, b) for move in moves]
        return moves, {moves[i]: values[i] for i in range(len(moves))}, max(values)
    else:
        values = [max_value(board, move, a, b) for move in moves]
        return moves, {moves[i]: values[i] for i in range(len(moves))}, min(values)


def max_value(board: Board, move, a, b):
    new_board = board.apply_move(move)
    check = new_board.winner()
    v = -inf
    if check is not None:
        return check
    for move in new_board.moves():
        v = max(v, min_value(new_board, move, a, b))
        if v >= b:
            break
        a = max(a, v)

    return v


def min_value(board: Board, move, a, b):
    new_board = board.apply_move(move)
    check = new_board.winner()
    v = inf
    if check is not None:
        return check
    for move in new_board.moves():
        v = min(v, max_value(new_board, move, a, b))
        if v <= a:
            break
        b = min(b, v)

    return v
