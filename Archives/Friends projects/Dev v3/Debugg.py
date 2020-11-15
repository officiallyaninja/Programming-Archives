import sys
import json
import random
import copy

guess_count = n = num = op = Jnum = Jop = Jnum_check = Jop_check = 1  # Initialising Global Variables


def Jmap(licht):  # Jumbled Mapper

    Jumbled = random.sample(licht, len(licht))

    Mapping = {}

    for x in range(0, len(licht)):
        Mapping[licht[x]] = Jumbled[x]

    return(Mapping)


def Game(x):

    global guess_count
    global n
    global num
    global op
    global Jnum
    global Jop
    global Jnum_check
    global Jop_check

    if x is True:

        n = int(input("Enter range limit : "))
        num = list(range(0, n+1))

        op = ["+", "-", "*", "/"]  # op means operation

        Jnum = Jmap(num)
        Jop = Jmap(op)

        Jnum_check = list(Jnum.keys())  # Check to see remaining keys to find
        Jop_check = list(Jop.keys())

        guess_count = 3  # setting up for the initial guess

        """DEBUG"""
        print(n)
        print(num)
        print(op)
        print(Jnum)
        print(Jop)
        print(Jnum_check)
        print(Jop_check)
        print(guess_count)

    if x is False:

        with open('Save.json') as json_file:
            save = json.load(json_file)
            n = save['n']
            num = save['num']
            op = save['op']
            Jnum = save['Jnum']
            Jop = save['Jop']
            Jnum_check = save['Jnum_check']
            Jop_check = save['Jop_check']
            guess_count = save['guess_count']

        for key in Jnum.keys():
            key = str(key)

        """DEBUG"""
        print(n)
        print(num)
        print(op)
        print(Jnum)
        print(Jop)
        print(Jnum_check)
        print(Jop_check)
        print(guess_count)

    def Save():

        global guess_count
        global n
        global num
        global op
        global Jnum
        global Jop
        global Jnum_check
        global Jop_check

        """DEBUG"""
        print(n)
        print(num)
        print(op)
        print(Jnum)
        print(Jop)
        print(Jnum_check)
        print(Jop_check)
        print(guess_count)

        save = {}
        save['n'] = n
        save['num'] = num
        save['op'] = op
        save['Jnum'] = Jnum
        save['Jop'] = Jop
        save['Jnum_check'] = Jnum_check
        save['Jop_check'] = Jop_check
        save['guess_count'] = guess_count

        with open('Save.json', 'w') as outfile:
            json.dump(save, outfile)

        print("Saving and Exiting")
        sys.exit()

    def Check():

        global Jnum_check
        global Jop_check

        print("The numbers left to find out are", Jnum_check)
        print("The operations left to find out are", Jop_check)

        Choose()

    def Guess():

        global guess_count
        global Jnum
        global Jop
        global Jnum_check
        global Jop_check

        K = input("Enter Number / Operation (Jumbled) : ")
        V = input("Enter Guess : ")

        if K in Jop.keys():
            x = (V == Jop[K])
        else:
            x = False

        if x or (V == str(Jnum[int(K)])):
            print("Your Guess was right !")
            guess_count = 3
            temp = copy.deepcopy(Jnum_check)
            if K in list(map(str, temp)):
                Jnum_check.remove(int(K))
            elif K in Jop_check:
                Jop_check.remove(K)
            else:
                pass

            if len(Jop_check) == len(Jnum_check) == 0:
                print("You Won !")
                sys.exit()

        else:
            print("Guess Wrong")
            guess_count -= 1
            print("You have", guess_count, "consecutive chances left")
            if guess_count == 0:
                print("You Lose")
                sys.exit()

        Choose()

    def Operation():
        n1 = int(input("Enter number 1 : "))
        op = input("Enter operation : ")
        n2 = int(input("Enter number 2 : "))
        print("Output is", eval(str(Jnum[n1])+str(Jop[op])+str(Jnum[n2])))
        Choose()

    def Choose():

        with open("./Choose.txt") as f:
            print(f.read())

        INPUT = input("Enter option : ")

        if INPUT == "1":

            Operation()
        if INPUT == "2":

            Guess()
        if INPUT == "3":

            Check()
        if INPUT == "4":

            Save()

        else:
            print("Not a valid option")
            Choose()

    Choose()


def Intro_and_Rules():
    with open("./Intro_and_Rules.txt") as f:
        print(f.read())
        Menu()


def Menu():

    with open("./Menu.txt") as f:
        print(f.read())

    INPUT = input("Enter option : ")

    if INPUT == "1":
        Intro_and_Rules()
    if INPUT == "2":
        Game(True)  # New
    if INPUT == "3":
        Game(False)  # Load

    else:
        print("Not a valid option")
        Menu()


def Splash():                           # This is the banner text
    with open("./Splash.txt") as f:
        print(f.read())


Splash()
Menu()
