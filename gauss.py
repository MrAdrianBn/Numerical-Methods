import math
import random


def read():
    with open('matrix.txt', 'r') as f:
        matrix = [[float(num) for num in line.split(',')] for line in f]
    return matrix


result = [0.0 for _ in range(len(read()))]


def shuffle_rows(matrix):
    first_row = random.randint(0, len(matrix) - 1)
    second_row = random.randint(0, len(matrix) - 1)
    while first_row == second_row:
        second_row = random.randint(0, len(matrix) - 1)
    temp_row = matrix[first_row]
    matrix[first_row] = matrix[second_row]
    matrix[second_row] = temp_row
    return matrix


def triangular_matrix(matrix, ep):
    for i in range(len(matrix) - 1):
        for j in range(i + 1, len(matrix)):
            if matrix[i][i] == 0:
                return False
            m = matrix[j][i] / matrix[i][i]
            for k in range(i, len(matrix) + 1):
                matrix[j][k] -= (matrix[i][k] * m)
    if abs(matrix[len(matrix) - 1][len(matrix) - 1]) < ep and abs(matrix[len(matrix) - 1][len(matrix)]) < ep:
        print("UKŁAD NIEOZNACZONY")
        #exit(0)
        return
    elif abs(matrix[len(matrix) - 1][len(matrix) - 1]) < ep and (matrix[len(matrix) - 1][len(matrix)] != 0 or abs(matrix[len(matrix) - 1][len(matrix)]) < ep):
        print("UKŁAD SPRZECZNY")
        #exit(0)
        return
    return matrix


def calculate_results(matrix):
    result[len(matrix) - 1] = matrix[len(matrix) - 1][len(matrix)] / matrix[len(matrix) - 1][len(matrix) - 1]  #
    index = 0  # NIEOZNACZONY DZIELI PRZEZ 0 BO 0=0 W OSTATNIM WIERSZU
    # PRZY SPRZECZNYM JEST TEZ DZIELENIE PRZEZ 0 TYLKO ZE WYSTEPUJE 0 = COS
    for i in range(len(matrix) - 2, -1, -1):  # i = 1
        temp = 0
        for j in range(len(matrix) - 1, i, -1):  # j = 2
            if j == len(matrix) - 1:
                temp = matrix[i][len(matrix)] - (matrix[i][j] * result[j])  # temp = 25 - 6.33 * x3
            else:
                temp += -1 * matrix[i][j] * result[j]  # temp = 12 - 1 * x3 + (-3 * x2)
            index = j
        temp /= matrix[i][index - 1]
        result[i] = temp
    return result


def print_matrix(matrix):
    for i in range(len(matrix)):
        print(matrix[i])


def solve(matrix):
    counter = 0
    if triangular_matrix(matrix, 0.00001) is None:
        return
    while not triangular_matrix(matrix, 0.00001):
        matrix = shuffle_rows(matrix)
        counter += 1
        if counter == math.factorial(len(matrix)):  # jesli wszystkie mozliwe zamiany wierszy nic nie wniosly to danej macierzy nie mozna rozwiazac (naszym sposobem)
            raise ValueError("Nie można rozwiązać tego układu równań")
    return calculate_results(triangular_matrix(matrix, 0.000001))


# triangular_matrix(read(), 0.0001)

def main():
    flag = True
    while flag:
        print("Podaj operacje:\n"
              "c - rozwiąż układ równań z pliku\n"
              "x - zakończ działanie programu")
        char = input()
        match char:
            case "c":
                print("Rozwiązanie tego układu to :" + str(solve(read())))
            case "x":
                flag = False
            case _:
                print("Podaj poprawną opcje")


main()

# print(solve(read()))