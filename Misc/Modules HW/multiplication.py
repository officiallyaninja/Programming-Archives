import copy


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
