import copy

M1 = [[12, 10, 6],
      [32, 1, 6],
      [12, 0, 6]]
m1 = len(M1)
n1 = len(M1[0])


M2 = [[40, 12, 19],
      [12, 40, 33],
      [12, 0, 6]]
m2 = len(M2)
n2 = len(M2[0])

# Addition

if m1 == m2 and n1 == n2:
    sum_M1_M2 = copy.deepcopy(M1)
    for i in range(0, m1):
        for j in range(0, n1):
            sum_M1_M2[i][j] += M2[i][j]
else:
    sum_M1_M2 = ["Not Valid"]

for x in sum_M1_M2:
    print(x)

print("="*10)

# Difference

if m1 == m2 and n1 == n2:
    diff_M1_M2 = copy.deepcopy(M1)
    for i in range(0, m1):
        for j in range(0, n1):
            diff_M1_M2[i][j] = (M1[i][j])-(M2[i][j])
else:
    diff_M1_M2 = ["Not Valid"]

for x in diff_M1_M2:
    print(x)

print("="*10)

# Multiplication

if n1 == m2:
    M = []
    for x in range(0, m1):
        M.append([])

    for i1 in range(0, m1):
        for j2 in range(0, n2):
            count = 0
            if count % n2 == 0:
                sume = 0
            else:
                pass
            for j1 in range(0, n1):
                sume += M1[i1][j1]*M2[j1][j2]
                count += 1
            M[i1].append(sume)
else:
    M = ["Not Valid"]

for x in M:
    print(x)

print("="*10)

# Transpose

M = []
for x in range(0, n1):
    M.append([])
for i in range(0, n1):
    for z in range(0, m1):
        M[i].append(M1[z][i])
for x in M:
    print(x)

print("="*10)

#
