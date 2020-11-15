def decide(choice):
    print(choice)
    decision = input("\n")
    while True:
        if decision == "y":
            return True
            break
        elif decision == "n":
            return False
            break
        else:
            pass

