import copy
# CFGW
ilegalStates = [
    "CG|FW",
    "GW|CF",
    "FW|CG",
    "F|CGW",
    "CGW|F",
    "CF|GW"
]
characters = ["C", "", "G", "W"]
west = []
east = []
nodes = []
winningNodes = []

class main:
    def search(self):
        te = []
        tw = ["C", "F", "G", "W"]
        n = node(tw, te, ["CFGW|"])
        nodes.append((n))

        while len(nodes) > 0:
            result = nodes[0].getNodes()
            nodes.remove(nodes[0])
            for x in result:
                tempName = getName(x[0], x[1])
                if tempName == "|CFGW":
                    x[2].append(getName(x[0],x[1]))
                    print("winner")
                    print(x[2])
                else:
                    valid = True
                    for y in x[2]:
                        if tempName == y:
                            valid = False

                    if valid:
                        x[2].append(getName(x[0],x[1]))
                        nodes.append(node(x[0], x[1], x[2]))

def getName( WEST, EAST):
    name = ""
    for x in WEST:
        name += x
    name += "|"
    for x in EAST:
        name += x
    return name

class node:
    def __init__(self, WEST, EAST,  VISITED):
        self.west = WEST
        self.east = EAST
        self.west.append("")
        self.east.append("")
        self.visitedNodes = VISITED

    def getNodes(self):
        res = []
        if "F" in self.east:
            if len(self.visitedNodes) == 7 :
                print(self.east)

            self.east.remove("F")
            self.west.append("F")
            for x in self.east:

                te = copy.deepcopy(self.east)
                tw = copy.deepcopy(self.west)
                tw.sort()
                te.remove("")
                tw.remove("")

                if x != "":
                    te.remove(x)
                    tw.append(x)
                    tw.sort()

                if self.check(tw, te):
                    res.append((copy.deepcopy(tw), copy.deepcopy(te), copy.deepcopy(self.visitedNodes)))
        else:
            self.west.remove("F")
            self.east.append("F")

            for x in self.west:
                te = copy.deepcopy(self.east)
                tw = copy.deepcopy(self.west)
                te.remove("")
                tw.remove("")

                if x != "":
                    tw.remove(x)
                    te.append(x)
                    te.sort()

                if self.check(tw, te):
                    res.append((copy.deepcopy(tw), copy.deepcopy(te), copy.deepcopy(self.visitedNodes)))
        return res

    def check(self, tw, te):
        valid = True
        tn = getName(tw, te)

        for x in ilegalStates:
            if tn in x :
                valid = False

        return valid

m = main()
m.search()