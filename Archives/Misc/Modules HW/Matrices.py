from addition import *
from determinant import *
from inverse import *
from multiplication import mult
from transpose import *


matrix1 = [
    [1, -1, 5],
    [-1, 1, 6],
    [1, -4, 8]]
matrix2 = [
    [4, 5, 8],
    [5, 2, 6],
    [9, 9, 12]]


def show(matrix):
    for row in matrix:
        print(row)


print('matrix1: ')
print('')
show(matrix1)
print('')
print('matrix2: ')
print('')
show(matrix2)
print('')

print("1: add")
print("2: determinant")
print("3: inverse")
print("4: multiplication")
print("5: transpose")
x = input('enter choice: ')

if x == '1':
    print('matrx1 + matrix2 =')
    show(add(matrix1, matrix2))
if x == '2':
    print('determinant of matrix1 is')
    show(det(matrix1))
    print('determinant of matrix2 is')
    show(det(matrix2))
if x == '3':
    print('inverse of matrix1 is')
    show(inverse(matrix1))
    print('inverse of matrix2 is')
    show(inverse(matrix2))
if x == '4':
    print('matrix1 * matrix2 = ')
    show(mult(matrix1, matrix2))
if x == '5':
    print('transpose of matrix1 is')
    show(transpose(matrix1))
    print('transpose of matrix2 is')
    show(transpose(matrix2))
input('thank you for using this program. \n press enter to exit')
