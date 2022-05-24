import time
import random
import math

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

def recuit_simule():

    S0 = heuristique(tri_a)
    S_etoile = S0.copy()
    S = S0.copy()
    R = 100
    borne_inf_temperature = 1
    T = 10230
    alpha = .9
    stop = False

    while not stop:

        S_etoile_ancienne = S_etoile.copy()
        voisins = genererVoisins(S)
        #selectionner le meilleurs des voisins
        iter = R

        while iter > 0:

            i = random.randint(0, len(voisins)-1)
            S_prime = voisins[i]
            if(F(S_prime) >=  F(S)):
                S = S_prime
            else:
                r = random.random()
                Delta_F = F(S)-F(S_prime)
                if r < math.exp(-(Delta_F/T)):
                    S = S_prime

            if F(S) > F(S_etoile):
                S_etoile = S

            iter -= 1

        T = alpha*T
        if T <= borne_inf_temperature:
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
                S_etoile = recuit_simule()
                time_end = time.time()
                print("Solution S* = " + str(S_etoile))
                print(F(S_etoile))
                print(time_end - time_start)
worker()
