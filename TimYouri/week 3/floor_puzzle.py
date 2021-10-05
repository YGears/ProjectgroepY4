import itertools

floors = [1,2,3,4,5]

for (L,M,N,E,J) in list(itertools.permutations(floors)):

    if L!=5:
        if M != 1:
            if N != 1 and N != 5:
                if E > M:
                    if J > (N+1) or J < (N-1):
                        if N > (M + 1) or N < (M - 1):
                            print("Loes woont op verdieping: " + str(L))
                            print("Marja woont op verdieping: " + str(M))
                            print("Niels woont op verdieping: " + str(N))
                            print("Erik woont op verdieping: " + str(E))
                            print("Joep woont op verdieping: " + str(J))

