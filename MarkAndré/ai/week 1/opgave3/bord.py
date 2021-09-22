directions = [ #hor, vert
    [1,0], #right centre
    [0,1], #centre bottom
    [0,-1], #centre top
    [-1,0] #left centre
]

class bord:
    def __init__(self):
        SIZE = 9
        self.grid = [[0 for x in range(SIZE)] for y in range(SIZE)]
        self.size = SIZE
        self.goal = SIZE * SIZE
        self.visitedNodes = ((0,4))

        presetnodes = (
        [(0, 0), 7], [(0, 2), 3], [(0, 4), 1], [(0, 6), 59], [(0, 8), 81], [(1, 3), 33], [(1, 4), 34], [(1, 5), 57],
        [(2, 0), 9], [(2, 2), 31], [(2, 6), 63], [(2, 8), 79], [(3, 1), 29], [(3, 7), 65], [(4, 0), 11], [(4, 1), 12],
        [(4, 4), 39], [(4, 7), 66], [(4, 8), 77], [(5, 1), 13], [(5, 7), 67], [(6, 0), 15], [(6, 2), 23], [(6, 6), 69],
        [(6, 8), 75], [(7, 3), 43], [(7, 4), 42], [(7, 5), 49], [(8, 0), 19], [(8, 2), 21], [(8, 4), 45], [(8, 6), 47],
        [(8, 8), 73])

        for x in presetnodes:
            self.setClue(x[0],x[1])
        self.latest = (0,4)

    def latestChanged(self):
        return self.latest

    def printBord(self):
        for y in range(self.size):
            line = ""
            for x in range(self.size):
                if self.grid[x][y] > 9:
                    line += " " + str(self.grid[x][y])
                else:
                    line += "  " + str(self.grid[x][y])
            print(line)

    def setClue(self, node, value):
        self.latest = node
        self.grid[node[1]][node[0]] = value

    def getCloseNodes(self, node, currVal):
        self.currentVal = currVal
        res = []
        for x in directions:

            tempX = node[0] + x[0]
            tempY = node[1] + x[1]
            tempNode = (tempX, tempY)
            if tempX < 0 or tempY < 0 or tempX == self.size or tempY == self.size or tempNode in self.visitedNodes :
                continue
            else:
                if self.grid[tempY][tempX] == 0:
                    res.append((node[0] + x[0], node[1] + x[1]))
                else:
                    if self.grid[tempY][tempX] == self.currentVal:
                        res.clear()
                        res.append((node[0] + x[0], node[1] + x[1]))
                        break
        return res