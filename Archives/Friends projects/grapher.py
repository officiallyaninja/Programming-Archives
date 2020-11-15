x=width = 25
licht = list(width * " ")
for i in range (1,(x+1)):
    licht[int(((x+1)/2)-1)] = ' ♦'
    if i == int((x+1)/2) :
        licht = list(width * "♦ ")
    for z in licht:
            print (z , end = "")
    print()
    licht = list(width * " ")
input()
