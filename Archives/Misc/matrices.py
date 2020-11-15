import copy

matrix1 = [
    [1, 2, 3],
    [2, 1, 2],
    [2, 2, 1]]
matrix2 = [
    [4],
    [5]]


p_mat = [[3, 8], [5, 9], [8, -6], [7, -2], [-5, 3], [-9, 5]]


def add(m1, m2):
    m3 = []
    for k in range(0, len(m1)):
        m3.append([])
        for l in range(0, len(m1[k])):
            m3[k].append(None)

    for i in range(0, len(m1)):
        for j in range(0, len(m1[i])):
            m3[i][j] = m1[i][j] + m2[i][j]
    return m3


def reduce(m, e):
    m_new = m.copy()
    for i in range(0, len(m)):
        m_new[i] = m[i].copy()
    for i in range(0, len(m_new)):
        for j in range(0, len(m_new[i])):
            if e[0] == i:
                m_new[i] = None
            elif e[1] == j:
                m_new[i][j] = None
    m_alt = []
    n = -1
    for k in range(0, len(m_new)):
        if m_new[k] is None:
            continue
        else:
            m_alt.append([])
            n += 1
        for l in range(0, len(m_new)):
            if m_new[k] is None:
                continue
            elif m_new[k][l] is None:
                continue
            else:
                m_alt[n].append(m[k][l])
    return(m_alt)


def det(m):
    if len(m) == 1:
        return m[0][0]
    else:
        determinant = 0
        for i in range(0, len(m)):
            minor = reduce(m, (0, i))
            determinant += m[0][i] * det(minor) * ((-1) ** i)
            # print('det:',determinant,'cofactor:',det(minor),'a:',m[0][i],'term:', m[0][i] * det(minor) * ((-1) ** i))

        return determinant


def null_matrix(m, n):
    null_mat = []
    for i in range(0, m):
        null_mat.append([])
        for j in range(0, n):
            null_mat[i].append(0)
    return null_mat


def mult(m1, m2):
    if isinstance(m1, float) or isinstance(m1, int):
        m3 = copy.deepcopy(m2)
        for i in range(0, len(m3)):
            for j in range(0, len(m3[0])):
                m3[i][j] *= m1
    else:
        m3 = null_matrix(len(m1), len(m2[0]))
        if len(m1[0]) != len(m2):
            return None
        else:
            pass

            for i in range(0, len(m3)):
                for j in range(0, len(m3[0])):
                    for k in range(0, len(m1[0])):
                        m3[i][j] += m1[i][k] * m2[k][j]

    return m3


def transpose(m):
    m2 = null_matrix(len(m[0]), len(m))
    for i in range(0, len(m)):
        for j in range(0, len(m[0])):
            m2[j][i] = m[i][j]
    return(m2)


def show_matrix(matrix):
    for row in matrix:
        print(row)


def cofactor_matrix(m):
    cofactor = null_matrix(len(m), len(m[0]))
    for i in range(len(m)):
        for j in range(len(m[0])):
            cofactor[i][j] = det(reduce(m, (i, j))) * ((-1) ** (i + j))
    return(cofactor)


def adjoint(M):
    return transpose(cofactor_matrix(M))


def inverse(M):
    if det(M) == 0:
        return None
    else:
        return mult((1 / det(M)), adjoint(M))


def solve(A, B):
    invert = inverse(A)
    if invert is None:
        return None
    else:
        return mult(invert, B)


def consistency(A, B):
    if det(A) != 0:
        print('consistent, unique solution')
        return True
    else:
        if mult(adjoint(A), B) == 0:
            print('consistent, infinite solutions')
            return True
        else:
            print('inconsistent')
            return False


def area_of_triangle(p1, p2, p3):
    q1, q2, q3 = list(p1), list(p2), list(p3)
    matrix = [q1, q2, q3]
    for row in matrix:
        row.append(1)
    return abs(det((matrix))) / 2


def find_eq_of_line(p1, p2):
    q1, q2 = list(p1), list(p2)
    q1.append(1)
    q2.append(1)
    matrix = [[1, 1, 1]]
    # this first row is for the general points x and y, but they are 1 and 1 because we only need the coefficients
    matrix.extend([q1, q2])
    cofac = cofactor_matrix(matrix)
    co_efficients = cofac[0].copy()
    # the first row of the cofactor matrix will contain, the coefficient of x,y and 1
    # coeffients list containt elements [a,b,c] such that ax+by+c = 0, and points p1 and p2 are solutions for this equation
    return co_efficients


def intersection(m1, m2):
    n1, n2 = copy.deepcopy(m1), copy.deepcopy(m2)
    co1, co2 = find_eq_of_line(n1[0], n1[1]), find_eq_of_line(n2[0], n2[1])
    coefficient_matrix = [
        [co1[0], co1[1]],
        [co2[0], co2[1]]
    ]
    c_matrix = [
        [-1 * co1[2]],
        [-1 * co2[2]]
    ]

    solution_matrix = solve(coefficient_matrix, c_matrix)
    if solution_matrix is None:
        return None
    x = solution_matrix[0][0]

    x1 = n1[0][0]
    x2 = n1[1][0]

    return x in range(x1, x2) or x in range(x2, x1)


def sort_points(m):
    n = copy.deepcopy(m)
    if intersection((m[0], m[1]), (m[2], m[3])):
        print(1)
        m = [n[0], n[2], n[1], n[3]]
    elif intersection((m[0], m[2]), (m[1], m[3])):
        print(2)
        m = [n[0], n[1], n[2], n[3]]
    elif intersection((n[0], n[3]), (n[1], n[2])):
        m = [n[0], n[1], n[3], n[2]]
    else:
        m = n
    return(m)


def area_of_quadrilateral(p1, p2, p3, p4):
    q = sort_points([p1, p2, p3, p4])
    return area_of_triangle(q[1], q[2], q[4]) + area_of_triangle(q[2], q[3], q[4])


def polynomial(points):
    coefficientMatrix = null_matrix(len(points), len(points))
    for i in range(0, len(coefficientMatrix)):
        for j in range(0, len(coefficientMatrix[0])):
            x = points[i][0]
            coefficientMatrix[i][j] = x**j
    y_matrix = [[]]
    for i in range(0, len(points)):
        y_matrix[0].append(points[i][1])
    y_matrix = transpose(y_matrix)

    solution_matrix = solve(coefficientMatrix, y_matrix)
    return transpose(solution_matrix)[0]


A = matrix1
term1 = mult(A, A)
term2 = mult(-4, A)
term3 = [[-5, 0, 0],
         [0, -5, 0],
         [0, 0, -5]]


def display(text, matrix):
    print(text, end='\n')
    for line in matrix:
        print(line)
    print()


A = [[1,2,1],
    [-1,1,2],
    [2,-1,1]]

print((det(adjoint(adjoint(A))))**(1/4))