from transpose import null_matrix, transpose
from determinant import det, reduce


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
