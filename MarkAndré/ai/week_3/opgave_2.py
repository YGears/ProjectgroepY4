import math as math
import itertools as itertools
import copy as copy
'''Constraints:
    1 every Ace borders a King
    2 every King borders a Queen
    3 every Queen borders a Jack
    4 no Ace borders a Queen
    5 no two of the same cards border each other
A:
    1: 40320, n!
    2: 3809
C

------------plek 5
5 kan niet a zijn omdat 
	4 of 3 een A moet zijn omdat alleen 3 en 4 een andere square grenzen zodat de heer een vrouw grenzt
	
	3 en 4 kunnen niet allebei een heer zijn want
		als 3 en 4 een Heer is dan
				kan alleen 0 een A zijn omdat
				als 2 een A is dan kan Heer4 geen vrouw grenzen en de andere squares grenzen geen heer
			
			waardoor 1 een boer moet zijn omdat een vrouw een boer moet grenzen
			
			waardoor op 6 of 7 een vrouw moet zijn wat niet kan omdat de A geen vrouw kan grenzen

5 kan geen Vrouw zijn want 
	dan moet de andere vrouw op 1, 2 of 0 zijn omdat de elkaar niet mogen borderen
	
	de vrouw kan niet op 0 want dan moet 3 een boer zijn 
		dat kan niet want de enigste squares over met 2 grenzen (voor de heer) grenzen met elkaar

Als 5 een boer is dan 
	moet de andere boer op 0, 1 of 2 staan	
	
	de boer kan niet op 0 want dan 
		moetten de vrouwen op 3 en 4 staan 
			waardoor alleen square 2 de heer kan hebben en er zijn nog 2 heren over
			
----- nu voor plek 0
Als 0 een A is dan moet 3 een heer zijn waardoor 2 of 5 een vrouw moet zijn
    als 2 een vrouw is dan moet 1 of 4 een boer zijn
        als 1 een boer is dan kan 4 boer of heer zijn
            als 4 een boer is dan moet 5 een vrouw zijn
                waardoor je een aas op 6 of 7 moet staan wat niet mag omdat hij dan geen heer grenst.
            als 4 een heer is dan moet 5 een aas zijn
                waardoor je een vrouw op 6 of 7 moet staan wat niet mag omdat ze dan geen boer grenst.
                
    als 5 een vrouw is dan moet er een boer op 4, 6 of 7 staan
        als er een boer op 4 staat dan kan 2 alleen een aas of een vrouw zijn
            als 2 een aas is dan kan de overgebleven vrouw alleen op 1 komen, wat neit kan omdat ze dan geen boer grenzt
            als 2 een vrouw is dan is er geen plek meer voor de overgebleven aas om aan een heer te grenzen
    
    
als 0 een boer is dan kan 3 een aas, heer of vrouw zijn
    als 3 een aas is dan moet 2 of 5 een heer zijn
        als 2 een heer is dan moet 1 of 4 een vrouw zijn
            als 1 een vrouw is grenzt ze geen boer
            als 4 een vrouw is dan moet 5 een boer zijn
                waardoor 6 of 7 een vrouw moet zijn
                    waardoor er geen plek is voor een heer om een vrouw te grenzen
    als 3 een heer is dan moet 5 een vrouw zijn
        als 5 een vrouw is dan moet de andere vrouw op 1 of 2 staan
            als 1 een vrouw is dan moet 2 een boer zijn
                waardoor een geen plek meer is voor de andere aas om een heer te grenzen
        
    als 3 een vrouw is dan kan op 5 een heer of boer staan
        als 5 een heer is dan kan de andere heer alleen op 1 staan
            waardoor plek 2 een vrouw moet zijn, maar dit mag niet
        als 5 een boer is dan kan plek 2 een boer of heer staan
            als 2 een boer is dan is er geen plek waar een aas een heer kan grenzen
            als 2 een heer is dan moet 1 en 4 een aas zijn 
                waardoor een heer op 6 of 7 moet staan, wat niet kan omdat hij dan geenv rouw grenzt

waardoor 0 een heer moet zijn
        
'''
# the board has 8 cells, let’s represent the board with a dict key=cell, value=card
start_board = {cell: '.' for cell in range(8)}
cards = ['K', 'K', 'Q', 'Q', 'J', 'J', 'A', 'A']
neighbors = {0:[3], 1:[2], 2:[1,4,3], 3:[0,2,5], 4:[2,5], 5:[3,4,6,7], 6:[5], 7:[5]}

