#!/usr/bin/env python3

import sys

import time


def calculate_path(route, cities):
    """ route - droga zapisana za pomoca indeksow miast """

    result = 0
    prev = 0
    for i in range(1, len(route)):
        result += cities[route[prev]][route[i]]
        prev += 1
    return result

def basic_path(lenght, cities):
    """ Algorytm zachlanny do znalezienia pierwszej trasy """

    result = [0]
    current = 0
    # dopoki sa jeszcze nieodwiedzone miasta
    while len(result) < lenght-2:
        best = -1
        distance = int(max(cities[current]))
        for i in range(0, lenght):
            # jezeli miasto nie zostalo jeszcze odwiedzone
            if i not in result:
                # znajdz najblizsze miasto
                if cities[current][i] != 0 and cities[current][i] < distance:
                    distance = cities[current][i]
                    best = i
        if best > 0:
            current = best
            result.append(current)
    # dodaj brakujace
    for i in range(1,lenght):
        if i not in result:
            result.append(i)
            current = i
    return result

def two_opt(path, tabu):
    """ Algorytm 2-opt """

    neigh = []
    for i in range(0, len(path) + 1):
        for k in range(i + 1, len(path) + 2):
            copy = path.copy()
            result = []
            helper = copy[i:k+1]
            helper.reverse()
            result += copy[:i]
            result += helper
            result += copy[k+1:]
            # czy wynik nie jest zakazany
            if result not in tabu:
                neigh.append(result)
    return neigh

def swap(path, cost, tabu, city):
    """Swap wartosci sciezki"""

    res = []
    for i in range(0, len(path)+1):
        for j in range(i + 1, len(path)):
            copy = path.copy()
            helper = copy[i]
            copy[i] = copy[j]
            copy[j] = helper
            val = calculate_path(copy + [copy[0]], city)
            if copy not in tabu and val < cost:
                res = copy
                return res


def minimalize(time_limit, city):
    """ Glowna funkcja minimalizujaca """

    rem_time = 0
    tabu_counter = 0
    tabu_limit = len(city)//2
    repeat = 0
    tabu = []
    last_working = []
    steps = basic_path(len(city), city)
    result = calculate_path(steps + [steps[0]], city)
    clk_start = time.process_time()
    while rem_time < time_limit:
        new_neigh = two_opt(steps, tabu)
        if len(new_neigh) > 0:
            for x in new_neigh:         # sprawdzanie sasiedztwa
                if x not in tabu:       # czy sasiad nie jest zakazany
                    val = calculate_path(x + [x[0]], city) # sprawdzanie kosztu
                    if val < result:
                        result = val
                        steps = x.copy()
                    else:
                        if tabu_counter > tabu_limit:
                            tabu.pop(0)
                            tabu_counter = 0
                        # jesli sprawdzony sasiad nie poprawil wyniku
                        tabu.append(x)
                        tabu_counter += 1
                        repeat += 1
        else:
            # przypadek minimum lokalnego
            res = swap(steps, result, tabu, city)
            if res != None:
                steps = res.copy()
                result = calculate_path(steps + [steps[0]], city)

        clk_tick = time.process_time()
        rem_time = clk_tick - clk_start

    return steps + [steps[0]] + [result]


def main():
    args = sys.argv
    params = []
    time = 0
    args = sys.stdin.readline()
    args = args.split()
    time = int(args[0])
    n = int(args[1])
    for line in sys.stdin:
        line = line.split()
        row = []
        for num in line:
            row.append(int(num))
        params.append(row)
    if n != len(params):
        print("Wrong args! ")
        return
    result = minimalize(time, params)
    print(result[-1])
    print("---------------------------------------------------------------------")
    print(result[:-1])


if __name__ == "__main__":
    main()
