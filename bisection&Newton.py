import sympy as sp
import numpy as np
from matplotlib import pyplot as plt
import random

x = sp.symbols('x')

pol = [-1,3,5,-9,1]
trig = (sp.sin(0.5 * x)) ** 3
exp = 3 ** x - 9


def show_plot(string, x1, x2):
    plt.figure(figsize=(12, 8))
    args = np.linspace(x1, x2, 100)
    if string == "w":
        args = np.linspace(0,5,100)
    plt.plot(args, calculate_value(string, args), '-', color='red')
    plt.axhline(0, color='black', linewidth=.5)
    plt.axvline(0, color='black', linewidth=.5)
    plt.show()


def tangent(string, x1, x2, it, ep):
    if not is_root(calculate_value(string, x1), calculate_value(string, x2)):
        raise ValueError("W podanym przedziale nie ma miejsca zerowego")
    else:
        while True:
            x_rand = random.uniform(x1, x2)  # random float
            it -= 1
            if it == 0:
                return x_rand
            else:
                f_value = calculate_value(string, x_rand)
                der_value = calculate_derivative_value(string, x_rand)
                temp = x_rand
                x_rand -= f_value / der_value
                if abs(temp - x_rand) < ep:
                    return x_rand


def bisection(string, x1, x2, ep, it):
    if not is_root(calculate_value(string, x1), calculate_value(string, x2)):
        raise ValueError("W podanym przedziale nie ma miejsca zerowego")
    else:
        iterations = it
        while True:
            iterations -= 1
            middle = (x1 + x2) / 2
            if abs(x1 - middle) < ep:
                return middle
            else:
                if is_root(calculate_value(string, x1), calculate_value(string, middle)):
                    x2 = middle
                else:
                    x1 = middle
            if iterations == 0:
                return middle


def calculate_value(string, arg):
    if string == 'w':
        return calculate_by_horner(pol, arg)
    elif string == 't':
        return trigo(arg)
    elif string == 'e':
        return expo(arg)


def calculate_derivative_value(string, arg):
    if string == 'w':
        return calculate_by_horner(derivative_pol(), arg)
    elif string == 't':
        dif = trig.diff(x)
        return dif.evalf(subs={x: arg})
    elif string == 'e':
        dif = exp.diff(x)
        return dif.evalf(subs={x: arg})


def calculate_by_horner(tab, arg):
    result = tab[0]
    for i in range(1, len(tab)):
        result = (result * arg) + tab[i]
    return result


def derivative_pol():
    tab_der = [0 for _ in range(len(pol) - 1)]
    for i in range(len(tab_der)):
        tab_der[i] = pol[i] * (len(tab_der) - i)
    return tab_der


def is_root(value1, value2):
    if value1 * value2 < 0:
        return True
    else:
        return False


def get_x():
    print("Podaj argument x rozpatrywanego przedziału: ")
    arg = float(input())
    return arg


def trigo(arg):
    return np.sin(0.5 * arg) ** 3


def expo(arg):
    return 3 ** arg - 9


def finalize(choose, ep, it):
    x1 = get_x()
    x2 = get_x()
    print("bisekcja: " + "\n")
    print(bisection(choose, x1, x2, ep, it))
    print("\n" + "styczne: " + "\n")
    print(tangent(choose, x1, x2, it, ep))
    show_plot(choose, x1, x2)


def main():
    ep = 0.0
    it = 0
    print("Proszę wybrać funkcję [ wielomian - w | trygonometryczna - t | wykładnicza - e ]: ")
    choose = input()
    print("Proszę wybrać warunek stopu [ liczba iteracji - i | osiągnięcie epsilon - e ]: ")
    stop = input()
    if stop == 'i':
        print("Proszę podać liczbę iteracji: ")
        it = int(input())
        ep = -0.1
    elif stop == 'e':
        print("Proszę podać wartość epsilon: ")
        ep = float(input())
        it = -1
    if choose == 'w':
        finalize(choose, ep, it)
    elif choose == 't':
        finalize(choose, ep, it)
    elif choose == 'e':
        finalize(choose, ep, it)


main()
