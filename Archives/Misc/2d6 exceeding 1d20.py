import random

def twoD6():
    return random.randint(1,6) + random.randint(1,6)

def oneD20():
    return random.randint(1,20)


for i in range(0,100):
    successes = 0
    size = 1_000_000
    for i in range(0,size):
        if twoD6() > oneD20():
            successes += 1

    print(successes/size)
