#!/usr/bin/env python3

import sys

import time

from random import randint

from random import random

import numpy as np

from collections import deque


def basic_path(maze, start_pos):
    """ Pierwsza trasa """
    start_x = start_pos[0]
    start_y = start_pos[1]


    # odwiedzone pola
    visited = [[False for j in range(len(maze[i]))] for i in range(len(maze))]
    visited[start_x][start_y] = True

    # kolejka przechowujaca trase
    queue = deque()
    start = [start_x, start_y, []]
    queue.append(start)

    while len(queue) > 0:
        curr = queue.popleft()
        # trasa zostala znaleziona
        if maze[curr[0]][curr[1]] == "8":
            return curr[2]
        else:
            steps = [[-1, 0, "U"], [1, 0, "D"], [0, 1, "R"], [0, -1, "L"]]
            # poszukiwanie odpowiedniego sasiada
            for step in steps:
                x = curr[0] + step[0]
                y = curr[1] + step[1]
                if x > -1 and x < len(maze) and y > -1 and y < len(maze) and maze[x][y] != "1" and visited[x][y] == False:
                    path = curr[2].copy()
                    path.append(step[2])
                    queue.append([x, y, path])
                    visited[x][y] = True


    return -1

def check_path(maze, path, start_pos):
    """ Funkcja do sprawdzania poprawnosci trasy """
    x = start_pos[0]
    y = start_pos[1]
    end = False
    leng = 0
    copy = maze.copy()
    for i in range(len(path)):
        leng += 1
        if path[i] == 'U':
            x -= 1
        elif path[i] == 'D':
            x += 1
        elif path[i] == 'R':
            y += 1
        elif path[i] == 'L':
            y -=1

        if copy[x][y] == '8':
            end = True
            break

        if copy[x][y] == '1':
            break

    return [end, leng]

def two_swap(path):
    """ Swap losowych krokow - generowanie sasiedztwa """
    copy = path.copy()
    result = []
    for i in range(len(path)):
        for j in range(i+1, len(path)):
            new_i = randint(i, len(path)-1)
            new_j = randint(j, len(path)-1)
            copy[new_i], copy[new_j] = copy[new_j], copy[new_i]
            result.append(copy)

    return result

def probability(T, x, y):
    """Prawdopodobienstwo wybrania sasiada, gdy jest gorszym wynikiem"""
    
    np.seterr(all='ignore')
    helper = (y - x)/T
    res = np.exp(-1 * helper)
    return res

def find_path(maze, m, n, start_pos, time_limit):
    """ Glowna funkcja minimalizujaca trase"""
    tabu = []
    rem_time = 0
    road = basic_path(maze, start_pos)
    if road == -1:
        print("Sth went wrong! ")
        return[-2]


    T = 100
    reduction = 0.75

    clk_start = time.process_time()
    while rem_time < time_limit:
        if T == 0:
            break

        neighbor = two_swap(road)
        for el in neighbor:
            helper = check_path(maze, el, start_pos)
            if helper[0]:
                if helper[1] < len(road):
                    # obciecie dlugosci trasy
                    road = el[:helper[1]]
                else:

                    # wybor gorszego sasiada z odpowiednim prawdopodobienstwem
                    if random() <= probability(T, len(road), len(el[:helper[1]])):
                        road = el[:helper[1]]

        T = T * reduction

        clk_tick = time.process_time()
        rem_time = clk_tick - clk_start

    return road

def main():

    params = []
    args = sys.stdin.readline()
    args = args.split()
    start_pos = 0
    time = int(args[0])
    n = int(args[1])
    m = int(args[2])
    counter = 0
    for line in sys.stdin:
        line = line.split()
        row = ""
        for num in line:
            if '5' in num:
                start_pos = [counter, num.index('5')]
            row += num.strip()
            counter+=1
        params.append(row)

    if len(params) != n:
        print("Wrong args! [check n]")
        return

    road = find_path(params, m, n, start_pos, time)
    steps = len(road)

    print("Dlugosc: ", steps)
    for i in range(len(road)):
        print(road[i], end='')
    print("")

if __name__ == "__main__":
    main()
