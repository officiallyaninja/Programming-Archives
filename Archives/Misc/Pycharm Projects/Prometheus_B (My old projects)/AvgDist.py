import math
import random
correct = 1
total =1
while True:
    sum = 0
    for a in range(0,2):
        card = random.randint(1,7)
        sum += card

    if sum > 12:
        correct +=1

    total +=1

    print(correct/total)