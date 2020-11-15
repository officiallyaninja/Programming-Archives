# Determinants

M1 = [[3,10],
    [2,-1]]

def determ(M):
    import copy

    m = len(M)
    n = len(M[0])


    if m == 1:
        return M[0][0] # m=n=0

    else:
        count = 0
        R = 0

        for j in range(0,n):
            a = M[0][j]

            if count%2 != 0 :
                a = -a
            else:
                pass

            delM = copy.deepcopy(M)
            delM.pop(0)
            for x in range (0,len(delM)):
                del delM[x][j]

            R += a * determ(delM)
            count += 1

    return(R)

print(determ(M1))
