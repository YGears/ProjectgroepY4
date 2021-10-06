import math as math
import copy as copy

filter = {"L": 10000, "M": 1000, "N": 100, "E": 10, "J": 1}
flat = {"L": 0, "M": 0, "N": 0, "E": 0, "J": 0}
people = ["L","M","N","E","J"]

foundStates = []
step = 0
found = False
numbers = [0, 0, 0, 0, 0] # what do they mean?

def assignHomes(number):
    # for x in people:
    #     flat[x] = math.floor(number / filter[x]) % 5

    n5 = flat[people[4]] + 1
    n4 = flat[people[3]]
    n3 = flat[people[2]]
    n2 = flat[people[1]]
    n1 = flat[people[0]]

    if n5 == 5:
        n5 = 0
        n4 = flat[people[3]] + 1
        if n4 == 5:
            n4 = 0
            n3 = flat[people[2]] + 1
            if n3 == 5:
                n3 = 0
                n2 = flat[people[1]] + 1
                if n2 == 5:
                    n2 = 0
                    n1 = flat[people[0]] + 1

    flat[people[4]] = n5
    flat[people[3]] = n4
    flat[people[2]] = n3
    flat[people[1]] = n2
    flat[people[0]] = n1
    return n1

limit = 0
while limit != 5:
    step +=1
    possible = True

    limit = assignHomes(step)

    #placement resttrictions
    if flat["L"] == 4:# print("loes top level")
        possible = False
    if flat["M"] == 0:# print("Marja lowest level")
        possible = False
    if flat["N"] == 0 or flat["N"] == 4:# print("Niels lowest or top level")
        possible = False

    #relational restrrictions
    if flat["E"] - flat["M"] < 1:# print("erik below marja")
        possible = False
    if abs((flat["J"] - flat["N"])) == 1:# print("joe near niels")
        possible = False
    if abs((flat["N"] - flat["M"])) == 1:# print("niels near marja")
        possible = False

    for x in people: # if not same number
        for y in people:
            if flat[x] == flat[y] and not x == y:
                possible = False

    if possible:
        foundStates.append(copy.deepcopy(flat))

print(step)
for x in foundStates:
    print(x)