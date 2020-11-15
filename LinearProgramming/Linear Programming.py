import numpy as np
from itertools import combinations
import os


def vector(array: str):
    array = array.replace(' ', '')
    array = array.replace('(', '')
    array = array.replace(')', '')
    array = array.split(',')
    array = [float(i) for i in array]
    row_vector = np.array(array)
    return np.transpose(row_vector)


print('enter coefficient just as a list of numbers seperated by commas')
print('eg: 5x + 3.5y - z becomes 5,5.5,-1')
z_string = input('enter coefficient of Z function: ')
z_vector = vector(z_string)

dimensions = len(z_vector)
z = lambda x: z_vector.dot(x)

inequalities = []  # will be a list of lambda functions
equations = {}  # will be in the form (coefficients of LHS): RHS


error_message = ''
def add_constraint(inequality: str) -> None:
    global error_message
    # eg of inequality -> "1,2,3<100" corresponds to x+2y+3z <= 100
    inequality = inequality.replace('=','')
    inequality = inequality.replace(' ', '')
    inequality = inequality.replace(')', '')
    inequality = inequality.replace('(', '')

    error_message = 'no < or > in expression'
    assert '<' in inequality or '>' in inequality
    error_message = '< AND > in expression'
    assert not ('<' in inequality and '>' in inequality)

    symbol = '<' if '<' in inequality else '>'

    index = inequality.index(symbol)
    coefficients = vector(inequality[0: index])
    RHS = float(inequality[index+1:])

    error_message = 'dimensions in Z != dimensions in constraint'
    assert len(coefficients) == dimensions

    error_margin = 0.000000000000001
    
    if symbol == '<':
        inequalities.append(lambda x: coefficients.dot(x) <= RHS + error_margin)
    elif symbol == '>':
        inequalities.append(lambda x: coefficients.dot(x) >= RHS - error_margin)

    equations[tuple(coefficients)] = RHS

non_negativity = input('should all the parameters of this problem be non-negative/positive?(y/n): ')
if non_negativity == 'y':
    non_negative_constraints = np.identity(dimensions)
    for row in non_negative_constraints:
        add_constraint(str(tuple(row)) + '>0')


user_input = '  '
while user_input != '':
    user_input = input('add constraint: ')
    try:
        add_constraint(user_input)
    except AssertionError:
        if user_input != '':
            print('ERROR: ' + error_message)
else:
    pass
intersection_points = []


for combination in combinations(equations.keys(),dimensions):
    matrix = []
    vector = []  # dependent values vector
    for coefficient_list in combination:
        matrix.append(coefficient_list)
        vector.append(equations[coefficient_list])
    matrix = np.array(matrix)
    vector = np.transpose(np.array(vector))

    try:
        point = np.linalg.solve(matrix,vector)
        intersection_points.append(point)
    except np.linalg.LinAlgError:
        pass

feasible_points = []

for point in intersection_points:

    for inequality in inequalities:
        if not inequality(point):
            break
    else:
        feasible_points.append(point)


maxZ = None
max_points = []
minZ = None
min_points = []

for point in feasible_points:
    Z = z(point)
    if maxZ is None or Z > maxZ:
        maxZ = Z
        max_points = [point]

    elif Z == maxZ:
        max_points.append(point)

    if minZ is None or Z < minZ:
        minZ = Z
        min_points = [point]

    elif Z == minZ:
        min_points.append(point)

if len(feasible_points) == 0:
    print('There are no possible solutions to these constraints')
else:

    print('max value is', f"\033[93m{maxZ}\033[0m", 'at point(s)')
    for point in max_points:
        print(f'\033[94m{(tuple(point))}\033[0m')

    print('min value is',  f"\033[91m{minZ}\033[0m", 'at point(s)')
    for point in min_points:
        print(f'\033[96m{(tuple(point))}\033[0m')

input('press enter to quit: ')
