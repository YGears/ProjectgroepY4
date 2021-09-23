import random


def create_board():
    # A list to store the board
    grid = []
    # A list of letters in the alphabet
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                'n', 'o', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'y', 'z']
    # A for loop for row (i) entries (left to right)
    for i in range(size):
        board_rows = []  # Empty List witch wil be used to store multiple lists of rows for nxn bord
        # A for loop for column (j) entries (Top to bottom)
        for j in range(size):
            board_rows.append(random.choice(alphabet)) # Add a random letter from the alphabet to a list of board_rows
        grid.append(board_rows)  # add a list of board_rows to the board (grid -> list)
    return grid


# Function to print nxn board to CLI
def print_board(grid):
    for i in range(size):
        for j in range(size):
            print(grid[i][j], end=" ")  # Print 1 Letter with whitespace
        print()  # Linebreak


# Function to import words from txt to python list
def import_words():
    wordlist = []  # Create a list to store the words
    with open("words_NL.txt", "r") as f:
        for line in f:
            word = line.strip()  # remove blank space
            wordlist.append(word)  # add word to list of words
    return wordlist


# Function to create a set of prefix from the words
def create_prefix(words):
    prefix_set = set()  # A Set to store all prefixes, its a set so no duplicates
    for word in words:
        for x in range(1, len(word)):  # For every word in words
            prefix_set.add(word[0:x])       # Add the letter(neighbour) of word to the prefix
    return prefix_set


# A Function to get adjacent cells for a Node (i = Rows , j = Columns)
def get_adjacent_letters(i, j):
    # List to store adjacent cells for a Node values are stored as : (Left),(Right),(Up),(Down)
    adjacent_cells = [((i - 1) % size, j), ((i + 1) % size, j), (i, (j - 1) % size), (i, (j + 1) % size)]
    return adjacent_cells


def dfs(x, y, route, visited, final):
    # for each neighbour, check if the route is in the words array and print it
    # then, check if it is in the prefix array, and then solve for that state
    visited.append((x, y))
    for neighbour in get_adjacent_letters(x, y):
        # Get the letter of board[location]
        letter = board[neighbour[0]][neighbour[1]]
        # Add letter to the current route, route is a group of letters that can form a word from the prefix
        route = route + letter
        if neighbour not in visited:
            if route in words:
                print("Woord gevonden: {}".format(route))
                # If its a word add it to the list
                final.append(route)
            if route in prefix_set:
                # If route (combination of letters) is in prefix_set call dfs
                dfs(neighbour[0], neighbour[1], route, visited.copy(), final)
        # reversing the route for backtracking purpose
        route = route[:-1]
    return final


# A Function to find all possible words using dfs
def find_words():
    results = []  # List to store all possible words
    for x in range(size):
        for y in range(size):
            dfs(x, y, board[x][y], [], results)  # For each grid(x,y) location call function dfs
    return results


# NxN means x/i/row and y/j/col are equal for bord size
print("Enter bord size n :")
size = int(input())
board = create_board()
print_board(board)
words = import_words()
prefix_set = create_prefix(words)
print()
#import timeit
#start = timeit.default_timer()
results = find_words()
print(results)
#stop = timeit.default_timer()
#print('Time: ', stop - start)


# Time complexity is O(n^2)
# n = board size --> 1x1, 2x2, 3x3 nxn --> n^2
# find_words , nested forloop --> n^2

'''
Sources 
https://stackabuse.com/depth-first-search-dfs-in-python-theory-and-implementation/
https://stackoverflow.com/questions/13475409/python-boggle-game
https://www.w3schools.com/python/ref_random_choice.asp
https://stackoverflow.com/questions/509211/understanding-slice-notation
+ wat commands van andere stackoverlows
AI Les 1 --> https://www.youtube.com/watch?v=F3RIW0AV8co
AI Les 2 --> https://www.youtube.com/watch?v=KdQBEukytGY
'''