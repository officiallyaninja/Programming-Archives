def count_boomerangs(lst):
    count = 0
    for i in range(len(lst) - 2):
        if lst[i] == lst[i+2] and lst[i] != lst[i+1]: count += 1

    return count