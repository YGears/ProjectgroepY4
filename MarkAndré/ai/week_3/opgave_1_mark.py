import itertools

floors = [0, 1, 2, 3, 4]

for (L, M, N, E, J) in list(itertools.permutations(floors)):
    # Loes woont niet op de bovenste verdieping
    if L != 4:
        continue
    # Marja woont niet op de begane grond
    if M != 0:
        continue
    # Niels woont niet op de begane grond en niet op de bovenste verdieping
    if N != 0 or N != 4:
        continue
    # Erik woont (tenminste één verdieping) hoger dan Marja
    if E > M:
        continue
    # Joep woont niet op een verdieping één hoger of lager dan Niels
    if J > (N + 1) or J < (N - 1):
        continue
    # Niels woont niet op een verdieping één hoger of lager dan Marja
    if N > (M + 1) or N < (M - 1):
        continue

names = ("Loes", "Marja", "Niels", "Erik", "Joep")
floor_level = (L, M, N, E, J)
dict_result = dict(zip(names, floor_level))
result = dict_result.items()

for k, v in result:
    print("{} woont op verdieping {}".format(k, v))