def is_valid(board):
    if AbordersK(board) and KbordersQ(board) and QbordersJ(board) and AnotbordersQ(board) and XnotborderX(board):
        return True
    return False

def AbordersK(board):
    abk = True
    for x in range(len(board)): # elke A grenst een K
        if board[x] == 'A':
            borderingCards = []

            for y in neighbors[x]:
                borderingCards.append(board[y])
            if 'K' not in borderingCards: abk = False
    return abk

def KbordersQ(board):
    kbq = True
    for x in range(len(board)): # elke heer grenst een vrouw
        if board[x] == 'K':
            borderingCards = []

            for y in neighbors[x]:
                borderingCards.append(board[y])
            if 'Q' not in borderingCards: kbq = False

    return kbq

def QbordersJ(board):
    qbj = True
    borderingCards = []
    for x in range(len(board)): # elke vrouw grenst een boer
        if board[x] == 'Q':
            borderingCards = []

            for y in neighbors[x]:
                borderingCards.append(board[y])
            if 'J' not in borderingCards: qbj = False
    return qbj

def AnotbordersQ(board):
    anbq = True
    borderingCards = []
    for x in range(len(board)): # elke Aas grenst geen vrouw
        if board[x] == 'A':
            borderingCards = []

            for y in neighbors[x]:
                borderingCards.append(board[y])
            if 'Q' in borderingCards: anbq = False
    return anbq

def XnotborderX(board): # geen kaart mag zichzelf grenzen
    xnbx = True
    for x in range(len(board)):
        for y in neighbors[x]:
            if y != x and board[x] in cards:
                if board[y] == board[x]:
                    xnbx = False
    return xnbx

def test():
    # is_valid(board) checks all cards, returns False if any card is invalid
    print('f ',is_valid({0: 'J', 1: 'K', 2: 'Q', 3: 'Q', 4: 'J', 5: 'K', 6: 'A', 7: 'A'}))
    print('f ',is_valid({0: 'J', 1: 'J', 2: 'Q', 3: 'Q', 4: 'K', 5: 'K', 6: 'A', 7: 'A'}))
    print('t ',is_valid({0: '.', 1: '.', 2: '.', 3: '.', 4: '.', 5: '.', 6: '.', 7: '.'}))
    print('t ',is_valid({0: 'J', 1: '.', 2: '.', 3: '.', 4: '.', 5: '.', 6: '.', 7: '.'}))
    print('f ',is_valid({0: '.', 1: '.', 2: '.', 3: 'J', 4: 'J', 5: 'A', 6: 'J', 7: 'J'})) # [1]
    print('f ',is_valid({0: 'J', 1: '.', 2: '.', 3: '.', 4: 'J', 5: 'K', 6: 'J', 7: 'Q'})) # [3]
    print('f ',is_valid({0: '.', 1: 'Q', 2: '.', 3: '.', 4: 'Q', 5: 'J', 6: '.', 7: '.'})) # [3] # opdracht zei true maar is nie zo
    print('f ',is_valid({0: 'Q', 1: '.', 2: '.', 3: 'K', 4: '.', 5: '.', 6: '.', 7: '.'})) # [3]
    print('f ',is_valid({0: '.', 1: 'A', 2: 'Q', 3: '.', 4: '.', 5: 'Q', 6: '.', 7: '.'})) # [4]
    print('f ',is_valid({0: '.', 1: '.', 2: '.', 3: '.', 4: 'J', 5: 'J', 6: '.', 7: '.'})) # [5]
    print('f ',is_valid({0: '.', 1: '.', 2: '.', 3: '.', 4: '.', 5: 'Q', 6: '.', 7: 'Q'})) # [5]
    print('f ',is_valid({0: 'Q', 1: 'Q', 2: '.', 3: '.', 4: '.', 5: '.', 6: '.', 7: '.'})) # opdracht zei true maar is nie zo
    print('t ',is_valid({0: '.', 1: 'Q', 2: 'J', 3: 'Q', 4: '.', 5: '.', 6: '.', 7: '.'})) # eigen
    print('f ',is_valid({0: '.', 1: '.', 2: 'Q', 3: '.', 4: '.', 5: 'Q', 6: 'J', 7: '.'})) # eigen
    print('t ',is_valid({0: 'K', 6: 'K', 2: 'Q', 5: 'Q', 4: 'J', 7: 'J', 1: 'A', 3: 'A'})) # eigen


