def harmonic_sum(lst):
    reciprocal_sum = 0
    for num in lst:
        reciprocal_sum += 1/num
        
    return 1/reciprocal_sum

def harmonic_avg(lst):
    return len(lst)*harmonic_sum(lst)

nums = list((i for i in range(1,101)))

print(harmonic_sum(nums))
print(harmonic_avg(nums))