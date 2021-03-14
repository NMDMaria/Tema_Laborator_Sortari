import time
import random
import sys
sys.setrecursionlimit(10**8)



def Bubble(N, Max, L): # O(n^2)
    # N = 10^3 - aprox 0.1 max
    # N = 10^4 - aprox 10 max
    # N = 10^5 - // too much
    """ Pentru fiecare iteratie a for-ului parinte stim ca ultimele i elemente sunt deja sortate
         din modul de functionare a algoritmului (vezi powerpoint) asa ca pt fiecare iteratie
         a for-ului copil putem sa scapam de i comparatii
     Daca pentru o iteratie a for-ului copil niciun element nu isi schimba locul sortarea
         poate fi considerata terminata deoarece inseamna ca sortarea a fost terminata anterior"""

    for i in range(N):
        did_i_swap = False
        for j in range(N - i - 1):  # pt ca accesam ultimul element oricum prin j+1
            if L[j] > L[j + 1]:
                L[j + 1], L[j] = L[j], L[j + 1]
                did_i_swap = True
        if not did_i_swap:
            break
    return L


def Count(N, Max, L): # O(n+k)
    """
    Optimizam memoria prin a declara vectorul counter doar pt nr din intervalul minim, maxim
    in loc de toate numere de la 0 la Max
    Algoritmul este problematic pt int cu aprox. Max >= 4*10^6 -> prea multa memorie ocupata
    """
    minim = min(L) # O(n) - python documentation
    maxim = max(L) # O(n) - python documentation
    counter = [0] * (maxim - minim + 1)# pt a salva memorie, nu avem nevoie de vector pt elemente care nu apar in input
    for i in range(N):
        counter[L[i] - minim] += 1
    index = 0
    for nr in range(minim, (maxim + 1)):
        for j in range(counter[nr - minim]):
            L[index] = nr
            index = index + 1
    return L


def Merge(N, Max, L): # O(nlogn)
    def merge(t, st, mij, dr):  # O(n) n = nr de elemente intre st si dr
        # interclasare din acelasi vector doar ca pointeri capete diferiti
        i = st
        j = mij + 1
        aux = []
        while i <= mij and j <= dr:
            if t[i] <= t[j]:
                aux.append(t[i])
                i += 1
            else:
                aux.append(t[j])
                j += 1
        aux.extend(t[i:mij + 1])
        aux.extend(t[j:dr + 1])
        t[st:dr + 1] = aux[:]

    def sort(t, st, dr):
        if dr - st >= 1:
            mij = (dr + st) // 2
            sort(t, st, mij)
            sort(t, mij + 1, dr)
            if t[mij] > t[mij + 1]: # pt a evita interclasari inutile
                # daca ultimul el din jum stanga e mai mic decat primul element din jum dreapta
                # inseamna ca ambele jumatati sunt sortate corect -> nu mai e nevoie de interclasare
                merge(t, st, mij, dr)

    sort(L, 0, N - 1)
    return L


def NaturalMerge(N, Max, L): # O(nlogn) but slightly better
    def interclasare(t, st, mij, dr):  # O(n) n = nr de elemente intre st si dr
        i = st
        j = mij
        aux = []
        while i < mij and j < dr:
            if t[i] <= t[j]:
                aux.append(t[i])
                i += 1
            else:
                aux.append(t[j])
                j += 1
        aux.extend(t[i:mij])
        aux.extend(t[j:dr])
        return aux

    output = [0] * N
    idx_grupari = [0]
    nr_grupari_sortate = 0
    for i in range(1, N + 1):
        if i == N or L[i - 1] > L[i]:
            nr_grupari_sortate += 1
            idx_grupari.append(i) # aici se termina o prima subsecv cresc

    while nr_grupari_sortate > 1:
        new = 0
        for i in range(0, nr_grupari_sortate - 1, 2):
            output[idx_grupari[i]: idx_grupari[i + 2]] = interclasare(L, idx_grupari[i], idx_grupari[i + 1], idx_grupari[i + 2])
            idx_grupari[new] = idx_grupari[i] # am combinat 2 grupari sortate -> scap de una din index
            new += 1
        if nr_grupari_sortate % 2 == 1:
            last = idx_grupari[nr_grupari_sortate - 1]
            output[last:N] = L[last:N]
            idx_grupari[new] = idx_grupari[nr_grupari_sortate - 1]
            new += 1
            # gruparea fara pereche am considerat-o "merged" cu nimic deci se poate scoate
        idx_grupari[new] = N # tot timpul ultima secv cresc se termina pe N - 1
        nr_grupari_sortate = new
        L = output
    return L


