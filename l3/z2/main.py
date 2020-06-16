#!/usr/bin/env python3

import sys

import time

from random import random
from random import randint

import hmap as h

DICT = None
LETTERS = []

def init_dict(filename):
    global DICT
    DICT = h.hmap(100)
    DICT.load(filename)

def init_letters(letters):
    global LETTERS
    LETTERS = letters.copy()

def get_input():
    letters = []
    weights = []
    words = []
    arguments = []
    args = sys.stdin.readline()
    args = args.split()
    start_pos = 0
    time = int(args[0])
    n = int(args[1])
    s = int(args[2])

    counter = 0
    try:
        for line in sys.stdin:
            line = line.strip().split()

            if counter < n:
                letters.append(line[0])
                weights.append(line[1])
            else:
                if len(line) == 1:
                    words.append(line[0])
                else:
                    raise IndexError

            counter += 1

    except IndexError:
        return -1

    arguments.append(time)
    arguments.append(letters)
    arguments.append(weights)
    arguments.append(words)

    return arguments

def get_points(letters, weights, word):
    """ Punktacja slow """
    points = 0
    for letter in word:
        index = letters.index(letter)
        points += int(weights[index])

    return points

def check_if_possible(word):
    """ Sprawdzenie czy wyraz jest w slowniku"""
    global DICT
    global LETTERS

    mult = LETTERS.copy()


    if DICT.find(word):
        for letter in word:
            if letter in mult:
                mult.remove(letter)
            else:
                return False

        return True

    else:
        return False


def recombination(population, word_A, word_B):
    """ Rekombinacja
        Return:
            - result_A: sklejenie 2. wyrazow, w losowych miejscach
            - result_B: sklejenie 2. wyrazow z dodatkowa wstawka z wyrazu A lub B
    """

    if randint(0, 1) == 1:
        helper = word_A
    else:
        helper = word_B

    index_A = randint(0, min(len(word_A), len(word_B))-1)
    index_B = randint(0, min(len(word_A), len(word_B))-1)

    result_A = word_A[:index_A] + word_B[index_A:]
    result_B = word_A[:index_A] + word_B[index_A:index_B] + helper[index_B:]

    return result_A, result_B

def generate_pairs(population):
    """ Tworzenie par, poprzez wybor losowych wyrazow (bez powtorzen) """

    indexes = [i for i in range(len(population))]
    pairs = []
    for i in range(len(population)//2):
        helper = []
        for _ in range(2):
            index = randint(0, len(indexes)-1)
            helper.append(population[index])
            indexes.pop(index)
            if len(indexes) == 0:
                break
        pairs.append(helper)

    return pairs

def mutation(new_word, letters, pm):
    """ Mutacja z podanym prawdopodobienstwem pm"""
    if random() < pm:
        index = randint(0, (len(new_word)-1))
        curr = new_word[index]
        mutation = curr
        while mutation == curr:
            mutation = letters[randint(0, (len(letters)-1))]
            new_word = new_word[:index] + mutation + new_word[index+1:]

    return new_word

def generate_words(time_max, letters, weights, words):
    """ Glowna funkcja maksymalizacji wyniku """

    init_letters(letters)
    population = [word for word in words]

    # najwieksza liczba punktow
    maximum = 0
    # wyraz z najwieksza liczba punktow
    result = ""
    # prawdopodobienstwo mutacji
    pm = 0.1
    # maksymalny rozmiar populacji, musi byc parzysty
    max_population = 200

    rem_time = 0
    counter = 0

    clk_start = time.process_time()
    while rem_time < time_max:

        # selekcja
        pairs = generate_pairs(population)

        for pair in pairs:
            for word in pair:
                # poszukiwanie slowa z najwieksza punktacja
                if check_if_possible(word):
                    points = get_points(letters, weights, word)
                    if points > maximum:
                        maximum = points
                        result = word

            # rekombinacja, powstaje 2 dzieci
            if(len(pair) == 2):
                new_word_A, new_word_B = recombination(population, pair[0], pair[1])

                # mutacja z okreslonym prawdopodobienstwem
                new_word_A = mutation(new_word_A, letters, pm)
                new_word_B = mutation(new_word_B, letters, pm)

                if new_word_A not in population:
                    population.append(new_word_A)

                if new_word_B not in population:
                    population.append(new_word_B)


        if len(population) > max_population:
            for word in population:
                if check_if_possible(word) == False:
                    population.remove(word)
            if len(population) > max_population:
                population = sorted(population, key=lambda word: get_points(letters, weights, word), reverse=True)
                population = population[:max_population]

        clk_tick = time.process_time()
        rem_time = clk_tick - clk_start

    return [result] + [maximum]

def main():
    init_dict("dict.txt")
    arguments = get_input()
    if arguments != -1:
        result = generate_words(arguments[0], arguments[1], arguments[2], arguments[3])
        print(result[1])
        sys.stderr.write((result[0] + "\n"))
    else:
        sys.stderr.write("Bad input!\n")

if __name__ == "__main__":
    main()
