#!/usr/bin/env python3

import sys

import time

from random import random

from random import uniform

from statistics import mean

def yang_func(X, E):
    sum = 0
    for i in range(5):
        sum += E[i] * (abs(X[i])**(i+1))

    return sum

def random_velocity(arguments):
    seed = mean(arguments)
    helper = []
    for _ in range(len(arguments)):
        helper.append(random()*seed)

    return helper

def create_swarm(size, first, E):
    swarm = []

    # X, best X, Y, v
    helper = []
    helper.append(first)
    helper.append(first)
    helper.append(yang_func(first, E))
    helper.append(random_velocity(first))

    swarm.append(helper)
    for i in range(size):
        helper = []
        if min(first) != max(first):
            helper.append([uniform(min(first), max(first)) for _ in range(5)])
        else:
            helper.append([uniform((min(first) - 1), max(first)) for _ in range(5)])

        helper.append(helper[0])
        helper.append(yang_func(helper[0], E))
        helper.append(random_velocity(helper[0]))
        swarm.append(helper)

    return swarm


def check_if_end(swarm):
    last = swarm[0][0]
    same = True
    stopped = True
    for bee in swarm:
        # sprawdzany jest przypadek gdy osobniki sie pokryja
        if bee[0] != last and same == True:
            same = False
        # sprawdzany jest przypadek gdy predkosc wszystkich osobnikow jest 0
        if bee[3] != 0 and stopped == True:
            stopped = False

        if stopped == False and same == False:
            return False

        last = bee[0]

    return True

def minimalize(params, time_max):
    E = params[5:]
    result = params[:5]
    swarm = create_swarm(20, result, E)
    minimum = swarm[0][2]
    max_fail = 20
    fail = 0

    # wspolczynnik hamowania
    inhibit = 0.4
    # beta
    local_res = 2
    # eta
    global_res = 2

    rem_time = 0

    clk_start = time.process_time()
    while time_max > rem_time:

        # sprawdzany jest warunek koncowy
        if check_if_end(swarm):
            break

        for bee in swarm:
            # liczymy wartosc dla obecnego polozenia osobnika
            val = yang_func(bee[0], E)
            # jezeli val jest mniejsza niż minimum tego osobnika
            if val < bee[2]:
                fail = 0
                global_res = 2
                local_res = 2
                bee[2] = val
                bee[1] = bee[0].copy()
                # jezeli val jest mniejsza niz minimum globalne
                if val < minimum:
                    minimum = val
                    result = bee[1].copy()
            else:
                fail += 1

            if fail >= max_fail:
                global_res = 4
                local_res = 1

        for bee in swarm:
            for i in range(len(bee[0])):
                # dla kazdego osobnika z niezerowa predkoscia w danym wymiarze
                if bee[3][i] != 0:
                    # nowa predkosc w danym wymiarze
                    bee[3][i] = (inhibit * bee[3][i] + uniform(0, local_res)*(bee[1][i] - bee[0][i])
                              + uniform(0, global_res)*(result[i] - bee[0][i]))
                    # zmiana danej wspolrzednej
                    bee[0][i] += bee[3][i]

        if inhibit > 0.2:
            inhibit -= 0.0001

        sys.stderr.write((str(minimum) + '\n'))
        clk_tick =  time.process_time()
        rem_time = clk_tick - clk_start

    return result + [minimum]


def main():
    time = 0
    args = sys.stdin.readline().strip()
    args = args.split()

    if len(args) < 5:
        sys.stderr.write("Arguments are required!\n")
    else:
        try:
            for i in range(5):
                args[i+1] = float(args[i+1])
                args[i+6] = float(args[i+6])

            time = int(args[0])
        except ValueError:
            sys.stderr.write("Wrong args!\n")
            return


        result = minimalize(args[1:], time)
        for i in range(len(result)):
            print(result[i], end=' ')
        print()




if __name__ == "__main__":
    main()
