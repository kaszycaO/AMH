#!/usr/bin/env python3

import math as m

import sys

import time

import random


def happyCat(x):
    norm = 0
    sum = 0
    for i in range(4):
        norm += (x[i])**2

    for j in range(1, 5):
        arg = x[j-1]
        sum += arg


    return ((norm - 4)**(2))**(1/8) + 0.25*(0.5*norm + sum) + 0.5

def griewank(x):
    mul = 1
    sum = 0
    i = 1
    while i <= 4:
        arg = x[i-1]
        mul *= m.cos(arg/m.sqrt(i))
        sum += (arg**2/4000)
        i += 1
    return 1 + sum - mul

def get_random_args(min, max):
    x = []
    secure_random = random.SystemRandom()
    for i in range(4):
        x.append(secure_random.uniform(min, max))
    return x

def get_neighborhood(arg, rad):

    res = [[arg[0]+rad, arg[1], arg[2], arg[3]]]
    res += [[arg[0]-rad, arg[1], arg[2], arg[3]]]
    res += [[arg[0], arg[1]+rad, arg[2], arg[3]]]
    res += [[arg[0], arg[1]-rad, arg[2], arg[3]]]
    res += [[arg[0], arg[1], arg[2]+rad, arg[3]]]
    res += [[arg[0], arg[1], arg[2]-rad, arg[3]]]
    res += [[arg[0], arg[1], arg[2], arg[3]+rad]]
    res += [[arg[0], arg[1], arg[2], arg[3]-rad]]
    res += [[arg[0]+rad, arg[1]+rad, arg[2]+rad, arg[3]+rad]]
    res += [[arg[0]-rad, arg[1]-rad, arg[2]-rad, arg[3]-rad]]
    return res

def min_func(function, t, rad, x1, x2, radius_lim):
    rem_time = 0
    repeat = 0
    helper = []
    list_copy = get_random_args(x1, x2)
    val = function(list_copy)
    minimum = val
    radius = rad
    basic_rad = radius

    clk_start = time.process_time()
    while rem_time < t:

        # losowanie permutacji
        helper = get_random_args(min(list_copy), max(list_copy))

        if function(helper) < minimum:
            minimum = function(helper)
            list_copy = helper.copy()

        # szukanie sasiedztwa
        n = get_neighborhood(list_copy, radius)
        for i in n:
            val = function(i)
            # jesli znaleziona wartosc jest najmniejsza
            if minimum > val:
                repeat = 0
                minimum = val
                list_copy = i.copy()
            else:
                repeat +=1

        # jezeli znajdujemy sie w minimum lokalnym
        if repeat > 16 and radius > radius_lim:
            radius /= 4
            repeat = 0
        # jezeli udalo nam sie znalezc wartosc poszerzamy poszukiwania
        elif repeat < 8:
            radius = basic_rad
        elif radius > radius_lim:
            radius /= 2

        clk_tick =  time.process_time()
        rem_time = clk_tick - clk_start

    return list_copy + [minimum]

def main():
    time = 0
    func = -1
    args = sys.stdin.readline()
    args = args.split()

    if len(args) < 2:
        print("Arguments are required!")
    else:
        try:
            time = int(args[0])
            if args[1] == '0':
                print(min_func(happyCat, time, 5, -10, 10, 0.001))
            else:
                print(min_func(griewank, time, 0.1, -1, 1, 0.00001))
        except ValueError:
            print("Invalid parameter! Integers are required!")



if __name__ == "__main__":
    main()
