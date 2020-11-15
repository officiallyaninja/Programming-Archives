def Jmap(licht):  # Jumbled Mapper
    import random

    Jumbled = random.sample(licht, len(licht))

    Mapping = {}

    for x in range(0, len(licht)):
        Mapping[licht[x]] = Jumbled[x]

    return(Mapping)


num = list(range(0, 10+1))
operation = ["+", "-", "*", "/"]

Jnum = Jmap(num)
Joperation = Jmap(operation)


def Test():
    n1 = int(input("Enter number 1 : "))
    op = input("Enter operation : ")
    n2 = int(input("Enter number 2 : "))
    print("\nOutput is", eval(str(Jnum[n1])+str(Joperation[op])+str(Jnum[n2])))


def CheckN():
    K = int(input("Enter Number : "))
    V = int(input("Enter Guess : "))
    if V == Jnum.get(K):
        return(True)
    else:
        return(False)


def CheckO():
    K = input("Enter Number : ")
    V = input("Enter Guess : ")
    if V == Joperation.get(K):
        return(True)
    else:
        return(False)


Test()
x = CheckN()

print("Guess right") if x else print("Guess Wrong")


"""
# Test Platform
enter operation
eval string(value for n1 , op ,n2)
give output

option
make guess
or try operation

if make guess (ALL or percentage of numbers)
count--> tries
check if key=value if score ---> remove from checking list
        else -----> tries -1

    if tries = 0 >>end game

Save game option
    export current map to text file
    put a check save file option at beginin
        if save file Jnum and J map = from file
"""
