'''
import random

dimensions = 5
num_constraints = 40
file = open('constraints.txt', 'w')
list = []
for i in range(dimensions):
    list.append(random.randint(0, 100))
file.write(str(tuple(list)) + '\n')

for i in range(num_constraints):
    list = []
    for i in range(dimensions):
        list.append(random.randint(0,100))

    symbol = random.choice(['<','>'])
    file.write(str(tuple(list)) + f'{symbol}{random.randint(0,100)}' +'\n')


file.close()
'''




L1 = [100,900,300,400,500]
START = 1
SUM = 0
for C in range(START,4):
    SUM = SUM + L1[C]
    print(C, ':' ,SUM)
    SUM = SUM + L1[0]*10
    print(SUM)