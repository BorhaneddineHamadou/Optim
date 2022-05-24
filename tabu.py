import time

items = []
capacity = 0

def tri_a(element):
    return element[0]/element[1]

def heuristique(k):

    items_copy = items.copy()
    items_copy.sort(reverse=True, key=k)
    result = 0
    n = len(items_copy)
    i = int(0)
    solution = [0]*n #les valeurs de x
    W = capacity

    while i < n:
        x = 0
        while W-items_copy[i][1] > 0:
            result += items_copy[i][0]
            W -= items_copy[i][1]
            x += 1

        solution[items_copy[i][2]] = x
        i += 1

    return solution

def genererVoisins(S):

    voisins = list()
    for i in range(0, len(S)):
        tmp_S = S.copy()
        tmp_S[i] += 1
        voisins.append(tmp_S)
        tmp_S = S.copy()
        if tmp_S[i] >= 1:
            tmp_S[i] -= 1
            voisins.append(tmp_S)

    return voisins

def F(S):
    profit = 0
    C = capacity
    for i in range(0, len(S)):
        profit += (items[i][0]*S[i])
        C -= (items[i][1]*S[i])
        if C < 0:
            return -1
    return profit

def recherche_tabou(Aspiration=False):
    #solution initial
    S0 = heuristique(tri_a)
    S_etoile = S0.copy()
    S = S0.copy()
    LT = list() #la liste tabou
    t = 20 # la taille de LT
    stop = False
    LT.append(S)
    nMax = 101222

    while not stop:
        S_etoile_ancienne = S_etoile.copy()
        voisins = genererVoisins(S)
        S_prime = []
        f_S_prime = 0
        #selectionner le meilleurs des voisins
        for S_p in voisins:
            f_S_p = F(S_p)

            if (S_p not in LT) and (f_S_p > f_S_prime):
                S_prime = S_p.copy()
                f_S_prime = f_S_p

            elif (Aspiration == True and f_S_p > F(S_etoile)):
                S_etoile = S_p.copy()

        if f_S_prime == 0:
            stop = True

        else:
            if F(S_prime) > F(S_etoile):
                S_etoile = S_prime.copy()
            S = S_prime.copy()
            if(len(LT) == t):
                LT.pop(0)
            LT.append(S_prime)
        if S_etoile_ancienne == S_etoile:
            nMax -= 1

        if nMax == 0:
            stop = True

    return S_etoile

def worker():
    global items
    global capacity
    file = open("testcases.txt", 'r')
    benefices = []
    for line in file:
        values = line.split()
        if len(values) == 0:
            continue
        else:
            if values[0] == "$1":
                capacity = int(values[-1])
            elif values[0] == "$2":
                benefices = values[1:]
            elif values[0] == "$3":
                values = values[1:]
                for i in range(0, len(benefices)):
                    items.append([int(benefices[i]), int(values[i]), i])
                S0 = heuristique(tri_a)
                print(F(S0))
                print("Solution S0 = " + str(S0))
                time_start = time.time()
                S_etoile = recherche_tabou(True)
                time_end = time.time()
                print("Solution S* = " + str(S_etoile))
                print(F(S_etoile))
                print(time_end - time_start)
worker()
