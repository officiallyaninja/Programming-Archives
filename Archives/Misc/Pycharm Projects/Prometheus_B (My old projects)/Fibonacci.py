
num_terms = 100

i = 0
j = 1
k = 1
N = 1
for N in range(num_terms):
    print(k)
    k = i + j
    i = j
    j = k
    N = N + 1
