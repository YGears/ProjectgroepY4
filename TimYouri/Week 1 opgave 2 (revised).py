def solve(grid, h, w):
    results = []                                                                            # Lijst voor alle gevonden woorden
    d = []                                                                                  # Lijst met alle woorden uit woordenlijst
    with open('words_NL.txt') as f:
        for line in f:
            d.append(line.upper()[:-1])                                                     # Voeg woorden uit woordenlijst toe aan d
    for y in range(int(h)):
        for x in range(int(w)):
            print('checking position')
            results += find_words(grid, d, grid[y][x], y, x, set((y, x)))                   # Voer DFS uit op elke positie in de grid
    return set(results)                                                                     # maak een set van alle gevonden woorden om duplicatenten voorkomen


def find_words(grid, words, current, y, x, used):                                           # DFS algoritme
    neighbors = [(-1, 0), (0, -1), (0, 1), (1, 0)]                                          # Alle kanten waar het DFS gaat zoeken
    found = []
    if current in words:
        found.append(current)                                                               # Als de gevonden letter overeen komen met een woord, voeg dat woord toe aan de lijst
    for dy, dx in neighbors:
        if y == 0 and dy == -1 or y == len(grid) - 1 and dy == 1:                           # Check of de nieuwe y positie buiten de grid valt
            ny, nx = keep_in_grid_y(grid, y, x, dy, dx)                                     # Als de nieuwe y positie buiten de grid is, wrap around
        elif x == 0 and dx == -1 or x == len(grid[y]) - 1 and dx == 1:                      # Check of de nieuwe x positie buiten de grid valt
            ny, nx = keep_in_grid_x(grid, y, x, dy, dx)                                     # Als de nieuwe x positie buiten de grid is, wrap around
        else:
            ny, nx = y + dy, x + dx                                                         # Als beide binnn de grid vallen, update positie
        if (ny, nx) not in used:
            used.add((ny, nx))                                                              # Voeg positie toe aan de lijst met alle gecheckte posities voor deze start letter
            found.extend(find_words(grid, words, current + grid[ny][nx], ny, nx, used))     # Recursion. Check alle mogelijke posities voor elke start letter
            used.remove((ny, nx))                                                           # Haal de positie uit de lijst met gecheckte positie om de lijst klaar te maken voor de volgende DFS
    return list(set(found))


def keep_in_grid_y(grid, y, x, dy, dx):
    if y + dy > len(grid) - 1:
        ny = 0                                                                              # Als de nieuwe positie de ondergrens van de grid overschrijd, maak de y positie 0 (wrap around)
    else:
        ny = len(grid) - 1                                                                  # Als de nieuwe positie de bovengrens van de grid overschrijd, maak de y positie de hoogte van de grid -1 (wrap around)
    return ny, x + dx


def keep_in_grid_x(grid, y, x, dy, dx):
    if x + dx > len(grid[y]) - 1:                                                           # Als de nieuwe positie de rechter grens van de grid overschrijd, maak de x positie 0 (wrap around)
        nx = 0
    else:
        nx = len(grid[y]) - 1                                                               # Als de nieuwe positie de linker grens van de grid overschrijd, maak de y positie de breete van de grid -1 (wrap around)
    return y + dy, nx


if __name__ == '__main__':
    print("Tip: use a 3x3 or less board for testing. A bigger board takes a bit too long...")
    h = input("Height: ")                                                                   # Input de hoogte van het bord (grid)
    w = input("width: ")                                                                    # Input de breede van het bord (grid)
    board = []
    print("Input board (row by row and separate letters with a space):")
    for i in range(int(h)):
        board.append(input().upper().split())                                               # Input het bord
    words = solve(board, h, w)                                                              # Start met zoeken naar woorden
    for word in words:
        print(word)
