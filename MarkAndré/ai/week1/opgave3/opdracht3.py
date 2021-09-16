from bord import bord
import heapq
import copy

class main():

    def start(self ):
        step = 0
        currVal = 1
        b = bord()
        self.boards = []
        heapq.heappush(self.boards, (currVal, step, bord()))
        node = (0,4)

        while len(self.boards) > 0:
            first = False
            low = self.getLowest()
            bd = low[2]
            currVal = low[0] + 1
            node = bd.latestChanged()
            temp = bd.getCloseNodes(node, currVal)

            for x in temp:
                t = copy.deepcopy(bd)
                t.setClue(x, currVal)
                heapq.heappush(self.boards, (currVal, step, t))
                step += 1
                if currVal == 81:
                    t.printBord()
                    print(step)

    def getLowest(self):
        return heapq.heappop(self.boards)

m = main()
m.start()

