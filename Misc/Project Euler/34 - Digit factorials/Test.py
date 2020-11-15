import math
import time

fact = []
for i in range(0, 10):
    fact.append(math.factorial(i))


def digit_factorial(n):
    sum = 0

    for digit in str(n):
        x = fact[int(digit)]

        sum += x

    return sum


n = 1
i = 3
while True:
    if i == digit_factorial(i):
        print(i)
    i += 1
    if i % 1_000_000 == 0:
        print(n, "million")
        n += 1
