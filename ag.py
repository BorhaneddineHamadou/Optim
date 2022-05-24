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

def F(S):
    profit = 0
    C = capacity
    for i in range(0, len(S)):
        profit += (items[i][0]*S[i])
        C -= (items[i][1]*S[i])
        if C < 0:
            return -1
    return profit

def generer_population(nMax):

    population = list()

    S = heuristique(tri_a)

    population.append(S)

    iter = 1000
    while (len(population) < nMax) and (iter > 0):

        k = random.randint(0, len(population)-1)

        for i in range(0, len(S)):

            tmp_S = population[k].copy()
            tmp_S[i] += int(random.randint((min(1,tmp_S[i])), tmp_S[i]) / 2)
            if (len(population) < nMax):
                if tmp_S not in population:
                    population.append(tmp_S)

            tmp_S = population[k].copy()
            if (len(population) < nMax) and (tmp_S[i] >= 1):
                tmp_S[i] -= random.randint(min((1,tmp_S[i])), tmp_S[i])
                if(tmp_S not in population):
                    population.append(tmp_S)

            if len(population) == nMax:
                break
        iter -= 1

    return population

def selection(population, k):
    #selectionner k elements de la population selon la valeur de Fitness

    individus = list()

    f = [[F(population[i]),i] for i in range(0, len(population))]

    def tri_relation(element):
        return element[0]

    f.sort(reverse=True, key=tri_relation)

    for i in range(0, k):
        individus.append(population[f[i][1]])

    return individus

def croisement(parents, taille_population):

    Pc = 0.8 #taux de croisement

    fils = []

    stop = False

    taille_cromo = len(parents[0])

    individus = list()

    while len(individus) < taille_population:

        i = random.randint(0, len(parents)-1)

        j = random.randint(0, len(parents)-1)

        while j == i:
            j = random.randint(0, len(parents)-1)

        r = random.random()

        if r < Pc:
            continue

        parent1 = parents[i].copy()
        parent2 = parents[j].copy()

        #nous allons utiliser le croisement uniforme
        #generer un masque
        masque = random.randint(1, int((1 << taille_cromo)-1))

        for k in range(0, taille_cromo):

            if ((masque >> k) & 1) == 1:
                tmp = parent1[k]
                parent1[k] = parent2[k]
                parent2[k] = tmp

        individus.append(parent1)
        individus.append(parent2)

    return individus

def mutation(individus):

    taille_cromo = len(individus[0])

    for i in range(0, len(individus)):

        bit1 = random.randint(0, taille_cromo-1)
        bit2 = random.randint(0, taille_cromo-1)

        tmp = individus[i][bit1]
        individus[i][bit1] = individus[i][bit2]
        individus[i][bit2] = tmp

    return individus

def AG():

    stop = False
    taille_max_population = 20
    population = generer_population(taille_max_population)
    k = 10
    max_iter = 1000

    S = population[0]

    while not stop:

        ancienne_population = population
        parents = selection(population, k)
        nouvelle_generation = croisement(parents, len(population))
        mutants = mutation(nouvelle_generation)
        population = selection(mutants, k)

        if F(S) < F(population[0]):
            S = population[0]

        if (population == ancienne_population) or (max_iter == 0):
            stop = True

    return S

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
                S_etoile = AG()
                AG()
                time_end = time.time()
                print("Solution S* = " + str(S_etoile))
                print(F(S_etoile))
                print(time_end - time_start)
worker()
