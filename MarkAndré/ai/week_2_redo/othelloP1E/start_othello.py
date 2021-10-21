import heapq
import copy
import math as math
from bord import bord

"""

D: the max depth for a 2 sec response is 4
F: Door de pruning is de max diepte nu 5, 
verder kunnen we de efficientie vergroten door door de bord states te hashen en die in een hashmap te doen met de
 gevonden value, zodat wanneer er een branch (in dezelfde base recursion)op die map state komt, dan kan hij gewoon die 
 value pakken in plaats van dat elke branch de value weer herberekent

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

# The black and white pieces represent the two players.
EMPTY, BLACK, WHITE, OUTER = '.', '@', 'o', '?'
PIECES = (EMPTY, BLACK, WHITE, OUTER)
PLAYERS = {BLACK: 'Black', WHITE: 'White'}
players = [WHITE, BLACK]

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
        begin, end = 10*row + 1, 10*row + 9
        rep += '%d %s\n' % (row, ' '.join(board[begin:end]))
    return rep

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
#
# def play(black_strategy, white_strategy):
#     print(black_strategy)
#     print(white_strategy)
#     # play a game of Othello and return the final board and score

def next_player(board, prev_player):
    if legal_moves(not prev_player, board): return not prev_player
    elif legal_moves(prev_player, board): return prev_player
    # which player should move next?  Returns None if no legal moves exist

def minmax(player, board, depth, parentScore):
    if depth == maxDepth or player == None: # if max depth is reached or if there are no more moves to play
        return score(maxingPlayer, board)# return the score of the current board

    depth += 1 # increment depth
    if players[player] == maxingPlayer: # if the alg should be max-ing
        maxScore = -math.inf
        for move in legal_moves(players[player], board): # for every move
            childsBoard = copy.deepcopy(board) # create a copy of the board
            childsBoard = make_move(move, players[player], childsBoard) # play the move
            childsScore = score(maxingPlayer, childsBoard) # determine the score of the board after the move
            if childsScore >= parentScore: # if the score of the child is higher or the same
                child = minmax(next_player(childsBoard, player), copy.deepcopy(childsBoard), depth, childsScore) # resurse
                if child >= maxScore: # if move is higher or equals to the current best move
                    maxScore = child # replace the score with the score of the current child
        return maxScore # return the max score found
    else: # or min-ing: everything is the same as in 184 - 193 but this time it returns the lowest score
        minScore = math.inf
        for move in legal_moves(players[player], board):
            childsBoard = copy.deepcopy(board)
            childsBoard = make_move(move, players[player], childsBoard)
            childsScore = score(maxingPlayer, childsBoard)
            if childsScore >= parentScore:
                child = minmax(next_player(childsBoard, player), copy.deepcopy(childsBoard), depth, childsScore)
                if child <= minScore:
                    minScore = child
        return minScore

heuristics = [
    [10000, -50, 50, 50, 50, 50, -50, 10000],
    [-50, -50, -10, -10, -10, -10, -50, -50],
    [50, -10, 1, 1, 1, 1, -10, 50],
    [50, -10, 1, 1, 1, 1, -10, 50],
    [50, -10, 1, 1, 1, 1, -10, 50],
    [50, -10, 1, 1, 1, 1, -10, 50],
    [-50, -50, -10, -10, -10, -10, -50, -50],
    [10000, -50, 50, 50, 50, 50, -50, 10000]
]
def score(player, board):
    scoreBlack = 0
    scoreWhite = 0
    step = 0
    for node in board:
        if node == "@":
            y = step % 10
            x = math.floor(step / 10)
            scoreBlack += heuristics[x-1][y-1]
        elif node == "o":
            y = step % 10
            x = math.floor(step / 10)
            scoreWhite += heuristics[x-1][y-1]
        step += 1

    if player == "o":
        sc = [scoreWhite, scoreBlack]
    elif player == "@" :
        sc = [scoreBlack, scoreWhite]
    else:
        a = 100 / 0
    res = (sc[0] - sc[1])
    return res

# the  function start the minimax algorithm.
# returns the first possible move for the player that is not minmaxing
# determines the best move for minmaxing player
# uses pruning to reduce branch amount
def get_move(player, board, depth, parentScore):
    if players[player] != maxingPlayer: #if not maxingplayer
        return legal_moves(players[player], board)[0] # return first viable  move
    else:
        maxChildScore = -math.inf
        maxMove = 0
        for move in legal_moves(players[player], board):
            childsBoard = copy.deepcopy(board) # make copy of the board
            childsBoard = make_move(move, players[player], childsBoard) # play the move
            childsScore = score(maxingPlayer, childsBoard) # get the score of the board

            if childsScore >= parentScore or maxChildScore == -math.inf: # if the score of the child is higher or the same as the parent
                child = minmax(next_player(childsBoard, player), copy.deepcopy(childsBoard), depth, childsScore) # activate minmax
                if child >= maxChildScore or maxChildScore == -math.inf: # if the child got a score higher than the recorded max score, put this child as the max child
                    maxChildScore = child
                    maxMove = move
        return maxMove

def printStatus(move, blacksTurn, mainBoard):
    print("")
    print(str(move) + " - " + maxingPlayer + " - " + str(score(players[blacksTurn], mainBoard)))
    print(print_board(mainBoard))

mainBoard = initial_board()
maxingPlayer = WHITE
blacksTurn = False
maxDepth = 4

#
while any_legal_move("", mainBoard):# so long as someone can play a move

    legalMoves = legal_moves(players[blacksTurn], mainBoard) # get all legal moves for the current player
    if legalMoves: # if there are any
        if len(legalMoves) == 1: # if only 1 move is left
            make_move(legalMoves[0], players[blacksTurn], mainBoard)
        else:
            parentScore = score(maxingPlayer, mainBoard) # get the score of the current board
            move = get_move(blacksTurn, mainBoard, 0, parentScore) # get next move for the current player
            mainBoard = make_move(move, players[blacksTurn], mainBoard) # play the recieved move

            printStatus(move, blacksTurn, mainBoard)# print move + maxingPlayer + score of board + board

    blacksTurn = next_player(mainBoard, blacksTurn) # get next player

print("----------****----------")
print(print_board(mainBoard))
blackPoints = str(sum([x == "@" for x in mainBoard]))
whitePoints = str(sum([x == "o" for x in mainBoard]))
print("@ has : " + blackPoints + " pieces , " + str(score("@", mainBoard)) + " points")
print("o has : " + whitePoints + " pieces , " + str(score("o", mainBoard)) + " points")
sc = score(maxingPlayer, mainBoard)
if sc == 0:
    print("Draw")

elif blackPoints > whitePoints:
    print("@ wins")

else:
    print("o wins")

# heapq.heappush(boards, (priority, b))
# Play strategies

