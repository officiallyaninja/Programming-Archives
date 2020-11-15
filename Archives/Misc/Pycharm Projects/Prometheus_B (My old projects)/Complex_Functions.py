from math import *


def comp_num_to_str(a):
    real_part = ""
    imag_part = ""

    if a[1] >= 0:
        if int(a[0]) == float(a[0]):
            real_part = int(a[0])
        else:
            real_part = float(a[0])

        if int(a[1]) == float(a[1]):
            imag_part = int(a[1])
        else:
            imag_part = float(a[1])

        return str(real_part) + "+" + str(imag_part) + "i"

    else:
        if int(a[0]) == float(a[0]):
            real_part = int(a[0])
        else:
            real_part = float(a[0])

        if int(a[1]) == float(a[1]):
            imag_part = int(a[1])
        else:
            imag_part = float(a[1])

        return str(real_part) + str(imag_part) + "i"


def comp_str_to_num(a):
    real_part = ""
    if not a[-1] == "i":
        return float(a)
    else:
        real_part = ""
        imag_part = ""
        for x in range(0, list.index(list(a), "+" or "-")):
            real_part = real_part + list(a)[x]

        for x in range(list.index(list(a), "+" or "-") + 1, len(list(a))-1):
            imag_part = imag_part + list(a)[x]

        return float(real_part), float(imag_part)


def comp_add(a, b):
    return a[0] + b[0], a[1] + b[1]


def comp_sub(a, b):
    return a[0] - b[0], a[1] - b[1]


def quad_solver_real(num1, num2, num3):
    result1 = ((float(num2) * -1) + sqrt((pow(float(num2), 2)) - (4 * float(num1) * float(num3)))) / 2 * float(num1)
    result2 = ((float(num2) * -1) - sqrt((pow(float(num2), 2)) - (4 * float(num1) * float(num3)))) / 2 * float(num1)

    return result1, result2

def quad_solver_imag(num1, num2, num3):

    real_part_1 = (float(num2) * -1) / 2 * float(num1)
    imag_part_1 = (sqrt(abs(((float(num2))*float(num2))-4*float(num1)*float(num3))))/2*float(num1)

    return (str(real_part_1) + " + " + str(imag_part_1) + "i" + ", " + str(real_part_1) + " - " + str(
        imag_part_1) + "i")

def quad_solver(num1, num2, num3):

    if ((num2) *(num2)) - 4 * num1 * num3 >= 0:
        return (quad_solver_real(num1, num2, num3))

    else:
        return (quad_solver_imag(num1, num2, num3))