import math

import matplotlib.pyplot as plt
import numpy as np
import sympy as sym

linear = lambda x: -3 * x + 5
modulo = lambda x: abs(x)
polynomial = [3, 1, 2, -3]
trig = lambda x: math.cos(2 * x)


def convert_tab_to_fun():
    result = 0
    x = sym.symbols('x')
    for i in range(len(polynomial)):
        result += polynomial[i] * (x ** (len(polynomial) - i - 1))
    return result


def show_plot(fun_type, lagrange_fun, actual_fun, nodes):
    x_vals = np.linspace(min(nodes), max(nodes), 100)
    if fun_type == convert_tab_to_fun():
        y_actual = [actual_fun.subs(sym.symbols('x'), x_val) for x_val in x_vals]
        plt.scatter(nodes, [actual_fun.subs(sym.symbols('x'), node) for node in nodes], color='red',
                    label='Interpolation Nodes')
    else:
        y_actual = [actual_fun(x_val) for x_val in x_vals]
        plt.scatter(nodes, [actual_fun(node) for node in nodes], color='red',
                    label='Interpolation Nodes')

    y_lagrange = [lagrange_fun.subs(sym.symbols('x'), x_val) for x_val in x_vals]
    plt.plot(x_vals, y_actual, label='Actual Function')
    plt.plot(x_vals, y_lagrange, label='Lagrange Polynomial', linestyle='--')

    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.grid(True)
    plt.show()


def t_var(nodes):
    x = sym.symbols('x')
    distance = nodes[1] - nodes[0]
    return (x - nodes[0]) / distance  # zmienna t ktora potem wymnozymy przez interpolated by z t uzyskac x


def calculate_fun_value(fun, nodes):
    result = [0.0 for _ in range(len(nodes))]
    for i in range(len(nodes)):
        result[i] = fun(nodes[i])
    return result


def calculate_whole_horner(tab, nodes):
    values = [0.0 for _ in range(len(nodes))]
    for i in range(len(nodes)):
        values[i] = calculate_by_horner(tab, nodes[i])
    return values


def calculate_by_horner(tab, arg):
    result = tab[0]
    for i in range(1, len(tab)):
        result = (result * arg) + tab[i]
    return result


def substitute(yaxis, node):  # wylicza koncowy wielomian lagranga po podstawieniu x za t
    fun = calculate_lagrange(yaxis, node)
    return sym.simplify(fun.subs(sym.symbols('t'), t_var(node)))


def calculate_lagrange(y, x_tab):  # wylicza wielomian lagranga dla zmiennej t
    t = sym.symbols("t")
    temp = 1
    f = 0
    result = [0.0 for _ in range(len(x_tab))]
    summ = 1.0
    for j in range(len(x_tab)):
        for i in range(len(x_tab)):
            if j != i:
                summ *= j - i
                temp *= t - i
        result[j] = y[j] / summ
        temp *= result[j]
        f += temp
        temp = 1
        summ = 1.0
    return sym.simplify(f)


def get_nodes(a, b, number_of_nodes):  # zwraca wezly interpolacyjne rownych odleglosci
    nodes = [0.0 for _ in range(number_of_nodes)]
    distance = abs(b - a) / (number_of_nodes + 1)
    if b < a:
        temp = b
    else:
        temp = a

    for i in range(number_of_nodes):
        nodes[i] = temp + distance
        temp += distance
    return nodes


def get_user_arg(arg, y_value, nodes):
    return substitute(y_value, nodes).subs(sym.symbols('x'), arg)


def main():
    print("podaj funkcję: l, m, p, t")
    choose = input()
    match choose:
        case 'l':
            choose = linear
        case 'm':
            choose = modulo
        case 'p':
            choose = polynomial
        case 't':
            choose = trig

    print("podaj poczatek przedzialu: ")
    a = float(input())
    print("podaj koniec przedzialu: ")
    b = float(input())
    print("podaj ilosc wezlow: ")
    number = int(input())

    print("Podaj argument dla którego zostanie obliczona wartość funkcji")
    arg = float(input())

    nodes = get_nodes(a, b, number)
    if choose == polynomial:
        y_values = calculate_whole_horner(polynomial, nodes)
        choose = convert_tab_to_fun()
    else:
        y_values = calculate_fun_value(choose, nodes)
    print("obliczony wielomian lagranga: " + "\n")
    print(substitute(y_values, nodes))
    print("Obliczona wartość w podanym punkcie wynosi: " + "\n")
    print(get_user_arg(arg, y_values, nodes))

    show_plot(choose, substitute(y_values, nodes), choose, nodes)


main()
