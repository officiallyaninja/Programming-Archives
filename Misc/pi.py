from random import random


def random_coordinate() -> tuple:
    return random() - 0.5, random() - 0.5


def in_circle(point: tuple) -> bool:
    r = 0.5
    if point[0]*point[0] + point[1]*point[1] > r*r:
        return False
    else:
        return True

inside_count: int = 0
total_count: int = 0
while True:
    total_count += 1
    if in_circle(random_coordinate()):
        inside_count += 1

    ratio = inside_count/total_count
    print(f'{total_count} pi =', ratio*4)

