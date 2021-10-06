import numpy as np

# place triominoes in matrix 3 rows x 4 cols

NR_OF_COLS = 16  # 4 triominoes HB VB L RL + 12 cells
NR_OF_ROWS = 22  # 6*HB 4*VB 6*L 6*RL
temp_list = []

triominoes = [np.array(piece) for piece in [
    # horizontal bar (HB)
    [[1, 1, 1]],
    # vertical bar (VB)
    [[1], [1], [1]],
    # normal L (L)
    [[1, 0], [1, 1]],
    # rotated L (RL)
    [[1, 1], [0, 1]]
]
              ]


def make_matrix(triominoes):
    # create and return matrix as input for alg-x
    # matrix has 22 rows x 16 cols
    # and has the following cols: HB VB L RL (0,0) (0,1) (0,2) (0,3) (1,0) .... (3,3)

    def all_positions(triominoes):
        # find all positions to place triomino T in matrix M (3 rows x 4 cols)
        rows, cols = triominoes.shape
        for i in range(3 + 1 - rows):
            for j in range(4 + 1 - cols):
                M = np.zeros((3, 4), dtype='int')
                # place T in M
                M[i:i + rows, j:j + cols] = triominoes
                yield M

    rows = []
    for i, P in enumerate(triominoes):
        # i points to the 4 triominoes HB VB L RL
        for A in all_positions(P):
            # add 4 zeros to each row
            A = np.append(np.zeros(4, dtype='int'), A)
            A[i] = 1
            rows.append(list(A))
    return rows


def prepare(mx):
    # note that when applying alg-x we're only interested in 1's
    # so we add 2 lists that define where the 1's are
    rows = mx
    # note that zip(*b) is the transpose of b
    cols = [list(i) for i in zip(*rows)]

    def find_ones(rows):
        # returns indexes in rows where the ondes are
        # example: [[0, 3], [1, 3], [1, 2], [2]]
        lv_row_has_1_at = []
        for row in rows:
            x = []
            for i in range(len(row)):
                if row[i] == 1:
                    x.append(i)
            lv_row_has_1_at.append(x.copy())
        return lv_row_has_1_at

    row_has_1_at = find_ones(rows)  # read-only list; example: [[0, 3], [1, 3], [1, 2], [2]]
    col_has_1_at = find_ones(cols)  # read-only list; example: [[0], [1, 2], [2, 3], [0, 1]]

    # if there's a col without ones, then there is no exact cover possible
    for col in col_has_1_at:
        if not col:
            print("No solution possible!")

    row_valid = NR_OF_ROWS * [1]
    col_valid = NR_OF_COLS * [1]

    return row_valid, col_valid, row_has_1_at, col_has_1_at


def cover(r, row_valid, col_valid, row_has_1_at, col_has_1_at):
    # given a row r:
    #   cover all cols that have a 1 in row r
    #   cover all rows r' that intersect/overlap with row r
    # returns row_valid, col_valid
    for x in range(len(col_has_1_at)):
        for y in col_has_1_at[x]:
            if y != r and r in col_has_1_at[x]:
                row_valid[y] = 0
        if r in col_has_1_at[x]:
            col_valid[x] = 0

    row_valid[r] = 1
    return row_valid, col_valid


def make_solution_list(solution, row_has_1_at):
    valid_solutions = []
    # place triominoes in matrix D 3 rows x 4 cols
    D = [["  " for i in range(4)] for j in range(3)]

    for row_number in solution:
        # print(row_number) # 1 6 14 21
        row_list = row_has_1_at[row_number]
        # print(row_list)   # 0 5 6 7
        idx = row_list[0]
        assert idx in [0, 1, 2, 3]
        symbol = ['HB', 'VB', 'L ', 'RL'][idx]
        for c in row_list[1:]:  # skip first one
            D[c // 4 - 1][c % 4] = symbol   # put row number and collum number in D
            print(D)

    printBord = 1
    for i in D:
        if '  ' in i:
            printBord = 0
    if printBord:
        if D not in temp_list:
            temp_list.append(D)


def solve(r, t_row_valid, t_col_valid, row_position_of_1, col_position_of_1):
    possible = [r]
    row_valid_cover, col_valid_cover = cover(r, t_row_valid, t_col_valid, row_position_of_1, col_position_of_1)
    row = 0
    while row != -1:
        row = -1
        for x in range(len(row_valid_cover)):
            if row_valid_cover[x] == 1 and not x in possible:
                row = x
        if row != -1:
            row_valid_cover, col_valid_cover = cover(row, row_valid_cover, col_valid, row_position_of_1, col_position_of_1)
            possible.append(row)
    return possible, row_position_of_1


mx = make_matrix(triominoes)
for x in range(NR_OF_ROWS):
    row_valid, col_valid, row_has_1_at, col_has_1_at = prepare(mx)
    solution, row_has_1_at = solve(x, row_valid, col_valid, row_has_1_at, col_has_1_at)
    make_solution_list(solution, row_has_1_at)

for i in temp_list:
    print('------------------------')
    for k in i:
        print(k)