def Radix(N, Max, L): # O(nlgMax)
    def countingSort(N, L, base, exp, minim):
        # punem in galeti doar cate elemente cu % base = index
        galeata = [0] * base
        output = [0] * N
        index = 0
        for i in range(N):
            index = ((L[i] - minim) // exp) % base # cifra la care ne uitam -> scadem minim
            galeata[index] += 1
        for i in range(1, base):
            galeata[i] += galeata[i - 1]
        for i in range(N - 1, -1, -1):
            index = ((L[i] - minim) // exp) % base
            output[galeata[index] - 1] = L[i]
            galeata[index] -= 1
        return output

    base = 10
    minim = min(L) # n
    maxim = max(L) # n
    exp = 1
    while (maxim - minim) // exp >= 1:
        L = countingSort(N, L, base, exp, minim)
        exp *= base
    return L


def Radix2(N, Max, L): # O(nlog2(Max))
    def bucketSort(N, L, base, exp, minim):
        galeata = {i: [] for i in range(base)}
        output = []
        for i in range(N):
            index = (L[i] >> exp) & 1
            galeata[index].append(L[i])
        for b in range(base):
            k = len(galeata[b])
            for i in range(k):
                output.append(galeata[b][i])
        return output

    base = 2
    minim = min(L)
    exp = 0
    while (Max - minim) >> exp >= 1: ## lungimea avarage
        L = bucketSort(N, L, base, exp, minim)
        exp += 1
    return L


def QuickMediana5(N, Max, L):
    def BFPRT(N, A):  # mediana de 5 ocupa mult spatiu
        if N <= 5:
            A.sort()
            return A[N//2]

        grupuri = [sorted(A[i: i + 5]) for i in range(0, len(A), 5)]
        mediane = [grup[len(grup) // 2] for grup in grupuri]

        return BFPRT(len(mediane), mediane)

    def partition(L, st, dr, med):
        for i in range(st, dr + 1): # O(k)
            if L[i] == med:
                L[i], L[dr] = L[dr], L[i]
                break
        i = st
        for j in range(st, dr): # O(k)
            if L[j] <= med:
                L[i], L[j] = L[j], L[i]
                i += 1
        L[i], L[dr] = L[dr], L[i]
        return i

    def quickSort(L, st, dr):
        if st < dr:
            med = BFPRT(dr - st + 1, L[st: dr + 1])
            q = partition(L, st, dr, med)
            quickSort(L, st, q - 1)
            quickSort(L, q + 1, dr)

    quickSort(L, 0, N - 1)
    return L


def QuickRandom(N, Max, L):
    def partition(L, st, dr, med):
        for i in range(st, dr + 1):
            if L[i] == med:
                L[i], L[dr] = L[dr], L[i]
                break
        i = st
        for j in range(st, dr):
            if L[j] <= med:
                L[i], L[j] = L[j], L[i]
                i += 1
        L[i], L[dr] = L[dr], L[i]
        return i

    def quickSort(L, st, dr):
        if st < dr:
            med = L[random.randint(st, dr)]
            q = partition(L, st, dr, med)
            quickSort(L, st, q - 1)
            quickSort(L, q + 1, dr)

    quickSort(L, 0, N - 1)
    return L


def QuickDreapta(N, Max, L): # worst case O(n^2)
    def partition(L, st, dr, med):
        for i in range(st, dr + 1):
            if L[i] == med:
                L[i], L[dr] = L[dr], L[i]
                break
        i = st
        for j in range(st, dr):
            if L[j] <= med:
                L[i], L[j] = L[j], L[i]
                i += 1
        L[i], L[dr] = L[dr], L[i]
        return i

    def quickSort(L, st, dr):
        if st < dr:
            med = L[dr]
            q = partition(L, st, dr, med)
            quickSort(L, st, q - 1)
            quickSort(L, q + 1, dr)

    quickSort(L, 0, N - 1)
    return L


def SanityCheck(N, L):
    for i in range(1, N):
        if L[i - 1] > L[i]:
            return -1
    return 0


def generated():
    f = open("teste")
    sorts = [Bubble, Count, Merge, NaturalMerge, Radix, Radix2, QuickMediana5, QuickRandom, QuickDreapta]
    testcount = 0
    for test in f:
        testcount += 1
        print("{} {}".format(testcount, '--' * 20))
        print(test.strip())
        N = int(test.strip().split()[0].split("=")[1])
        Max = int(test.strip().split()[1].split("=")[1])
        L = [random.randint(0, Max + 1) for i in range(N)]
        copy_sorted = []
        copy_sorted.extend(L)
        start_time = time.time()
        copy_sorted.sort()
        end_time = time.time()
        print(f"Default sort in python --- Timsort O(nlogn) takes: {end_time - start_time} s")
        for sort in sorts:
            copy = []
            copy.extend(L)
            if N >= 100000 and sort is Bubble:
                print("Bubble sort merge foarte greu pentru mai mult de 10^5 numere")
            elif N >= 10000000 and (sort is QuickMediana5 or sort is QuickRandom or sort is QuickDreapta):
                print(f"{sort.__name__} genereaza in Python Maximum recursion depth error")
            else:
                start_time = time.time()
                copy = sort(N, Max, copy)
                end_time = time.time()
                if SanityCheck(N, copy) == 0:
                    print("sorted ok", end=" ")
                print(f"{sort.__name__} {end_time - start_time} s")


def list_sorted():
    L = [i for i in range(1000000)]
    return L
def list_munte():
    st = [i for i in range(1000)]
    st.append(1000)
    dr = [i for i in range(999, 0, -1)]
    st.extend(dr)
    return st
def list_OneElementMultipleTimes():
    elem = random.randint(0, 10000000)
    L = [elem for i in range(100000)]
    return L
def list_BigNumbers():
    L = [random.randint(10, 40000000) for i in range(1000000)]
    return L
def list_SmallNumbers():
    L = [random.randint(0, 100000) for i in range(1000000)]
    return L

def teste_date():
    sorts = [Bubble, Count, Merge, NaturalMerge, Radix, Radix2, QuickMediana5, QuickRandom, QuickDreapta]
    generators = [list_OneElementMultipleTimes, list_BigNumbers, list_SmallNumbers]
    testcount = 0
    for test in generators:
        testcount += 1
        print("{} {}".format(testcount, '--' * 20))
        L = test()
        N = len(L)
        Max = max(L)
        print('N=', N, ' ', 'Max=', Max, ' ', test.__name__, sep='')
        copy_sorted = []
        copy_sorted.extend(L)
        start_time = time.time()
        copy_sorted.sort()
        end_time = time.time()
        print(f"Default sort in python --- Timsort O(nlogn) takes: {end_time - start_time} s")
        for sort in sorts:
            copy = []
            copy.extend(L)
            if N >= 100000 and sort is Bubble and (test != list_sorted and test != list_munte and test != list_OneElementMultipleTimes):
                print("Bubble sort merge foarte greu pentru mai mult de 10^5 numere")
            elif ((test == list_sorted or test == list_munte) and sort is QuickDreapta) or (test == list_OneElementMultipleTimes and "Quick" in sort.__name__ ):
                print(f"{sort.__name__} pe {test.__name__} genereaza recursion depth error")
            else:
                start_time = time.time()
                copy = sort(N, Max, copy)
                end_time = time.time()
                if SanityCheck(N, copy) == 0:
                    print("sorted ok", end=" ")
                print(f"{sort.__name__} {end_time - start_time} s")


option = int(input("1 = teste generate random dupa N si Max, 2 = teste alese\n"))
if option == 1:
    generated()
elif option == 2:
    teste_date()