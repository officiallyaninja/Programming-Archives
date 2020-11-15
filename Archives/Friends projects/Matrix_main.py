from Matrix_modules import *
op = int(input('Type 1 for Addition, 2 for Subtraction, 3 for Scalar Multiplication and 4 for Matrix multiplication:'))
m1 = [[]]
m2 = [[]]


try:
    m1 = list(eval(input('Enter the elements in matrix A separated by commas:')))
except TypeError:
    eleA = int(input("So that's a 1x1 matrix huh? Type that for me again plz:"))
    m1[0].append(eleA)
    A = list(m1)
    matA = True
else:
    A = list_to_matrix(m1, colsA)
    matA = False
rowsA = int(input('Enter rows in matrix A:'))
colsA = int(input('Enter columns in matrix A:'))
if op == 3:
    c = int(input("Enter integer to be multiplied with the matrix:"))
else:
    try:
        m2 = list(eval(input('Enter the elements in matrix B separated by commas:')))
    except TypeError:
        eleB = int(input("So that's a 1x1 matrix huh? Type that for me again plz:"))
        m2[0].append(eleB)
        B = list(m2)
        matB = True
    else:
        B = list_to_matrix(m2, colsB)
    rowsB = int(input('Enter rows in matrix B:'))
    colsB = int(input('Enter columns in matrix B:'))
    matB = False
if op == 1:
    print(add_or_sub(A, B, op))
elif op == 2:
    print(add_or_sub(A, B, op))
elif op == 3:
    print(scalar_multi(A, c))
elif op == 4:
    print(multiplicator(A, B))
