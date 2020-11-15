import random

sample_size = 10000000000
marks = 0
passes = 0
Number_of_tests = 0

for i in range(0, sample_size):
    for j in range(0, 120):
        answer = (random.randint(1, 5))
        if answer == 1:
            marks = marks + 4
        else:
            marks = marks - 1

    if marks >= 10:
        passes = passes + 1
    else:
        pass
    marks = 0
    Number_of_tests += 1
    print(str((passes/Number_of_tests)))

print("total passed = " + str(passes))
print("total failed = " + str(sample_size - passes))

print("pass percentage = " + str((passes / sample_size)))
