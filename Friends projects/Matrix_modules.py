def list_to_matrix(lst, cols):
    matrix = []
    element = 0
    if cols == 1:
        for x in range(0, 1):
            for row_no in range(0, cols):
                matrix.append([])
                while element < len(lst):
                    matrix[row_no].append(lst[element])
                    element += 1
                    if len(matrix[row_no]) == cols:
                        break
    else:
        for row_no in range(0, cols):
            matrix.append([])
            while element < len(lst):
                matrix[row_no].append(lst[element])
                element += 1
                if len(matrix[row_no]) == cols:
                    break
    return matrix


def column_lister(matrix):
    cols = len(matrix[0])
    lstele = []
    for colno in range(0, cols):
        for element in matrix:
            elementB = element[colno]
            lstele.append(elementB)
    return lstele


def plf(matrix):
    plf = []
    for row in matrix:
        for element in row:
            plf.append(element)
    return plf


def multiplicator(A, B):
    rowsA = len(A)
    rowsB = len(B)
    colsA = len(A[0])
    colsB = len(B[0])
    pdt = []
    pdt_list = []
    row = []
    column = []
    row_no = 0
    col_no = 0
    while row_no < rowsA*colsA:
        for elementA in range(0, colsA):
            row.append(plf(A)[elementA+row_no])
        while col_no < rowsB*colsB:
            for elementB in range(0, rowsB):
                column.append(column_lister(B)[elementB+col_no])
            for element in range(0, len(row)):
                pdt.append(row[element]*column[element])
            pdt_list.append(sum(pdt))
            col_no += rowsB
            column = []
            pdt = []
        col_no = 0
        row_no += colsA
        row = []
    pdt_matrix = list_to_matrix(pdt_list, colsB)
    return pdt_matrix


def scalar_multi(A, c):
    cols = len(A[0])
    pdt = plf(A) * c
    pdt_matrix = list_to_matrix(pdt, cols)
    return pdt_matrix


def add_or_sub(A, B, op):
    colsA = len(A[0])
    element = 0
    final = []
    leng = len(plf(A))
    for row in range(0, colsA):
        final.append([])
        if op == 1:
            while element < leng:
                final[row].append(plf(A)[element]+plf(B)[element])
                element += 1
                if len(final[row]) % colsA == 0:
                    break
        if op == 2:
            while element < leng:
                final[row].append(plf(A)[element]-plf(B)[element])
                element += 1
                if len(final[row]) % colsA == 0:
                    break
    return final
