def null_matrix(m, n):
    null_mat = []
    for i in range(0, m):
        null_mat.append([])
        for j in range(0, n):
            null_mat[i].append(0)
    return null_mat


def transpose(m):
    m2 = null_matrix(len(m[0]), len(m))
    for i in range(0, len(m)):
        for j in range(0, len(m[0])):
            m2[j][i] = m[i][j]
    return(m2)
