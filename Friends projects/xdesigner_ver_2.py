x = 11
while True:
    for i in range(1,13+1):
        y = list(' '*13)
        if 13-i > i :
                y[i:13-i:1] = '='*len(y[i:13-i])
        if 13-i < i :
            y[13-i+1:i] = '='*(len(y[13-i:i])-1)
        y[i-1]=y[-i]='♦'
        for z in y:
            print(z,end='')
        print()
