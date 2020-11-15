import random
import time
# yes i know theres an inbuilt shuffle method but i didnt know that when I made the function.


moves = 0  # counts total number of expressions checked
shown = False  # text for the subtraction floor division note


def shuffle(deck):
    deck2 = []
    while len(deck) > 0:
        num = random.randint(0, len(deck) - 1)
        card = deck[num]
        deck2.append(card)
        deck.remove(card)

    return deck2


# jumbles the numbers (and operators)
op_list = shuffle(["+", "-", "/", "*"])
num_list = shuffle([1, 2, 3, 4, 5, 6, 7, 8, 9])
dic_num = {
    "1": num_list[0],
    "2": num_list[1],
    "3": num_list[2],
    "4": num_list[3],
    "5": num_list[4],
    "6": num_list[5],
    "7": num_list[6],
    "8": num_list[7],
    "9": num_list[8],
}
dic_op = {
    "+": op_list[0],
    "-": op_list[1],
    "/": op_list[2],
    "*": op_list[3]
}

# wall of tutorial and intro text

print("Welcome to the Number Jumbler!\n"
      "In this game all the operations(+ - * /) and numbers(1-9) have been mixed up and its your job to figure out which is which\n"
      "enter an expression in the form a∘b where a and b are single digit numbers and ∘ is an operation\n"
      "example: 5+3, 6*5, 2/8, 4-6 etc")
print('type "g" when you are ready to guess which number/operator is which')
# Main program

start_time = time.time()
while True:  # error handling while loop
    expression = input("enter expression: ")
    expression = expression.replace(" ", "")
    # first check is to make sure player doesnt want to guess
    if expression == 'guess':
        # this confirmation to make sure the players know they only have 1 chance to guess
        sure = input(" are you sure? (y/n). you only get 1 chance to guess: ")

        if sure.lower() == 'y':
            break
        else:
            print(" alright, come back when your ready")
            continue

    # general error handling

    if len(expression) < 3:
        print(" INVALID INPUT")
        continue
    if len(expression) > 3:
        # player probably tried something like 45+5 if they
        print(" INVALID INPUT(note: please only enter single digit operands)")
        continue                                                                # have a 4 char or longer string
    typed_num1, typed_op, typed_num2 = expression[0], expression[1], expression[2]
    # in case player tries % or // operators
    if typed_op not in dic_op.keys():
        print(" invalid operator only (+,-,*,/) are allowed")
        continue
    # catch-all error check at the end
    try:
        num1, op, num2 = dic_num[typed_num1], dic_op[typed_op], dic_num[typed_num2]
    except KeyError:
        print(" ERROR: invalid operator or number:")
        print(" Please input valid operators (+,-,*,/) and valid operands (1-9)")
        print(" note: 0 is not a valid operand")
        continue
    if num1 == num2:
        print(" ERROR: both numbers cannot be the same")
        continue

    else:
        # CALCULATING THE OUTPUT
        if op == '+':
            print(num1 + num2)
        elif op == '-':
            print(abs(num1 - num2))
        elif op == '*':
            print(num1 * num2)
        elif op == '/':
            print(num1 // num2)
        else:
            # no one should see this because the above error handling should catch all possible inputs that would lead here
            print("If you're seeing this message, I'm an idiot")
            continue
        if not shown:
            print("Note: the output will always be a positive integer, for all operations.")
            print('subtraction will give you the absolute difference and division performs floor division')
            shown = True
        moves += 1  # increments moves by 1 per each expression checked

# code for final guess

win = True  # setting variable to check if all guesses are correct

for num in dic_num.keys():  # loop runs through each number
    guess = ""
    while guess not in dic_num.keys():
        print("what value does the symbol", num, "have")
        guess = input("enter guess: ")  # player guesses what each number actually is
        if guess not in dic_num.keys():  # error handling for stupid typos
            print('INVALID GUESS')
            continue  # i think it's unnecessary to have this continue, but i have it anyway to make the code clearer
    if int(guess) != dic_num[num]:  # checks if guess is correct
        win = False
        # we need int(guess) and not just guess, because guess is a str and dic_num[num] is an int

    if int(guess) == dic_num[num]:
        print('CORRECT!')  # some feedback to let the player know they're right
    else:
        # shows correct answer to sate players curiosity
        print('THE CORRECT ANSWER IS: ', dic_num[num])

    # now we do the same but for each operation

for operator in dic_op.keys():  # loop runs through each operation
    guess = ""
    while guess not in dic_op.keys():
        print("what operation does the symbol", operator, "actually perform")
        # player guesses what each operation actually is
        guess = input("enter guess (type in +, -, * or /): ")
        if guess not in dic_op.keys():  # error handling for stupid typos
            print('INVALID GUESS')
            continue  # i think it's unnecessary to have this continue, but i have it anyway to make the code clearer
    if guess != dic_op[operator]:  # checks if guess is correct
        win = False

    if guess == dic_op[operator]:
        print('CORRECT!')  # some feedback to let the player know they're right
    else:
        # shows correct answer to sate players curiosity
        print('THE CORRECT ANSWER IS: ', dic_op[operator])

end_time = time.time()
time_taken = round(end_time - start_time, 2)
if win:
    print("HURRAY, you won! good job")
else:
    print("well, you didnt win. better luck next time.")
print("Expressions checked: ", moves)
print("time taken: ", time_taken)
