"""
Othello is a turn-based two-player strategy board game.
-----------------------------------------------------------------------------
Board representation
We represent the board as a flat-list of 100 elements, which includes each square on
the board as well as the outside edge. Each consecutive sublist of ten
elements represents a single row, and each list element stores a piece. 
An initial board contains four pieces in the center:
    ? ? ? ? ? ? ? ? ? ?
    ? . . . . . . . . ?
    ? . . . . . . . . ?
    ? . . . . . . . . ?
    ? . . . o @ . . . ?
    ? . . . @ o . . . ?
    ? . . . . . . . . ?
    ? . . . . . . . . ?
    ? . . . . . . . . ?
    ? ? ? ? ? ? ? ? ? ?
The outside edge is marked ?, empty squares are ., black is @, and white is o.
This representation has two useful properties:
1. Square (m,n) can be accessed as `board[mn]`, and m,n means m*10 + n. This avoids conversion
   between square locations and list indexes.
2. Operations involving bounds checking are slightly simpler.
"""
import random
import copy

max_depth = 6

value = 0

pos_value = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 50, -30, 10, 5, 5, 10, -30, 50, 0,
             0, -30, -40, -5, -5, -5, -5, -40, -30, 0,
             0, 10, -5, 20, 0, 0, 20, -5, 10, 0,
             0, 5, -5, 0, 10, 10, 0, -5, 5, 0,
             0, 5, -5, 0, 10, 10, 0, -5, 5, 0,
             0, 10, -5, 20, 0, 0, 20, -5, 10, 0,
             0, -30, -40, -5, -5, -5, -5, -40, -30, 0,
             0, 50, -30, 10, 5, 5, 10, -30, 50, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# The black and white pieces represent the two players.
EMPTY, BLACK, WHITE, OUTER = '.', '@', 'o', '?'
PIECES = (EMPTY, BLACK, WHITE, OUTER)
PLAYERS = {BLACK: 'Black', WHITE: 'White'}

# To refer to neighbor squares we can add a direction to a square.
UP, DOWN, LEFT, RIGHT = -10, 10, -1, 1
UP_RIGHT, DOWN_RIGHT, DOWN_LEFT, UP_LEFT = -9, 11, 9, -11
# in total 8 directions.
DIRECTIONS = (UP, UP_RIGHT, RIGHT, DOWN_RIGHT, DOWN, DOWN_LEFT, LEFT, UP_LEFT)


def squares():
    # list all the valid squares on the board.
    # returns a list of valid integers [11, 12, ...]; e.g. 19,20,21 are invalid
    # 11 means first row, first col, because the board size is 10x10
    return [i for i in range(11, 89) if 1 <= (i % 10) <= 8]


def initial_board():
    # create a new board with the initial black and white positions filled
    # returns a list ['?', '?', '?', ..., '?', '?', '?', '.', '.', '.', ...]
    board = [OUTER] * 100
    for i in squares():
        board[i] = EMPTY
    # the middle four squares should hold the initial piece positions.
    board[44], board[45] = WHITE, BLACK
    board[54], board[55] = BLACK, WHITE
    return board


def print_board(board):
    # get a string representation of the board
    # heading '  1 2 3 4 5 6 7 8\n'
    rep = ''
    rep += '  %s\n' % ' '.join(map(str, range(1, 9)))
    # begin,end = 11,19 21,29 31,39 ..
    for row in range(1, 9):
        begin, end = 10 * row + 1, 10 * row + 9
        rep += '%d %s\n' % (row, ' '.join(board[begin:end]))
    print(rep)


# -----------------------------------------------------------------------------
# Playing the game

# We need functions to get moves from players, check to make sure that the moves
# are legal, apply the moves to the board, and detect when the game is over.

# Checking moves. A move must be both valid and legal: it must refer to a real square,
# and it must form a bracket with another piece of the same color with pieces of the
# opposite color in between.

def is_valid(move):
    # is move a square on the board?
    # move must be an int, and must refer to a real square
    return isinstance(move, int) and move in squares()


def opponent(player):
    # get player's opponent piece
    return BLACK if player is WHITE else WHITE


def find_bracket(square, player, board, direction):
    # find and return the square that forms a bracket with square for player in the given
    # direction; returns None if no such square exists
    bracket = square + direction
    if board[bracket] == player:
        return None
    opp = opponent(player)
    while board[bracket] == opp:
        bracket += direction
    # if last square board[bracket] not in (EMPTY, OUTER, opp) then it is player
    return None if board[bracket] in (OUTER, EMPTY) else bracket


def is_legal(move, player, board):
    # is this a legal move for the player?
    # move must be an empty square and there has to be a bracket in some direction
    # note: any(iterable) will return True if any element of the iterable is true
    hasbracket = lambda direction: find_bracket(move, player, board, direction)
    return board[move] == EMPTY and any(hasbracket(x) for x in DIRECTIONS)


def make_move(move, player, board):
    # when the player makes a valid move, we need to update the board and flip all the
    # bracketed pieces.
    board[move] = player
    # look for a bracket in any direction
    for d in DIRECTIONS:
        make_flips(move, player, board, d)
    return board


def make_flips(move, player, board, direction):
    # flip pieces in the given direction as a result of the move by player
    bracket = find_bracket(move, player, board, direction)
    if not bracket:
        return
    # found a bracket in this direction
    square = move + direction
    while square != bracket:
        board[square] = player
        square += direction


# Monitoring players

