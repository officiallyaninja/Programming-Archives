from math import *


def sqr(num):
    return num*num


def quad_solver_real(num1, num2, num3):
    result1 = ((float(num2) * -1) + sqrt((pow(float(num2), 2)) -
                                         (4 * float(num1) * float(num3)))) / 2 * float(num1)
    result2 = ((float(num2) * -1) - sqrt((pow(float(num2), 2)) -
                                         (4 * float(num1) * float(num3)))) / 2 * float(num1)

    return result1, result2


def quad_solver_imag(num1, num2, num3):

    real_part_1 = (float(num2) * -1) / 2 * float(num1)
    imag_part_1 = (sqrt(abs(sqr(float(num2)) - 4 * float(num1) * float(num3)))) / 2 * float(num1)

    return (str(real_part_1) + " + " + str(imag_part_1) + "i" + ", " + str(real_part_1) + " - " + str(imag_part_1) + "i")


def quad_solver(num1, num2, num3):

    if sqr(num2) - 4 * num1 * num3 >= 0:
        return quad_solver_real(num1, num2, num3)

    else:
        return (quad_solver_imag(num1, num2, num3))


num_a = input("Enter Number a:")
num_b = input("Enter Number b:")
num_c = input("Enter Number c:")
try:
    print(quad_solver(float(num_a), float(num_b), float(num_c)))
except ValueError:
    print("That's not a number you idiot")
