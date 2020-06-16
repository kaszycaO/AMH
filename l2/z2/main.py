#!/usr/bin/env python3

import sys

import time

import random

from random import randint

import numpy as np

VALUES = [0, 32, 64, 128, 160, 192, 223, 255]

def copy_matrix(matrix):
    copy = [[matrix[i][j] for j in range(len(matrix[0]))] for i in range(len(matrix))]
    return copy

def print_matrix(matrix, n, m):
    for i in range(n):
        for j in range(m):
            print(matrix[i][j], end = " ")
        print("")

    print("")

def distance(n, m, matrix_A, matrix_B):
    sub = 0
    for i in range(n):
        for j in range(m):
            sub += (matrix_A[i][j] - matrix_B[i][j])**2

    return 1/(n*m) * sub

def get_start(n, m, k):
    """ Rozwiazanie startowe: macierz zbudowana na przemian z 0 i 255"""
    result = []

    values = []
    val = -1
    # inicjalizacja pierwszych wartosci wierszy
    for i in range(n):
        if i % k == 0 and (n - i) // k != 0:
            if val == 0:
                val = 255
            else:
                val = 0
        helper = [None]*m
        helper[0] = val
        values.append(helper)

    # uzupelnianie wierszy odpowiednia wartoscia
    for i in range(n):
        val = values[i][0]
        for j in range(1, m):
            #zmien wartosc co k, w przypadku gdy m % k != 0, powieksz blok
            if j % k == 0 and (m - j)//k != 0:
                if val == 0:
                    val = 255
                else:
                    val = 0
            values[i][j] = val

    return values

