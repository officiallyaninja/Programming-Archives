zodiac = {
    range(80, 110): "Aries",
    range(110, 141): "Taurus",
    range(141, 172): "Gemini",
    range(172, 204): "Cancer",
    range(204, 235): "Leo",
    range(235, 266): "Vigro",
    range(266, 296): "Libra",
    range(296, 326): "Scorpio",
    range(326, 356): "Saggitarius",
    range(356, 366) or range(1, 20): "Capricorn",
    range(20, 50): "Aquarius",
    range(50, 80): "Pisces"
}


while True:
    month = [None, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    while True:
        print("ZODIAC SIGN FINDER")
        date = input("Please enter the date to be checked in the format dd/mm/yyyy\n")

        # I decided not to use leap year functionality here since that would mess up with the ranges i specified
        try:
            number = sum(month[1:int(date[3:5])]) + int(date[0:2])
            if number == 0:
                print("Enter in the correct format please\n\n")
            else:
                break
        except:
            print("Enter in the correct format please\n\n")
            pass

    for key in zodiac:
        if number in key:
            print(zodiac[key])
            break
    else:
        print("Invalid date")

    confirm = input("Would you like to try again ? Y/N\n")
    if confirm == "Y" or confirm == "y":
        print()
        pass
    else:
        break
