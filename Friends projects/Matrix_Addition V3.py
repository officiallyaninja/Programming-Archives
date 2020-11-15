A = [[10,3,3,5],
     [2,1,4,6],
     [12,5,5,3],
     [5,4,3,7]]
B = [[5,6,3,2],
     [7,4,8,5],
     [15,6,6,6],
     [2,4,7,2]]
row = []
Sum = []
for y in range(0,len(A)):
    a,b = A[y],B[y]
    for z in range(0,len(A)): 
        row.append(a[z]+b[z])
    Sum.append(row)
    row = []
print(Sum)
        

