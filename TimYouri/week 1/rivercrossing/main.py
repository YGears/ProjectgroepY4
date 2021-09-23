stateRiver = ['FGCW', '']
illegalStates = ['WG', 'GC']
gameEnd = 0
lastLegalState = ['dr', 'dr']

visitedStates = []

def MoveTo(object):
  #if gameEnd == 0:
        if "F" in object:
            for x in object:
                if stateRiver[0].find(x) != -1:
                    stateRiver[0] = stateRiver[0].replace(x, '')
                    stateRiver[1] = stateRiver[1]+x

            if isEndState() == 1:
                print('You son of a bitch, you did it!')
                gameEnd = 1
                print(stateRiver)
                return

            if isIllegal() == 1:
                print("You cannot make move, MoveTo(" +object +"), it is illegal. game over")
                gameEnd = 1
                print('Your current state: ')
                print(stateRiver)
                print('Your last legal state: ')
                print()
                print(lastLegalState)
                print(illegalStates)
                return
            else:
                lastLegalState = stateRiver
            print(stateRiver)
        else:
            print("Moveto("+ object+ ") onmogelijk. Kan " + object + " niet verplaatsen zonder de boer.")

def MoveFrom(object):
    if "F" in object:
        for x in object:
            temp1 = stateRiver[0]
            temp2 = stateRiver[1]

            if temp2.find(x) != -1:
                stateRiver[1] = temp2.replace(x, '')
                stateRiver[0] = temp1+x
        print(stateRiver)

def isEndState():
    endstate = "FGCW"
    for x in endstate:
        if stateRiver[1].find(x) == -1:
            return 0
    return 1

def isIllegal():
    for x in illegalStates:
        if stateRiver[1].find(x) == -1:
            return 1
        if stateRiver[0].find(x) == -1:
            return 1


MoveTo("FWGC")
MoveTo("G")
MoveFrom("FWGC")
MoveTo("FW")