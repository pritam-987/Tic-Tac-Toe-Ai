"""
The Ai
"""

from copy import deepcopy

X = "X"
O = "O"


def initial_state():
    """
    Return the initial_state of the board
    """
    return [
        [None, None, None],
        [None, None, None],
        [None, None, None],
    ]


def player(board):
    """
    check who plays next
    """
    x = sum(row.count("X") for row in board)
    o = sum(row.count("O") for row in board)

    if x > o:
        return O
    if x == o:
        return X


def actions(board):
    actions = set()
    for row in range(3):
        for col in range(3):
            if board[row][col] is None:
                actions.add((row, col))

    return actions


def result(board, action):
    """
    Return the board with the result from the move(i, j)
    """
    new_board = deepcopy(board)
    if (
        action[0] >= 0
        and action[0] < len(new_board)
        and action[1] >= 0
        and action[1] < len(new_board)
    ):
        new_board[action[0]][action[1]] = player(board)

    else:
        raise ValueError("Invalid action")

    return new_board


def winner(board):
    """
    Return the winner if the game is not tie
    """
    lines = []

    # rows
    lines.extend(board)

    # col
    for c in range(3):
        lines.append([board[r][c] for r in range(3)])

    # diagonals
    lines.append([board[i][i] for i in range(3)])
    lines.append([board[i][2 - i] for i in range(3)])

    for line in lines:
        if line == [X, X, X]:
            return X
        if line == [O, O, O]:
            return O
    return None


def terminal(board):
    """
    if game over -> True, otherwise False
    """

    if winner(board) is not None:
        return True

    for row in board:
        if None in row:
            return False

    return True


def utility(board):
    """
    return 1 if X won the game, -1 if O won, 0 for a draw
    """
    if winner(board) == X:
        return 1
    if winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    return the most optimal move for the player
    """
    if terminal(board):
        return None

    if player(board) == X:
        best_value = float("-inf")
        best_action = None

        for action in actions(board):
            v = min_value(result(board, action))

            if v > best_value:
                best_value = v
                best_action = action

        return best_action
    else:
        best_value = float("inf")
        best_action = None

        for action in actions(board):
            v = max_value(result(board, action))

            if v < best_value:
                best_value = v
                best_action = action

        return best_action


def max_value(board):
    """
    return the max value for the minmax fuction
    """
    v = float("-inf")
    if terminal(board):
        return utility(board)
    for action in actions(board):
        v = max(v, min_value(result(board, action)))

    return v


def min_value(board):
    """
    return the min value for the minmax fuction
    """
    v = float("inf")
    if terminal(board):
        return utility(board)
    for action in actions(board):
        v = min(v, max_value(result(board, action)))

    return v
