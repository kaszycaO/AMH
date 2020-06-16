#!/usr/bin/env python3

import sys

import time

from random import randint


def basic_path(maze, start_pos):
    """ Pierwsza trasa: "po scianach" """
    path = []
    agent = start_pos.copy()
    escape = 1
    last_step = ""
    while escape != 8:
        if maze[agent[0]-1][agent[1]] == '8':
            path.append('U')
            escape = 8
        elif maze[agent[0]][agent[1] + 1] == '8':
            path.append('R')
            escape = 8

        elif maze[agent[0]][agent[1] - 1] == '8':
            path.append('L')
            escape = 8

        elif maze[agent[0]+1][agent[1]] == '8':
            path.append('D')
            escape = 8

        elif maze[agent[0]-1][agent[1]] == '0' and last_step != 'D':
            path.append('U')
            last_step = 'U'
            agent = [agent[0]-1, agent[1]]

        elif maze[agent[0]][agent[1] + 1] == '0' and last_step != 'L':
            path.append('R')
            last_step = 'R'
            agent = [agent[0], agent[1] + 1]

        elif maze[agent[0]+1][agent[1]] == '0' and last_step != 'U':
            path.append('D')
            last_step = 'D'
            agent = [agent[0]+1, agent[1]]

        elif maze[agent[0]][agent[1] - 1] == '0' and last_step != 'R':
            path.append('L')
            last_step = 'L'
            agent = [agent[0], agent[1]-1]



    return path

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

def two_swap(path, tabu):
    """ Swap losowych krokow - generowanie sasiedztwa """
    copy = path.copy()
    result = []
    counter = 0
    # sasiedztwo rozmiaru t - 1, t -> Tabu
    for i in range(len(path)):
        for j in range(i+1, len(path)):
            if counter > len(tabu):
                break
            else:
                new_i = randint(i, len(path)-1)
                new_j = randint(j, len(path)-1)
                copy[new_i], copy[new_j] = copy[new_j], copy[new_i]
                if copy not in tabu:
                    counter += 1
                    result.append(copy)

    return result

def find_path(maze, m, n, start_pos, time_limit):
    """ Glowna funkcja minimalizujaca trase"""
    tabu = []
    rem_time = 0
    tabu_limit = len(maze) //2
    road = basic_path(maze, start_pos)
    tabu.append(road)

    clk_start = time.process_time()
    while rem_time < time_limit:
        neighbor = two_swap(road, tabu)
        for el in neighbor:
            helper = check_path(maze, el, start_pos)
            if helper[0]:
                if helper[1] < len(road):
                    # obciecie dlugosci trasy
                    road = el[:helper[1]]
                    if len(tabu) >= tabu_limit:
                        tabu.pop(0)
                    tabu.append(road)

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
    print("Trasa: ", road)


if __name__ == "__main__":
    main()
