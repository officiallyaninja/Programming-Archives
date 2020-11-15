import numpy as np
from itertools import combinations


def vector(array: str):
    array = array.replace(' ', '')
    array = array.replace('(', '')
    array = array.replace(')', '')
    array = array.split(',')
    array = [float(i) for i in array]
    row_vector = np.array(array)
    return np.transpose(row_vector)


inequalities = []  # will be a list of lambda functions
equations = {}  # will be in the form (coefficients of LHS): RHS
non_negativity = False
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

    if symbol == '<':
        inequalities.append(lambda x: coefficients.dot(x) <= RHS)
    elif symbol == '>':
        inequalities.append(lambda x: coefficients.dot(x) >= RHS)

    equations[tuple(coefficients)] = RHS

with open('constraints.txt', 'r') as file:
    z_vector = vector(file.readline())
    dimensions = len(z_vector)
    for line in file:
        add_constraint(line)




if non_negativity:
    non_negative_constraints = np.identity(dimensions)
    for row in non_negative_constraints:
        add_constraint(str(tuple(row)) + '>0')


dimensions = len(z_vector)
z = lambda x: z_vector.dot(x)

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

input('press enter to close: ')
