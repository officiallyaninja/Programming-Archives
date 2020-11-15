from Player_class import Player

while True:
    try:
        num_players = int(input("Enter number of players: "))
        break
    except ValueError:
        print("please enter a valid Number")

players = []



