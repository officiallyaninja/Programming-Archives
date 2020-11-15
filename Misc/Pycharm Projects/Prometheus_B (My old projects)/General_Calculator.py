
num_a = float(input("Enter a number:"))
operation = input("enter operator (+, -, *, /, %):")
num_b = float(input("Enter another number:"))

if operation == "+":
    print(num_a + num_b)

elif operation == "-":
    print(num_a - num_b)

elif operation == "*":
    print(num_a * num_b)

elif operation == "/":
    if num_b == 0:
        print("you cant divide by zero")

    else:
        print(num_a / num_b)

elif operation == "%":
    print(num_a % num_b)

else:
    print("Error Invalid Operator")







