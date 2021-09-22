import copy
illegalStates = [
    "CG|FW", "GW|CF", "FW|CG", "F|CGW","CGW|F","CF|GW"]
path = []

def dfs (node, path=[]):

    path = path + [node.getname()]

    if is_goal(node.east):
        print("Het is gelukt!")
        return [path]

    paths = []

    for child in successors(node):

        stringcheck = child.getname()
        if stringcheck not in path:
            newpaths = dfs(child, path)

            for newpath in newpaths:
                paths.append(newpath)

    return paths

def is_goal(node):
    if "CFGW" in node:
        return True

def successors(node1):
    neighbours = []
    tw = copy.deepcopy(node1.west)
    te = copy.deepcopy(node1.east)
    f = "F"

    if "F" in tw:
        te = te + f
        tw1 = tw.replace("F", "")
        twfnode = node(tw1, te)
        if isLegal(twfnode.getname()):
            neighbours.append(twfnode)
        for x in tw1:
            if x != "F":
                te1 = te + x
                tw2 = tw1.replace(x, '')
            addnode = node(tw2, te1)
            if isLegal(addnode.getname()):
                neighbours.append(addnode)
        return neighbours

    if "F" in te:
        tw = tw + "F"
        te2 = te.replace("F", '')
        tefnode = node(tw, te2)
        if isLegal(tefnode.getname()):
            neighbours.append(tefnode)
        for x in te2:
            if x != "F":
                tw3 = tw + x
                te3 = te2.replace(x, '')
            addnode1 = node(tw3, te3)
            if isLegal(addnode1.getname()):
                neighbours.append((addnode1))
        return neighbours


    return neighbours

class node:
    def __init__(self, west, east):
        self.west = ''.join(sorted(west))
        self.east = ''.join(sorted(east))



    def getname(self):
        return "" + self.west +"|" + self.east

def isLegal(node):
    if node in illegalStates:
        return False
    return True

startnode = node("CFGW", "")
print(dfs(startnode))