def opdrA():
    validboards = []
    steps = 0
    numbers = [0,1,2,3,4,5,6,7]
    for x in list(itertools.permutations(numbers)):
        steps += 1
        tempCard = cards
        cardset = {}

        for y in x:
            cardset[y] = tempCard[0]
            tempCard = [z for z in tempCard[1:]]

        if is_valid(cardset):
            tempset = {}
            for y in range(8):
                tempset[y] = cardset[y]
            if not tempset in validboards:
                validboards.append(copy.deepcopy(tempset))
    for x in validboards:
        print(x)


def opdrB():

    tempCardset = copy.deepcopy(cards)
    tempCardset.remove("J")
    childs = []
    childsset = {}
    step = 0
    for x in neighbors:
        print(x)
        result = node((x, "J"), {0: '.', 1: '.', 2: '.', 3: '.', 4: '.', 5: '.', 6: '.', 7: '.'}, copy.deepcopy(tempCardset), step)
        childs.append(result)

    tempres = []
    for x in childs:
        for y in x[1]:
            if not "." in y.values():
                if not y in tempres:
                    tempres.append(y)
    for x in tempres:
        print(x)


def node(card, bordset, cardset, step):
    step += 1
    if not bordset[card[0]] == ".": # als hij een plek wil invullen die al gevuld is
        return (False, [bordset])

    bordset[card[0]] = card[1] # zet card op plek van bord

    if not XnotborderX(bordset): # als hij zichzelf grenzt
        return (False, [bordset])

    if card[1] == "K":
        if not KbordersQ(bordset): # als de koning niet een vrouw grenst return false
            return (False, [bordset])
    else:
        if not AnotbordersQ(bordset): # als een aas geen vrouw grenst return false
            return (False, [bordset])

        if card[1] == "Q":
            if not QbordersJ(bordset):# als een vrouw niet een boer grenst return false
                return (False, [bordset])
        elif card[1] == "A":
            if not AbordersK(bordset):
                return(False, bordset)

    if len(cardset) > 0: # als er nog kaarten zijn die gespeeld moetten worden
        childs = []
        for x in cardset: # maak voor elke kaart een niewe bord, haal deze kaart uit de kaartset
            tempCardset = copy.deepcopy(cardset)
            tempCardset.remove(x)
            for y in neighbors: # redeneer ermee verder voor elke neighbor
                childs.append(node((y, x), copy.deepcopy(bordset), tempCardset, step)) # verzamel de resultaten in een list

        validBords = []
        for child in childs: # voor elk resultaat
            if child[0]: # als de child een vol bord heeft
                for bords in child[1]:
                    validBords.append(bords)

        if len(validBords) > 0: # als de node een child had met een valide bord
            return (True, validBords)
        return (False, [])
    return (True, [bordset])

# test()
# opdrA()
opdrB()

