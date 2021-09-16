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
    # [1,1], #right top
    # [-1,1], #left top
    # [-1,-1], #left bottom
    # [-1,-1], #left bottom
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
            app.pause()#teken nieuwe bezochte nodes
            workingTup = mQ.get()#get de beste node
        except:
            print("No routes possible")
            break

        for x in directions:# voor alle directies
            newX = workingTup[0] + x[0] # get new x-as for node
            newY = workingTup[1] + x[1] # get new y as for node

            if(newX < 0 or newY < 0 or newX == cf.SIZE or newY == cf.SIZE):#als de nieuwe node buiten de grid valt
                continue

            if not get_grid_value((newX, newY)) == -1: #als de nieuwe node een blocked node is
                continue

            temptup = (newX, newY) #maak een tijdelijke tuple van de nieuwe coords
            if not (newX, newY) in visitedNodes:# if not in visited nodes (dus nog niet gezien)

                visitedNodes[(newX, newY)] = (workingTup[0], workingTup[1]) # stop de node in visited node en vanuit welke node hij is bereikt.
                dist = distance(temptup) #get distance tot de goal

                if alg == "A*": # op basis van welke alg gebruikt wordt verander je de manier waarop de weight gedaan wordt
                    mQ.put(copy.deepcopy(temptup),copy.deepcopy(dist))
                else:
                    step += 1 #increase step count
                    mQ.put(copy.deepcopy(temptup),step)

                app.plot_node((newX, newY), cf.PATH_C)

                if temptup == cf.GOAL:# als het eind bereikt is teken dan het lijn en stop de loop
                    draw(temptup)
                    break

def draw(node):#van eind tot start get preceding node van node en teken een lijn. Doe het dan met de preceding node van de preceding node. herhaal tot je bij start bent.
    prevNode = visitedNodes.get(node) # get preceding node
    if not prevNode == None: # als er geen preceding node is (en dus  de 1e is)
        app.plot_line_segment(node[0], node[1], prevNode[0], prevNode[1], color=cf.FINAL_C)# draw line
        app.pause()
        draw(prevNode)# recursive call

def distance(node):
    a = (goal[0] - node[0]) * (goal[0] - node[0])
    b = (goal[1] - node[1]) * (goal[1] - node[1])
    c = a + b
    result = round(math.sqrt(c),6)
    return result