import copy
characters = ["W","G","C"]
forbidden = [["G", "W"], ["C", "G"]]
forbidden2 = ["GW", "CG"]
west = []
east = []
nodes = []
winningNodes = []

class main:
    def search(self):
        tw = copy.deepcopy(characters)
        te = []
        n = node(tw, te, False, [])

        nodes.append((n))
        while len(nodes) > 0:
            result = nodes[0].getNodes()
            nodes.remove(nodes[0])
            # print(result)
            for x in result:
                if len(x[0]) == 0:
                    # winningNodes.append[copy.deepcopy(x)]
                    print("winner")
                else:
                    tempName = getName(x[0], x[1])
                    valid = True
                    for y in x[3]:
                        if getName(x[0], x[1]) == y:
                            valid = False
                        else:
                            print("")

                    # print(str(x[0]) + " " + str(x[1]))
                    if valid:
                        print(x[3])
                        x[3].append(getName(x[0],x[1]))
                        nodes.append(node(x[0], x[1], not x[2], x[3]))
            print(len(nodes))



def getName( WEST, EAST):
    name = ""
    for x in WEST:
        name += x
    name += "|"
    for x in EAST:
        name += x
    return name

class node:
    def __init__(self, WEST, EAST, SIDE, VISITED):
        self.west = WEST
        self.east = EAST
        self.side = SIDE
        self.visitedNodes = VISITED
        for x in self.west:
            if x == " " :
                self.west.remove(" ")
                continue

        for x in self.east:
            if x == " " :
                self.east.remove(" ")
                continue
        self.west.append(" ")
        self.east.append(" ")
        # print(VISITED)

        self.west.sort()
        self.east.sort()

    def getNodes(self):
        res = []
        if self.side:
            for x in self.east:
                te = copy.deepcopy(self.east)
                tw = copy.deepcopy(self.west)
                tw.append(x)
                tw.sort()
                te.remove(x)

                valid = True
                for x in forbidden2:
                    tne = ""
                    tnw = ""
                    for y in te:
                        tne += y

                    for y in tw:
                        tnw += y

                    if (tnw in x and len(tnw) > 1) or (tne in x and len(tne) > 1):
                        valid = False
                if valid:
                    res.append((tw, te, self.side, self.visitedNodes))
        else:
            for x in self.west:
                te = copy.deepcopy(self.east)
                tw = copy.deepcopy(self.west)
                te.append(x)
                te.sort()
                tw.remove(x)

                valid = True
                for x in forbidden2:
                    tne = ""
                    tnw = ""
                    for y in te:
                        tne += y

                    for y in tw:
                        tnw += y

                    if (tnw in x and len(tnw) > 1) or (tne in x and len(tne) > 1):
                        valid = False
                # print(str(tw) + " " + str(te))
                if valid:

                    res.append((tw, te, self.side, self.visitedNodes))
        return res

m = main()
m.search()


