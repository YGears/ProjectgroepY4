def solve(grid, h, w):
    results = []
    d = []
    with open('words_NL.txt') as f:
        for line in f:
            d.append(line.upper()[:-1])
    for y in range(int(h)):
        for x in range(int(w)):
            print('checking position')
            results += find_words(grid, d, grid[y][x], y, x, set((y, x)))
    return set(results)


def find_words(grid, words, current, y, x, used):
    neighbors = [(-1, 0), (0, -1), (0, 1), (1, 0)]
    found = []
    if current in words:
        found.append(current)
    for dy, dx in neighbors:
        if y == 0 and dy == -1 or y == len(grid) - 1 and dy == 1:
            ny, nx = keep_in_grid_y(grid, y, x, dy, dx)
        elif x == 0 and dx == -1 or x == len(grid[y]) - 1 and dx == 1:
            ny, nx = keep_in_grid_x(grid, y, x, dy, dx)
        else:
            ny, nx = y + dy, x + dx
        if (ny, nx) not in used:
            used.add((ny, nx))
            found.extend(find_words(grid, words, current + grid[ny][nx], ny, nx, used))
            used.remove((ny, nx))
    return list(set(found))


def keep_in_grid_y(grid, y, x, dy, dx):
    if y + dy > len(grid) - 1:
        ny = 0
    else:
        ny = len(grid) - 1
    return ny, x + dx


def keep_in_grid_x(grid, y, x, dy, dx):
    if x + dx > len(grid[y]) - 1:
        nx = 0
    else:
        nx = len(grid[y]) - 1
    return y + dy, nx


if __name__ == '__main__':
    print("Tip: use a 3x3 or less board for testing. A bigger board takes a bit too long...")
    h = input("Height: ")
    w = input("width: ")
    board = []
    print("Input board (row by row and separate letters with a space):")
    for i in range(int(h)):
        board.append(input().upper().split())
    words = solve(board, h, w)
    for word in words:
        print(word)
