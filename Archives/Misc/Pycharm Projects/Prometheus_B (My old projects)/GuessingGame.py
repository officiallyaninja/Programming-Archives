import random
secret_number = random.randint(1, 10)
guess = ""

N = "3"

while guess != secret_number and round(float(N)) > 0:

    guess = float(input("Enter Guess(" + str(N) + " tries remaining):"))
    if guess < secret_number:
        print("higher")

    elif guess > secret_number:
        print("lower")




    N = int(N) - 1

if guess == secret_number:
    print("A winner is you!")

else:
    print("A failure is you \n"
          "correct answer is " + str(secret_number))

