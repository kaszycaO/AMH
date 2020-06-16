#!/usr/bin/env python3

import sys

import math

import time

from random import random

import random as r

import numpy as np


def salomon(args):
    sum = 0
    pi = math.pi
    cos = math.cos

    for i in range(4):
        sum += args[i]**2
    return 1 - cos(2 * pi * math.sqrt(sum)) + 0.1 * math.sqrt(sum)

def neighbourhood(arg):
    """ Szukanie sasiedztwa """
    secure_random = r.SystemRandom()
    rad = secure_random.uniform(-0.5, 0.5)

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

def generate_start(min, max):
    """ Funkcja modyfikujaca argumenty przy poczatku petli"""
    result = []
    secure_random = r.SystemRandom()
    for i in range(4):
        val = secure_random.uniform(min, max)
        result.append(val)

    return result

def probability(T, x, y):
    """Prawdopodobienstwo wybrania sasiada, gdy jest gorszym wynikiem"""
    np.seterr(all='ignore')
    helper = (salomon(y) - salomon(x))/T
    res = np.exp(-1 * helper)
    return res

def min_function(args, time_max):

    val = salomon(args)
    minimum = val
    result = args.copy()

    T = 1000
    reduction = 0.75
    rem_time = 0

    clk_start = time.process_time()
    while time_max > rem_time:
        # Jezeli temperatura spadnie do zera, zakoncz
        if T == 0:
            break

        # Modyfikacja argumentow przy nowej iteracji
        result = generate_start(min(result), max(result))

        new_args = neighbourhood(result)
        for neighbour in new_args:
            new_val = salomon(neighbour)

            if new_val < minimum:
                result = neighbour.copy()
                minimum = new_val
            else:
                # Wybranie gorszego sasiada z odpowiednim prawdopodobienstwem
                if random() <= probability(T, result, neighbour):
                    result = neighbour.copy()
                    minimum = new_val

        # Obnizenie temperatury
        T = T * reduction
        clk_tick =  time.process_time()
        rem_time = clk_tick - clk_start

    return result + [minimum]

def main():
    time = 0
    args = sys.stdin.readline()
    args = args.split()

    if len(args) < 5:
        print("Arguments are required!")
    else:
        try:
            for i in range(len(args)):
                args[i] = int(args[i])

            time = args[0]
            result = min_function(args[1:], time)
            for i in range(len(result)):
                print(result[i], end=' ')
            print("")

        except ValueError:
            print("Invalid parameter! Integers are required!")

if __name__ == "__main__":
    main()
