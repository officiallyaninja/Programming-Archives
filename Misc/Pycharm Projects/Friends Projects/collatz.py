def col(x, steps=0):
    runtime = 0
    for a in range(0,steps):
        if x == 1:
            pass
        else:
            if x%2 == 0:
                return col(x/2)
            else:
                return col(3*x+1)

    return None