def get_blocks(result_matrix, n, m, k):
    """ Wydzielenie blokow z macierzy poczatkowej """
    blocks = []
    divider = []
    val = -1
    # podzial wierszy wzgledem wartosci
    for i in range(n):
        val = result_matrix[i][0]
        helper = []
        for j in range(0, m):
            if result_matrix[i][j] != val:
                divider.append(helper)
                helper = []
                val = result_matrix[i][j]

            helper.append([i, j])
        divider.append(helper)

    remove = []
    counter = 0
    previous = 0
    # dopasowanie wartosci z dividera i uformowanie blokow
    while counter < len(divider):
        helper = []
        if divider[counter] == None:
            counter += 1
            continue
        for i in range(k + 1):
            if i == k:
                # m//k definiuje odstepy w dividerze pomiedzy wartosciami
                # jednego bloku
                next = counter + i * (m//k)
                if next < len(divider):
                    index_A = divider[next][0][0]
                    index_B = divider[next][0][1]
                    index_C = previous[0][0]
                    index_D = previous[0][1]
                    # przypadek kiedy m != k lub n != k
                    if (result_matrix[index_A][index_B] == result_matrix[index_C][index_D] and
                       len(divider[next]) == len(previous)):
                            helper += divider[next]
                            divider[next] = None
            else:
                next = counter + i * (m//k)
                if next < len(divider):
                    previous = divider[next]
                    helper += divider[next]
                    divider[next] = None
                else:
                    break

        counter += 1
        blocks.append(helper)

    return blocks

def probability(T, x, y):
    """Prawdopodobienstwo wybrania sasiada, gdy jest gorszym wynikiem"""
    np.seterr(all='ignore')
    helper = (y - x)/T
    res = np.exp(-1 * helper)
    return res

def change_box_val(result_matrix, blocks, block, new_val):
    """ Zmiana wartosci bloku """

    for num in blocks[block]:
        result_matrix[num[0]][num[1]] = new_val

def swap_boxes(result_matrix, blocks, block1, block2):
    """ Zamiana blokow miejscami """

    val_1 = get_box_value(result_matrix, blocks, block1)
    val_2 = get_box_value(result_matrix, blocks, block2)

    change_box_val(result_matrix, blocks, block1, val_2)
    change_box_val(result_matrix, blocks, block2, val_1)

def check_if_working(matrix, blocks):
    """ Aktualizuje dane w blokach """
    for i in range(len(blocks)):
        index_A = blocks[i][0][0]
        index_B = blocks[i][0][1]
        val = matrix[index_A][index_B]
        change_box_val(matrix, blocks, i, val)

def get_box_width(blocks, block):
    """ Funkcja zwracajaca szerokosc danego bloku """

    counter = 0
    val = 0
    for el in blocks[block]:
        if counter == 0:
            val = el[0]

        new = el[0]
        if new != val:
            break
        else:
            counter += 1

    return counter

def change_random_box_size(result_matrix, blocks, n, m, k):
    """ Losowe zmniejszenie blokow """

    matrix_copy = copy_matrix(result_matrix)
    result = []
    bigger = []
    # Poszukiwanie blokow mozliwych do zmniejszenia
    for i in range(len(blocks)):
        if len(blocks[i]) > k*k:
            bigger.append(i)

    # W przypadku braku takich blokow (np. macierz, gdzie m i n % k == 0) zakoncz
    if len(bigger) == 0:
        return
    else:
        get_rand = randint(0, len(bigger) - 1)
        box = bigger[get_rand]
        width = get_box_width(blocks, box)
        height = int(len(blocks[box])/width)
        elements = m//k
        box_size = len(blocks[box])

        # przypadek dla granicy gornej
        if box < elements:
            # lewy sasiad i jego dane
            left_box = box-1
            width_2 = get_box_width(blocks, left_box)
            height_2 = int(len(blocks[left_box])/width_2)

            # dolny sasiad i jego dane
            down_box = box + elements
            width_3 = get_box_width(blocks, down_box)
            height_3 = int(len(blocks[down_box])/width_3)

            # sprawdz czy blok nie lezy na granicy macierzy
            if height_2 == height and width > k and box % elements != 0:
                points = []
                # dodaj punkty do prawej strony lewego sasiada
                for i in range(height):
                    points.append(blocks[box][i*(width)])
                result.append([box, left_box, points, 'L'])
            else:
                return

        # przypadek dla granicy dolnej
        elif box >= elements**2 - elements:
            # lewy sasiad i jego dane
            left_box = box-1
            width_2 = get_box_width(blocks, left_box)
            height_2 = int(len(blocks[left_box])/width_2)

            # gorny sasiad i jego dane
            up_box = box - elements
            width_3 = get_box_width(blocks, up_box)
            height_3 = int(len(blocks[up_box])/width_3)

            # istnieje kompatybilny sasiad po lewej stronie
            if height_2 == height and width > k and box % elements != 0:
                points = []
                for i in range(height):
                    points.append(blocks[box][i*(width)])
                result.append([box, left_box, points, 'L'])

            # istnieje kompatybilny sasiad na gorze
            elif width_3 == width and height > k:
                points = []
                # dodaj punkty do dolu sasiada z gory
                for i in range(0, width):
                    points.append(blocks[box][i])
                result.append([box, up_box, points, 'U'])
            else:
                return
        # badanie punktu srodkowego
        else:
            # lewy sasiad
            left_box = box-1
            width_2 = get_box_width(blocks, left_box)
            height_2 = int(len(blocks[left_box])/width_2)

            # gorny sasiad
            up_box = box - elements
            width_3 = get_box_width(blocks, up_box)
            height_3 = int(len(blocks[up_box])/width_3)

            if height_2 == height and width > k:
                points = []
                for i in range(height):
                    points.append(blocks[box][i*(width)])
                result.append([box, left_box, points, 'L'])

            elif width_3 == width and height > k:
                points = []
                for i in range(0, width):
                    points.append(blocks[box][i])
                result.append([box, up_box, points, 'U'])
            else:
                return

    change_boxes(matrix_copy, blocks, result)

def change_boxes(matrix, blocks, arguments):
    """ Funkcja zapisujaca zmiany po zmianie wielkosci """

    source = arguments[0][0]
    update = arguments[0][1]
    points = arguments[0][2]
    type = arguments[0][3]

    # wybrany zostal sasiad znajdujacy sie nad
    if type == 'U':
        index_A = blocks[update][0][0]
        index_B = blocks[update][0][1]
        val = matrix[index_A][index_B]
        for point in points:
            blocks[update].append(point)
            blocks[source].remove(point)

        change_box_val(matrix, blocks, update, val)

    # wybrany zostal sasiad znadjdujacy sie po lewej
    if type == 'L':
        width = get_box_width(blocks, update)
        index_A = blocks[update][0][0]
        index_B = blocks[update][0][1]
        val = matrix[index_A][index_B]
        for i in range(1, len(points)+1):
            blocks[update].insert(i*width + (i-1), points[i-1])
            blocks[source].remove(points[i-1])

        change_box_val(matrix, blocks, update, val)

def get_box_value(result_matrix, blocks, block):
    """ Pobierz wartosc bloku """

    index_A = blocks[block][0][0]
    index_B = blocks[block][0][1]

    return result_matrix[index_A][index_B]

def find_neighbourhood(matrix, blocks, start, n, m, k, T):
    """ Funkcja odpowidzialna za szukanie sasiedztwa """

    result_matrix = copy_matrix(matrix)
    matrix_copy = copy_matrix(matrix)
    x = distance(n, m, start, matrix)

    value_result = []
    swap_result = []

    # modyfikacja wartosci w blokach
    for i in range(len(blocks)):
        val = random.choice(VALUES)
        matrix_copy = copy_matrix(matrix)

        change_box_val(matrix_copy, blocks, i, val)
        new_val = distance(n, m, start, matrix_copy)
        if new_val < x:
            result_matrix = copy_matrix(matrix_copy)
            x = new_val

    value_result = copy_matrix(result_matrix)
    matrix_copy = copy_matrix(result_matrix)

    # modyfikacja polozenia blokow
    for i in range(1, len(blocks)):
        box_A = randint(0, len(blocks)-i)
        box_B = randint(0, len(blocks)-i)

        if box_A != box_B:
            matrix_copy = copy_matrix(result_matrix)
            if len(blocks[box_A]) == len(blocks[box_B]):
                swap_boxes(matrix_copy, blocks, box_A, box_B)
                new_val = distance(n, m, start, matrix_copy)

                if new_val < x:
                    result_matrix = copy_matrix(matrix_copy)
                    x = new_val

    matrix_copy = copy_matrix(result_matrix)
    swap_result = copy_matrix(result_matrix)

    # zmiana rozmiaru blokow
    change_random_box_size(result_matrix, blocks, n, m, k)
    check_if_working(result_matrix, blocks)
    # zwracanie 3 potencjalnych sasiadow
    return [result_matrix, swap_result, value_result]

def find_matrix(n, m, block_size, time_max, basic_matrix):
    """ Wlasciwa funkcja minimalizujaca """

    result = get_start(n, m, block_size)
    blocks = get_blocks(result, n, m, block_size)
    best_val = distance(n, m, basic_matrix, result)
    start = best_val

    T = 10000
    reduction = 0.8
    rem_time = 0

    clk_start = time.process_time()
    while time_max > rem_time:
        if T == 0:
            break

        neighbour = find_neighbourhood(result, blocks, basic_matrix, n, m, block_size, T)
        for neigh in neighbour:
            new = distance(n, m, basic_matrix, neigh)

            if new < best_val:
                result =  copy_matrix(neigh)
                best_val = new
            else:
                if random.random() <= probability(T, best_val, new):
                    result = copy_matrix(neigh)
                    best_val = new

        T = T * reduction


        clk_tick =  time.process_time()
        rem_time = clk_tick - clk_start

    print("Initial: ", start)
    print("Final: ", best_val)
    print_matrix(result, n, m)


def main():
    args = sys.argv
    params = []
    time = 0
    args = sys.stdin.readline()
    args = args.split()
    time = int(args[0])
    n = int(args[1])
    m = int(args[2])
    k = int(args[3])

    for line in sys.stdin:
        line = line.split()
        row = []
        for num in line:
            row.append(int(num))

        if m != len(row) and len(row) != 0:
            print(row)
            print("Wrong args! ")
            return

        if len(row) != 0:
            params.append(row)

    if n != len(params):
        print("Wrong args! ")
        return

    result = find_matrix(n, m, k, time, params)

if __name__ == "__main__":
    main()
