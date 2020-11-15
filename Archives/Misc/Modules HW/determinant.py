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
