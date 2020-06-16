#!/usr/bin/env python3

import sys

import time

from random import randint

from random import random


directions = ['U', 'D', 'R', 'L']

def basic_path(maze, paths, start_pos, n, m, p, s):
    global directions
    population = []
    length = len(paths[0])
    max_fails = n*m

    for path in paths:
        population.append(path)
        if length < len(path):
            length = len(path)

    for i in range(p - s):
        helper = ""
        result = check_path(maze, helper, start_pos)
        fails = 0
        while result[0] == False:
            helper = ""
            for _ in range(length):
                helper += directions[randint(0,3)]

            result = check_path(maze, helper, start_pos)
            fails += 1
            if fails >= max_fails:
                result = check_path(maze, population[randint(0, s-1)], start_pos)

        population.append(result[2])

    return population



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

    return [end, leng, path[:leng]]

def find_path(maze, m, n, p, s, start_pos, paths, time_limit):
    """ Glowna funkcja minimalizujaca trase"""
    global directions
    tabu = []
    rem_time = 0
    population = basic_path(maze, paths, start_pos, n, m, p, s)
    road = min(population)

    # prawdopodobienstwo mutacji
    pm = 0.01

    clk_start = time.process_time()
    while rem_time < time_limit:

        new_paths = population.copy()
        for path in population:
            # jesli badana droga jest najkrotsza, nie modyfikuj jej
            if len(path) < len(road):
                road = path
                continue

            # nowy potomek
            new_path = path
            # usuniecie jednego kroku ze sciezki
            index = randint(0, (len(path) - 1))
            new_path = new_path[:index] + new_path[index+1:]

            # losowa mutacja
            if random() < pm:
                index = randint(0, (len(path) - 1))
                curr = path[index]
                mutation = curr
                while mutation == curr:
                    mutation = directions[randint(0, 3)]
                new_path = new_path[:index] + mutation + new_path[index+1:]

            # dodanie trasy do listy, jezeli jest prawidlowa
            result = check_path(maze, new_path, start_pos)
            if result[0] == True:
                new_paths.append(result[2])



        population = []
        counter = 0
        # ustalenie nowej populacji
        while counter < p:
            # wybierane sa najkrotsze trasy
            element = min(new_paths)
            population.append(element)
            new_paths.remove(element)
            counter += 1

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
    s = int(args[3])
    p = int(args[4])
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


    first_paths = params[len(params) - s:]
    params = params[:len(params) - s]

    if len(params) != n:
        sys.stderr.write("Wrong args! [check n]\n")
        return

    road = find_path(params, m, n, p, s, start_pos, first_paths, time)
    steps = len(road)

    print("Dlugosc: ", steps)
    for i in range(len(road)):
        sys.stderr.write(road[i])
    sys.stderr.write("\n")

if __name__ == "__main__":
    main()
