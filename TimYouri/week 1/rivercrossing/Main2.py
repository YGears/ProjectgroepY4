import copy
illegalStates = [
    "CG|FW", "GW|CF", "FW|CG", "F|CGW","CGW|F","CF|GW"]
path = []

def dfs (node, path=[]):  # deze functie is overgenomen/gebruikt als template van de slides ai les 2

    path = path + [node.getname()] #pathname appending list aan list

    if is_goal(node.east):  # check naar eindstreep, direct uit deze iteratie van de loop lopen
        print("Het is gelukt!")
        return [path]

    paths = []  # lijst van lijsten van path

    for child in successors(node):  # recursive functie, successors geeft geldige succesors terug

        stringcheck = child.getname()  # check op nodenaam, niet memoryaddress
        if stringcheck not in path:
            newpaths = dfs(child, path)  # nog niet bezocht is nieuwe iteratie, returned die iteratie's paths[]

            for newpath in newpaths:  # toevoeging newpaths in paths
                paths.append(newpath)

    return paths

def is_goal(node): # check of einddoel is bereikt, in dit geval CFGW
    if "CFGW" in node:
        return True

def successors(node1): # functie om successor terug te geven (lijst van objecten)
    neighbours = [] # de lijst van objecten, per node opnieuw ingesteld
    tw = copy.deepcopy(node1.west)
    te = copy.deepcopy(node1.east)
    f = "F"
    # loopt door alle mogelijke opties afhankelijk van de positie van Farmer, sinds die nodig is om iets anders te verplaatsen
    if "F" in tw:
        te = te + f # farmer verplaatst altijd
        tw1 = tw.replace("F", "")
        twfnode = node(tw1, te) # één optie is altijd dat de farmer alleen teruggaat
        if isLegal(twfnode.getname()): # check of de node dan wel legal is
            neighbours.append(twfnode) # if so, toevoegen aan neighbours
        for x in tw1:  # door alle resterende opties van west lopen en de node toevoegen als de node geldig is
            if x != "F":
                te1 = te + x
                tw2 = tw1.replace(x, '')
            addnode = node(tw2, te1)
            if isLegal(addnode.getname()):
                neighbours.append(addnode)
        return neighbours
    # geld hetzelfde voor de vorige loop maar dan van east naar west
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

    # geeft aan het eind alle opties terug
    return neighbours

class node:
    def __init__(self, west, east):  # klasse heeft maar 2 variabelen, west en east
        self.west = ''.join(sorted(west))
        self.east = ''.join(sorted(east))



    def getname(self):  # naamgeving is altijd geordened en hetzelfde
        return "" + self.west +"|" + self.east

def isLegal(node):  # loopt door illegalstates en kijkt of de node.getname hier in voorkomt
    if node in illegalStates:
        return False
    return True

startnode = node("CFGW", "")  # startsituatie in een node
print(dfs(startnode))