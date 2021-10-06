import time

def cross(A, B):
    # concat of chars in string A and chars in string B
    return [a+b for a in A for b in B]

digits = '123456789'
rows   = 'ABCDEFGHI'
cols   = digits
cells  = cross(rows, cols) # 81 cells A1..9, B1..9, C1..9, ...

# unit = a row, a column, a box; list of all units
unit_list = ([cross(r, cols) for r in rows] +                             # 9 rows
             [cross(rows, c) for c in cols] +                             # 9 cols
             [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]) # 9 units


units = dict((s, [u for u in unit_list if s in u]) for s in cells)
peers = dict((s, set(sum(units[s],[])) - {s}) for s in cells)


def display(grid):
    # grid is a dict of {cell: string}, e.g. grid['A1'] = '1234'
    print()
    for r in rows:
        for c in cols:
            v = grid[r+c]
            # avoid the '123456789'
            if v == '123456789':
                v = '.'
            print (''.join(v), end=' ')
            if c == '3' or c == '6': print('|', end='')
        print()
        if r == 'C' or r == 'F':
            print('-------------------')
    print()


def test():
    # a set of tests that must pass
    assert len(cells) == 81
    assert len(unit_list) == 27
    assert all(len(units[s]) == 3 for s in cells)
    assert all(len(peers[s]) == 20 for s in cells)


def parse_string_to_dict(grid_string):
    # grid_string is a string like '4.....8.5.3..........7......2.....6....   '
    # convert grid_string into a dict of {cell: chars}
    char_list1 = [c for c in grid_string if c in digits or c == '.']
    # char_list1 = ['8', '5', '.', '.', '.', '2', '4', ...  ]

    assert len(char_list1) == 81

    # replace '.' with '1234567'
    char_list2 = [s.replace('.', '123456789') for s in char_list1]

    # grid {'A1': '8', 'A2': '5', 'A3': '123456789',  }
    return dict(zip(cells, char_list2))


def no_conflict(grid, c, val):
    # check if assignment is possible: value v not a value of a peer
    for p in peers[c]:
        if grid[p] == val:
            return False # conflict
    return True


def solve(grid):
    # backtracking search a solution (DFS)
    if is_solved(grid):                     # if sudoku is solved
        display(grid)                       # print solution
        return True
    c = find_empty_cell(grid)               # Get a cell that is empty for example A1

    for v in grid[c]:                       # Iterate over all the values (1t/m9) in grid[c] --> a cell example A1 note : Could also be range()
        if no_conflict(grid, c, v):         # can only move on if the value is a valid acction
            new_grid = grid.copy()
            new_grid[c] = v
            if make_arc_consistent(new_grid, c, v):
                if solve(grid):             # recursive call
                    return True             # found a solution
    return False                            # didn't find a solution, go back up


def make_arc_consistent(grid, c, v):
    grid_changed = False

    for p in peers[c]:
        #print("{} : {}".format(p, grid[p]))
        if v in grid[p]:
            if len(grid[p]) <= 1:           # conflict, no solution on this 'path'
                return False
            else:
                grid[p] = grid[p].replace(v, '')
                grid_changed = True
    if grid_changed:
        for c2, v2 in other_cells_with_one_value(grid, c):      # try again, recursive call
            new_grid = grid.copy()                              # if a False is returned the there's a conflict
            if not make_arc_consistent(new_grid, c2, v2):
                return False
    return True


def find_empty_cell(grid):
    for k, v in grid.items():
        if len(v) > 1:
            return k


def other_cells_with_one_value(grid, c):
    other_cells = []
    for k, v in grid.items():
        if len(v) == 1 and c != k:
            other_cells.append((k, v))
    return other_cells


def is_solved(grid):
    # A function that checks if a cell is already filled
    for v in grid.values():
        if len(v) != 1:
            return False        # if a cell has more than one value, the problem is not solved
    return True                 # if all cells have only one value that means the sudoku is solved



# minimum nr of clues for a unique solution is 17
slist = [None for x in range(20)]
slist[0] = '.56.1.3....16....589...7..4.8.1.45..2.......1..42.5.9.1..4...899....16....3.6.41.'
slist[1] = '.6.2.58...1....7..9...7..4..73.4..5....5..2.8.5.6.3....9.73....1.......93......2.'
slist[2] = '.....9.73.2.....569..16.2.........3.....1.56..9....7...6.34....7.3.2....5..6...1.'
slist[3] = '..1.3....5.917....8....57....3.1.....8..6.59..2.9..8.........2......6...315.9...8'
slist[4] = '....6.8748.....6.3.....5.....3.4.2..5.2........72...35.....3..........69....96487'
slist[5] = '.94....5..5...7.6.........71.2.6.........2.19.6...84..98.......51..9..78......5..'
slist[6] = '.5...98..7...6..21..2...6..............4.598.461....5.54.....9.1....87...2..5....'
slist[7] = '...17.69..4....5.........14.....1.....3.5716..9.....353.54.9....6.3....8..4......'
slist[8] = '..6.4.5.......2.3.23.5..8765.3.........8.1.6.......7.1........5.6..3......76...8.'
slist[9] = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
slist[10]= '85...24..72......9..4.........1.7..23.5...9...4...........8..7..17..........36.4.'
slist[11]= '...5....2...3..85997...83..53...9...19.73...4...84...1.471..6...5...41...1...6247'
slist[12]= '.....6....59.....82....8....45........3........6..3.54...325..6..................'
slist[13]= '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
slist[14]= '8..........36......7..9.2...5...7.......457.....1...3...1....68..85...1..9....4..'
slist[15]= '6..3.2....5.....1..........7.26............543.........8.15........4.2........7..'
slist[16]= '.6.5.1.9.1...9..539....7....4.8...7.......5.8.817.5.3.....5.2............76..8...'
slist[17]= '..5...987.4..5...1..7......2...48....9.1.....6..2.....3..6..2.......9.7.......5..'
slist[18]= '3.6.7...........518.........1.4.5...7.....6.....2......2.....4.....8.3.....5.....'
slist[19]= '1.....3.8.7.4..............2.3.1...........958.........5.6...7.....8.2...4.......'


for i,sudo in enumerate(slist):
    print('*** Sudoku {0} Start State ***'.format(i))
    d = parse_string_to_dict(sudo)
    start_time = time.time()
    display(d)
    print('*** Sudoku {0} Oplossing ***'.format(i))
    solve(d)
    end_time = time.time()
    hours, rem = divmod(end_time-start_time, 3600)
    minutes, seconds = divmod(rem, 60)
    print("Time : {:0>2}:{:06.3f} (M/S/MS)".format(int(minutes),seconds))
    print()
