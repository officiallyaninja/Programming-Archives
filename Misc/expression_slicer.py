"""
README:
there are a lot of instances where this function returns 'None',
so make sure your program know what to do if it happens to return none at some point.

if also made the program a little less efficient than it could be, to make it more readable.
because it doesnt need to be that efficient, but i do want you to be able to understand how to use it properly.

also, the input 'expression' needs to be a string, and the output list has each element as a string as well.
"""

# expression should be a string


# takes input of an operator and 2 operands, returns [num1,operator,num2]
def expression_slicer(expression):
    expression = expression.replace(" ", "")  # removes all spacing from the expression

    if expression.lower() == "save":
        # heres where you put the save function
        return None
    if expression.lower() == "guess":
        # heres where you put the guess function
        return None
    if expression.lower() == "check":
        # heres where you put the check function
        return None

    # character set is the set of all valid characters in the expressions
    operators = ['+', '-', '*', '/']
    character_set = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    character_set.extend(operators)

    operator_count = 0  # tracks how many operators are there in the expression

    # makes sure the expression only contains valid characters, that is numbers and operators only
    for character in expression:
        if character in character_set:
            pass
        else:
            print('ERROR: INVALID CHARACTER/COMMAND DETECTED')
            return None

    # counts how many operators there are in the expression
    for operator in operators:
        operator_count += expression.count(operator)

    # checks to make sure there is only 1 operator
    if operator_count < 1:
        print('ERROR: NO OPERATOR DETECTED')
        return None
    elif operator_count > 1:
        print('ERROR: TOO MANY OPERATORS')
        return None

    elif operator_count == 1:
        pass

    # mathematically speaking, the error message below should be impossible to trigger.
    else:
        print('if you are seeing this error message, something has seriously fucked up')
        return None

    # following code figures out which operator is being used

    for operator in operators:
        if operator in expression:
            op = operator  # op is the operator in the expression
            break
    index = expression.index(op)  # this is the index value of the operator in the expression

    num1 = expression[0:index]  # num1 is the number before the operator
    num2 = expression[index + 1:]  # num2 is the number after the operator

    return [num1, op, num2]


while True:
    x = expression_slicer(input('blah: '))
    if x is not None:
        print(x)
