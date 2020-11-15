A = [[10,3],
     [2,1]]
B = [[5,6],
     [7,4]]
X = []
Sum = []
for a in A:
    X.append(a)
y = 0
while y<len(X):
        b = B[y]
        x = X[y]
        row1 = [x[0]+b[0],x[1]+b[1]]
        Sum.append(row1)
        y+=1
print(Sum)
        

