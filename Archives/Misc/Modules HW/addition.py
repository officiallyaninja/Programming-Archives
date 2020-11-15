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