# define an exception
class IllegalMoveError(Exception):
    def __init__(self, player, move, board):
        self.player = player
        self.move = move
        self.board = board

    def __str__(self):
        return '%s cannot move to square %d' % (PLAYERS[self.player], self.move)


def legal_moves(player, board):
    # get a list of all legal moves for player
    # legal means: move must be an empty square and there has to be is an occupied line in some direction
    return [sq for sq in squares() if is_legal(sq, player, board)]


def any_legal_move(player, board):
    # can player make any moves?
    return any(is_legal(sq, player, board) for sq in squares())


# Putting it all together. Each round consists of:
# - Get a move from the current player.
# - Apply it to the board.
# - Switch players. If the game is over, get the final score.

def random_legal_move(player, board):
    if any_legal_move(player, board):
        return random.choice(legal_moves(player, board))
    else:
        return None


def play(black_strategy, white_strategy):
    # play a game of Othello and return the final board and score
    b = initial_board()
    current = BLACK
    print_board(b)
    # move = dfs_pruning(b, max_depth, float('-inf'), float('inf'), BLACK, BLACK)
    # b = make_move(move, BLACK, b)
    # print_board(b)

    while any_legal_move(current, b):
        if current is BLACK:
            b = make_move(black_strategy(b, max_depth, float('-inf'), float('inf'), current, current), current, copy.deepcopy(b))
            # b = make_move(black_strategy(current, copy.deepcopy(b)), current, copy.deepcopy(b)) #random
        if current is WHITE:
            b = make_move(white_strategy(b, max_depth, float('-inf'), float('inf'), current, current), current, copy.deepcopy(b)) # pruning
            # b = make_move(white_strategy(current, copy.deepcopy(b)), current, copy.deepcopy(b)) #random
        print_board(b)
        if not any_legal_move(current, b):
            print(current, " doesn't have any moves left!")
            break
        # print("Score for player " + str(PLAYERS.get(current)) + " :" + str(minimax(b, max_depth, current)))
        current = next_player(b, current)


    print("game has ended!")
    s = score(b)
    print("score:")
    print("Black: " + str(s[0]))
    print("White: " + str(s[1]))

    if s[0] > s[1]:
        print("Black has won!")
    elif s[0] < s[1]:
        print("White has won!")
    elif s[0] is s[1]:
        print("it's a tie")


def next_player(board, prev_player):
    # which player should move next?  Returns None if no legal moves exist
    if prev_player is None:
        return BLACK
    else:
        if prev_player is WHITE:
            if any_legal_move(WHITE, board) is not None:
                return BLACK
            else:
                return None
        elif prev_player is BLACK:
            if any_legal_move(BLACK, board) is not None:
                return WHITE
            else:
                return None


#
# def get_move(strategy, player, board):
#     # call strategy(player, board) to get a move'
#     pass

def score(board):
    # compute player's score (number of player's pieces minus opponent's)

    black = board.count(BLACK)
    white = board.count(WHITE)
    return black, white


# def minimax(node, depth, player):
#     global value
#     if max_depth == depth:
#         value = getHeuristic(node, player)
#     if depth == 0 or next_player(node, player) is None:
#         return getHeuristic(node, player)
#     if player == BLACK:
#         for child in getChildren(node, player):
#             value = max(value, minimax(child, depth - 1, WHITE))
#         return value
#     else:
#         for child in getChildren(node, player):
#             value = min(value, minimax(child, depth - 1, BLACK))


def dfs_pruning(board, depth, alpha, beta, max_player, player):
    if depth == 0 or max_player is None or not any_legal_move(max_player, copy.deepcopy(board)):
        return get_heuristic(copy.deepcopy(board), player)

    if max_player == player:
        max_eval = float('-inf')
        for i in legal_moves(max_player, board):
            eval = dfs_pruning(make_move(i, max_player, copy.deepcopy(board)), depth - 1, alpha, beta,
                               next_player(copy.deepcopy(board), max_player), player)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
            print("depth: ", depth, "alpha: ", alpha, "beta: ", beta, "eval: ", eval, "max_eval: ", max_eval)
            if depth == max_depth:
                return i
        return max_eval

    else:
        min_eval = float('inf')
        for i in legal_moves(max_player, board):
            eval = dfs_pruning(make_move(i, max_player, copy.deepcopy(board)), depth - 1, alpha, beta,
                               next_player(copy.deepcopy(board), max_player), player)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
            print("depth: ", depth, "alpha: ", alpha, "beta: ", beta, "eval: ", eval, "max_eval: ", min_eval)
            if depth == max_depth:
                return i
        return min_eval


def get_heuristic(node, player):
    scoreBlack = 0
    scoreWhite = 0

    i = range(11, 89)

    for x in i:
        if 1 <= (x % 10) <= 8:
            # print(pos_value[x])
            if node[x] == '@':
                scoreBlack = scoreBlack + pos_value[x]
            if node[x] == 'o':
                scoreWhite = scoreWhite + pos_value[x]
    if player is WHITE:
        return scoreWhite
    if player is BLACK:
        return scoreBlack
    else:
        return '777'


def getChildren(node, player):
    children = []
    i = 0
    for move in legal_moves(player, node):
        print("legal move:")
        print(move)
        tb = make_move(move, player, copy.deepcopy(node))
        children.append(tb)

    for child in children:
        i = i + 1
        print('kind' + str(i))
        print(print_board(child))
        print(get_heuristic(child, player))
    return children


# Play strategies
play(dfs_pruning, dfs_pruning)
