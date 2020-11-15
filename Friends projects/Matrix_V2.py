import copy


def MAdd(M1, M2):

    m1 = len(M1)
    n1 = len(M1[0])
    m2 = len(M2)
    n2 = len(M2[0])     # m1,n1 and m2,n2 are orders of the matrix

    if m1 == m2 and n1 == n2:
        sume = copy.deepcopy(M1)        # Sume is a dummy variable to add the matrices
        for i in range(0, m1):
            for j in range(0, n1):
                sume[i][j] += M2[i][j]

        return(sume)

    else:
        return(None)


def MSub(M1, M2):

    m1 = len(M1)
    n1 = len(M1[0])
    m2 = len(M2)
    n2 = len(M2[0])

    if m1 == m2 and n1 == n2:
        sume = copy.deepcopy(M1)
        for i in range(0, m1):
            for j in range(0, n1):
                # The only difference from add function is this -ve increment
                sume[i][j] -= M2[i][j]

        return(sume)

    else:
        return(None)


def MMult(M1, M2):

    m1 = len(M1)
    n1 = len(M1[0])
    m2 = len(M2)
    n2 = len(M2[0])

    if n1 == m2:

        M = []
        for x in range(0, m1):
            M.append([])            # Creates Empty rows

        for i1 in range(0, m1):
            for j2 in range(0, n2):

                count = 0
                if count % n2 == 0:
                    sume = 0
                else:
                    pass                # Initializing for sume

                for j1 in range(0, n1):
                    sume += M1[i1][j1]*M2[j1][j2]
                    count += 1
                M[i1].append(sume)

        return(M)

    else:
        return(None)


def Mtrans(M1):

    m1 = len(M1)
    n1 = len(M1[0])

    M = []
    for x in range(0, n1):
        M.append([])

    for i in range(0, n1):
        for j in range(0, m1):
            M[i].append(M1[j][i])

    return(M)


def R_C_del(M, i, j):  # SUPPLIMENTARY
    # Deletes row i and coloumn j (zero indexing)

    delM = copy.deepcopy(M)
    delM.pop(i)
    for x in range(0, len(delM)):
        del delM[x][j]
    return(delM)


def determ(M):

    m = len(M)
    n = len(M[0])

    if m == n:

        if m == 1:
            return M[0][0]

        else:
            count = 0
            R = 0

            for j in range(0, n):
                a = M[0][j]

                if count % 2 != 0:  # odd th execution of loop
                    a = -a
                else:
                    pass

                R += a * determ(R_C_del(M, 0, j))  # R_C_del reduces the determinant
                count += 1

        return(R)

    else:
        return(None)


def cofactor(M):

    m = len(M)
    n = len(M[0])

    if m == n:
        dummy = copy.deepcopy(M)
        for i in range(0, m):
            for j in range(0, n):
                dummy[i][j] = determ(R_C_del(M, i, j))g*((-1)**(i+j))

        return(dummy)

    else:
        return(None)


M1 = [[1, 2], [3, 4]]

print(determ(M1))
