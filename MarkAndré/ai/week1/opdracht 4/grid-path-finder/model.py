import random
import heapq
import math
import config as cf
import copy

# global var
goal = [0,0]
app = 0
grid  = [[0 for x in range(cf.SIZE)] for y in range(cf.SIZE)]
visitedNodes = {}
directions = [ #hor, vert
    [1,0], #right centre
    [0,1], #centre bottom
    [0,-1], #centre top
    [-1,0] #left centre
]

class PriorityQueue:
    # a wrapper around heapq (aka priority queue), a binary min-heap on top of a list
    def __init__(self):
        # create a min heap (as a list)
        self.elements = []
    
    def empty(self):
        return len(self.elements) == 0
    
    # heap elements are tuples (priority, item)
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    
    # pop returns the smallest item from the heap
    # i.e. the root element = element (priority, item) with highest priority
    def get(self):
        return heapq.heappop(self.elements)[1]

def bernoulli_trial(app):
    return 1 if random.random() < int(app.prob.get())/10 else 0

def get_grid_value(node):
    # node is a tuple (x, y), grid is a 2D-list [x][y]
    return grid[node[0]][node[1]]

def set_grid_value(node, value): 
    # node is a tuple (x, y), grid is a 2D-list [x][y]
    grid[node[0]][node[1]] = value

def search(newapp, start, newgoal, alg):
    # plot a sample path for demonstration
    # for i in range(cf.SIZE-1):
    #     app.plot_line_segment(i, i, i, i+1, color=cf.FINAL_C)
    #     app.plot_line_segment(i, i+1, i+1, i+1, color=cf.FINAL_C)
    #     app.pause()
    global goal, app, visitedNodes
    visitedNodes = {}
    goal = newgoal
    app = newapp
    step(start, alg)

def step(start, alg):
    mQ = PriorityQueue()
    dist = distance(start)
    mQ.put(start, dist)
    step = 0
    newX = 0
    newY = 0
    visitedNodes[(0, 0)] = "start"

    while dist > 0:
        try:
            app.pause()
            workingTup = mQ.get()
            # app.plot_line_segment(workingTup[0], workingTup[1], newX, newY, color=cf.FINAL_C)
        except:
            print("No routes possible")
            break

        for x in directions:
            newX = workingTup[0] + x[0]
            newY = workingTup[1] + x[1]

            if(newX < 0 or newY < 0 or newX == cf.SIZE or newY == cf.SIZE):
                continue

            if not get_grid_value((newX, newY)) == -1:
                app.plot_line_segment(workingTup[0], workingTup[1], newX, newY, color=cf.BLOCK_C)
                continue

            temptup = (newX, newY)
            if not (newX, newY) in visitedNodes:

                step += 1
                visitedNodes[(newX, newY)] = (workingTup[0], workingTup[1])
                dist = distance(temptup)

                if alg == "A*":
                    mQ.put(copy.deepcopy(temptup),copy.deepcopy(dist))
                else:
                    mQ.put(copy.deepcopy(temptup),step)

                app.plot_node((newX, newY), cf.PATH_C)
                if newY == 24 and newX == 24:

                    draw((24, 24))
                    break

def draw(node):
    prevNode = visitedNodes.get(node)
    if not node == "start":
        app.plot_line_segment(node[0], node[1], prevNode[0], prevNode[1], color=cf.FINAL_C)
        draw(prevNode)

def distance(node):
    a = (goal[0] - node[0]) * (goal[0] - node[0])
    b = (goal[1] - node[1]) * (goal[1] - node[1])
    c = a + b
    return round(math.sqrt(c),6)