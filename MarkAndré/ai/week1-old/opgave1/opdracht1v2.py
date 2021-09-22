import copy
ilegalStates = ["CG|FW", "GW|CF", "FW|CG", "F|CGW", "CGW|F", "CF|GW"]
characters = ["C", "", "G", "W"]
west, east, nodes = ([] for i in range(3))

def getName(WEST, EAST):
    name = "".join([x for x in WEST]) + "|" + "".join([x for x in EAST])
    return name

class main:
    def search(self):
        nodes.append((node(["C", "F", "G", "W"], [], ["CFGW|"])))

        while len(nodes) > 0:
            result = nodes.pop().getNodes()

            for x in result:
                tempName = getName(x[0], x[1])

                if tempName == "|CFGW":
                    x[2].append(getName(x[0], x[1]))
                    print("winner = " + str(x[2]))
                else:
                    valid = True
                    for y in x[2]:
                        if tempName == y: valid = False

                    if valid:
                        x[2].append(getName(x[0], x[1]))
                        nodes.append(node(x[0], x[1], x[2]))

class node:
    def __init__(self, WEST, EAST, VISITED):
        self.west = WEST
        self.east = EAST
        self.west.append("")
        self.east.append("")
        self.visitedNodes = VISITED

    def getNodes(self):
        self.res = []
        self.direction = [self.west, self.east]
        self.i = 1
        if "F" in self.east:
            self.i = 0

        self.direction[self.i].append(self.direction[not self.i].pop(self.direction[not self.i].index("F")))
        self.direction[self.i].sort()
        self.step(self.direction[not self.i])
        return self.res

    def step(self, side):
        for x in side:
            te = copy.deepcopy(self.east)
            tw = copy.deepcopy(self.west)
            td = [te, tw]
            te.remove("")
            tw.remove("")

            if x != "":
                td[self.i].remove(x)
                td[not self.i].append(x)
                td[not self.i].sort()
            if self.check(getName(tw, te)): self.res.append((copy.deepcopy(tw), copy.deepcopy(te), copy.deepcopy(self.visitedNodes)))

    def check(self, tn):
        return not tn in ilegalStates

m = main().search()