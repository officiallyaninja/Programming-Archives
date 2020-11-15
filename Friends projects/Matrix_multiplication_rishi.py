A = [[1, 2, 3],
     [6, 3, 3],
     [4, 2, 1]]
B = [[4, 4, 3],
     [3, 2, 3],
     [1, 4, 2]]


def matrix_converter(A):  # unravles a matrix into a linear list
    lst = []
    for m in A:
        for f in m:
            lst.append(f)
    return lst


plf_A = matrix_converter(A)  # plf -> pure list form
plf_B = matrix_converter(B)


def no_of_rows(matrix):
    rows_no = len(matrix)
    return rows_no


def no_of_columns(matrix):
    cols_no = int(len(matrix_converter(matrix)) / len(matrix))
    return len(matrix[0])


def multiplier(A, B, plf_A, plf_B):
    rows_noA = no_of_rows(A)
    rows_noB = no_of_rows(B)
    cols_noA = no_of_columns(A)
    # print(cols_noA)
    cols_noB = no_of_columns(B)
    pdt = []
    pdtlist = []
    rows = []
    pdtmatrix = []
    b = 0
    x = 0
    z = 0
    d = 0
# 0 1 2
# 3 4 5
# 6 7 8
    for rowjumper in range(0, len(plf_A), cols_noA):
        # print(jumper)
        for rowbase in range(0, cols_noA):
            # print(base)
        num1 = plf_A[rowjumper+rowbase]
        # print(num1)
        for columnjumper in range(0, cols_noB):
            # print(columnjumper)
            for columnbase in range(0, len(plf_B), cols_noB):
                print(columnbase)
                num2 = plf_B[columnjumper+columnbase]
                # print(num2)


    # while x<(2*(int(len(plf_A)/len(B)))):
    #     #print(x)
    #     for m in range(0,int(len(plf_A)/len(B))):
    #         for a in range(0,int(len(plf_A)/len(A))):
    #             #print(a)
    #             #print(x)
    #             #print(m)
    #             #print(a+x)
    #             p1 = plf_A[a+x]
    #             #print(a+x)
    #             #print(p1)
    #             while b<(int(len(plf_B)/len(A)))**2:
    #                 print(b)
    #                 p2 = plf_B[b+m]
    #                 #print(p2)
    #                 pdt.append(p1*p2)
    #                 #print(b+m)
    #                 b += int(len(plf_B)/len(B))
    #                 break
    #         b = 0
    #         pdt = sum(pdt)
    #         #print(pdt)
    #         pdtlist.append(pdt)
    #         pdt = []
    #     x += cols_noA
    # print(pdtlist)
    # while d <(int(len(plf_A)/len(B))**2):
    #     #print(d)
    #     rows = []
    #     while z < (int(len(pdtlist)/rows_no)):
    #         #print(d)
    #         rows.append(pdtlist[z+d])
    #         #print(z+d)
    #         z += 1
    #     z = 0
    #     d += int(len(plf_A)/len(B))
    #     #print(rows)
    #     pdtmatrix.append(rows)
    # return(pdtmatrix)
print(multiplier(A, B, plf_A, plf_B))
