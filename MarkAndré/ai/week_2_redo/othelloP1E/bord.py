class bord:
    def __init__(self, GRID, MOVES, TURN):
        self.turn = TURN
        self.grid = GRID
        self.moves = MOVES

    def getGrid(self):
        return self.grid

    def getMoves(self):
        return self.moves

    def getTurn(self):
        return self.turn