def Menu():

    with open("./Menu.txt") as f:
        print(f.read())

    I = int(input("Enter option : "))

    if I == 1:
        # Intro & Rules Function
    if I == 2:
        # New Game Function
    if I == 3:
        # Load Game Function

    else:
        print("No option has been selected")
        Menu()


Menu()
