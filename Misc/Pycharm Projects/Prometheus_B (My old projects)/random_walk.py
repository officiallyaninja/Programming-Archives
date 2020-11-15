import random
pos = [0, 0]
inc = 0
choice = 0
i = 0
freq = 10000
while True:
    x = random.randint(0, 3)
    if x == 0:
        pos[0] += 1
    elif x == 1:
        pos[0] += -1
    elif x == 2:
        pos[1] += 1
    elif x == 3:
        pos[1] += -1
    if pos == [0, 0]:
        inc += 1
    print(pos)
