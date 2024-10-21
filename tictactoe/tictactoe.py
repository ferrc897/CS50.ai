"""
Tic Tac Toe Player
"""
import copy
import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    count = 0
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] is not None:
                count += 1
    if count % 2 == 0:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] is EMPTY:
                actions.add((i,j))
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    board = copy.deepcopy(board)
    row, column, = action
    if action not in actions(board):
        raise Exception("Invalid Move")

    result = board
    result[row][column] = player(board)

    return result
    


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(len(board)):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] is not EMPTY:
            return board[i][0]
    for j in range(len(board)):
        if board[0][j] == board[1][j] == board[2][j] and board[0][j] is not EMPTY:
            return board[i][j]
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not EMPTY:
        return board[0][2]

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    count = 0
    if winner(board) is not None:
        return True
    if len(actions(board)) == 0:
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    result = winner(board)

    if result == X:
        return 1
    elif result == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    ivalue = -math.inf
    if player(board) == X:
        for action in actions(board):
            value = min_value(result(board,action))
            if value > ivalue:
                ivalue = value
                act = action
        return act
            


    if player(board) == O:
        ivalue = math.inf
        for action in actions(board):
            value = max_value(result(board, action))
            if value < ivalue:
                ivalue = value
                act = action
        return act


def min_value(s):
    if terminal(s):
        return utility(s)
    v = math.inf
    for action in actions(s):
        v = min(v, max_value(result(s, action)))
    return v


def max_value(s):
    if terminal(s):
        return utility(s)
    v = -math.inf
    for action in actions(s):
        v = max(v, min_value(result(s, action)))
    return v

