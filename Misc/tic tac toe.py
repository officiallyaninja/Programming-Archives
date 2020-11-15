
symbol = {
    -1: 'X',
    0: ' ',
    1: 'O'
}
row_coordinate = {
    'A': 0,
    'B': 1,
    'C': 2
}
board = [0 for i in range(0, 9)]
ERROR_MESSAGE = 'ERROR: Invalid Input'


def show_board() -> None:
    print('  1 2 3')  # shows horizontal coordinates of spaces
    # extra spaces is due to the offset caused by having letter coordinates on left.

    for i in range(0, 3):
        row = ''  # the row that is to eventually be printed
        for j in range(0, 3):
            index = (3*i) + j  # gets the index of the space on the board its supposed to be on
            row += symbol[board[index]] + '|'*(j != 3)

        letter = list(row_coordinate.keys())[i]  # to show vertical coordinate of spaces
        print(letter + ' ' + row)


def get_coordinate(player: int) -> tuple:   # to ensure coordinate is in format <letter><number>
    # eg: A1, B2, C2, A3 etc are valid

    while True:
        coordinate = input(f'Enter coordinate for {symbol[player]}: ')

        if len(coordinate) != 2:
            print(ERROR_MESSAGE)
            continue
        # now we know the input is only 2 letters
        if coordinate[0].upper() not in list(row_coordinate.keys()):
            print(ERROR_MESSAGE)
            continue
        if coordinate[1] not in ['1', '2', '3']:
            print(ERROR_MESSAGE)
            continue

        row_index = row_coordinate[coordinate[0].upper()]
        column_index = int(coordinate[1]) - 1

        # coordinate[0] will be A, B or C which will be converted to 0,1,2 respectively
        # coordinate[1] will be 1,2 or 3 which will be converted to 0,1,2 respectively

        return row_index, column_index


def mark(symbol_key: int, location: tuple) -> bool:  # returns true if space was available, false if already occupied
    if symbol_key not in [1, -1]:
        raise ValueError("Symbol Key should be 1 or -1 ya dummy")

    row, column = location  # location should contain (row, column)

    index = row*3 + column
    if board[index] != 0:
        return False

    board[index] = symbol_key
    return True


def check(a, b, c):  # a,b and c are in [-1,0,1]
    return int((board[a]+board[b]+board[c]) / 3)


def check_winner() -> int:  # returns 1, 0, or -1
    # ROWS
    for i in range(0, 8, 3):
        winner = check(i, i+1, i+2)
        if winner != 0:
            return winner
    # COLUMNS
    for i in range(0, 3):
        winner = check(i, i + 3, i + 6)
        if winner != 0:
            return winner
    # DIAGONALS
    winner = check(0, 4, 8)
    if winner != 0:
        return winner
    winner = check(2, 4, 6)
    if winner != 0:
        return winner

    return 0


player = -1  # player1 is symbol[-1] and player2 is symbol[1]
while True:  # while no one has won
    show_board()
    while True:  # loop continues forever until player chooses valid spot
        if mark(player, get_coordinate(player)) is True:
            break
        else:
            print('ERROR: space already occupied')

    winner = check_winner()
    if winner != 0:
        print(f'the winner is {symbol[winner]}!')
        break

    if 0 not in board:
        print('THE GAME IS A DRAW!')
        break

    player *= -1
show_board()  # shows the board one final time after someone wins or a draw happens

