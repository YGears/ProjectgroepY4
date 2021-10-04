'''Constraints:
    1 every Ace borders a King
    2 every King borders a Queen
    3 every Queen borders a Jack
    4 no Ace borders a Queen
    5 no two of the same cards border each other

'''
# the board has 8 cells, let’s represent the board with a dict key=cell, value=card
import copy
import itertools

dfs_solutions = []
start_board = {cell: '.' for cell in range(8)}
cards = ['K', 'K', 'Q', 'Q', 'J', 'J', 'A', 'A']
neighbors = {0: [3], 1: [2], 2: [1, 4, 3], 3: [0, 2, 5], 4: [2, 5], 5: [3, 4, 6, 7], 6: [5], 7: [5]}


def is_valid(board):
    card_positions = []
    if sum(map("K".__eq__, board.values())) > 2 \
            or sum(map("Q".__eq__, board.values())) > 2 \
            or sum(map("J".__eq__, board.values())) > 2 \
            or sum(map("A".__eq__, board.values())) > 2:
        return False
    for pos in board:
        if board[pos] != '.':
            card_positions.append(pos)
        else:
            continue
        if not card_positions:
            return False
        for card_pos in card_positions:
            pos_neighbor = []
            for i in neighbors[card_pos]:
                pos_neighbor.append(board[i])
            if list(set(pos_neighbor)) is ['.']:
                print(pos_neighbor)
                return True
            if board[card_pos] in pos_neighbor:
                return False
            if '.' in pos_neighbor:
                continue
            elif board[card_pos] == 'A' and 'K' not in pos_neighbor \
                    or board[card_pos] == 'K' and 'Q' not in pos_neighbor \
                    or board[card_pos] == 'Q' and 'J' not in pos_neighbor \
                    or board[card_pos] == 'A' and 'Q' in pos_neighbor:
                return False
    return True


def bruteforce():
    solutions = []
    for (a, b, c, d, e, f, g, h) in list(itertools.permutations(cards)):
        brute_board = {0: a, 1: b, 2: c, 3: d, 4: e, 5: f, 6: g, 7: h}
        if is_valid(brute_board):
            solutions.append(str(brute_board))
    s = set(solutions)
    for i in s:
        print(i)
    print('brute force found ', len(s), " solutions")


def dfs(board, depth):
    if is_valid(board):
        if sum(map(".".__eq__, board.values())) == 0:
            dfs_solutions.append(board)
            return True
        for card in ['K', 'Q', 'J', 'A']:
            board[depth] = card
            dfs(copy.deepcopy(board), depth+1)
    return False


def test():
    # is_valid(board) checks all cards, returns False if any card is invalid
    print('f ', is_valid({0: 'J', 1: 'K', 2: 'Q', 3: 'Q', 4: 'J', 5: 'K', 6: 'A', 7: 'A'}))
    print('f ', is_valid({0: 'J', 1: 'J', 2: 'Q', 3: 'Q', 4: 'K', 5: 'K', 6: 'A', 7: 'A'}))
    print('t ', is_valid({0: '.', 1: '.', 2: '.', 3: '.', 4: '.', 5: '.', 6: '.', 7: '.'}))
    print('t ', is_valid({0: 'J', 1: '.', 2: '.', 3: '.', 4: '.', 5: '.', 6: '.', 7: '.'}))
    print('f ', is_valid({0: '.', 1: '.', 2: '.', 3: 'J', 4: 'J', 5: 'A', 6: 'J', 7: 'J'}))  # [1]
    print('f ', is_valid({0: 'J', 1: '.', 2: '.', 3: '.', 4: 'J', 5: 'K', 6: 'J', 7: 'Q'}))  # [3]
    print('t ', is_valid({0: '.', 1: 'Q', 2: '.', 3: '.', 4: 'Q', 5: 'J', 6: '.', 7: '.'}))  # [3]
    print('f ', is_valid({0: 'Q', 1: '.', 2: '.', 3: 'K', 4: '.', 5: '.', 6: '.', 7: '.'}))  # [3]
    print('f ', is_valid({0: '.', 1: 'A', 2: 'Q', 3: '.', 4: '.', 5: 'Q', 6: '.', 7: '.'}))  # [4]
    print('f ', is_valid({0: '.', 1: '.', 2: '.', 3: '.', 4: 'J', 5: 'J', 6: '.', 7: '.'}))  # [5]
    print('f ', is_valid({0: '.', 1: '.', 2: '.', 3: '.', 4: '.', 5: 'Q', 6: '.', 7: 'Q'}))  # [5]
    print('t ', is_valid({0: 'Q', 1: 'Q', 2: '.', 3: '.', 4: '.', 5: '.', 6: '.', 7: '.'}))


print(' --- tests --- ')
test()
print('\n')
print(' --- Brute force --- ')
bruteforce()
print('\n')
print(' --- dfs & backtracking --- ')
dfs(start_board, 0)
for i in dfs_solutions:
    print(i)
print('dfs with backtracking found ', len(dfs_solutions), " solutions")

