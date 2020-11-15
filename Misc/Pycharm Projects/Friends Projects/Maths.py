# Changing Date to Numbers
Month = int(input("Enter month of birth in numbers "))
Day = int(input("Enter day of birth "))
Year = int(input("Enter year of birth in yyyy form "))


def Date_to_numbers(Month, Day, Year):
    while True:
        if Month == 1 and Day in range(1, 31):
            return print(int(Day))
        if Month == 2:
            return print(int(31 + Day))
        if Month == 3:
            if Year / 4 == Year//4:
                return print(int(60 + Day))
            else:
                return print(int(59 + Day))
        if Month == 4:
            if Year / 4 == Year//4:
                return print(int(91 + Day))
            else:
                return print(int(90 + Day))
        if Month == 5:
            if Year / 4 == Year//4:
                return print(int(121 + Day))
            else:
                return print(int(120 + Day))
        if Month == 6:
            if Year / 4 == Year//4:
                return print(int(152 + Day))
            else:
                return print(int(151 + Day))
        if Month == 7:
            if Year / 4 == Year//4:
                return print(int(182 + Day))
            else:
                return print(int(181 + Day))
        if Month == 8:
            if Year / 4 == Year//4:
                return print(int(212 + Day))
            else:
                return print(int(211 + Day))
        if Month == 9:
            if Year / 4 == Year//4:
                return print(int(243 + Day))
            else:
                return print(int(242 + Day))
        if Month == 10:
            if Year / 4 == Year//4:
                return print(int(273 + Day))
            else:
                return print(int(272 + Day))
        if Month == 11:
            if Year / 4 == Year//4:
                return print(int(304 + Day))
            else:
                return print(int(303 + Day))
        if Month == 12:
            if Year / 4 == Year//4:
                return print(int(334 + Day))
            else:
                return print(int(333 + Day))


for Date_to_numbers(Month, Day, Year)in range(357, 366) or range(1, 19):
    zodiac = "a Capricorn"
for Date_to_numbers(Month, Day, Year)in range(20, 50):
    zodiac = "an Aquarius"
for Date_to_numbers(Month, Day, Year)in range(51, 82):
    zodiac = "a Pisces"
for Date_to_numbers(Month, Day, Year)in range(83, 113):
    zodiac = "an Aries"
for Date_to_numbers(Month, Day, Year)in range(114, 145):
    zodiac = "a Taurus"
for Date_to_numbers(Month, Day, Year)in range(146, 177):
    zodiac = "a Gemini"
for Date_to_numbers(Month, Day, Year)in range(178, 210):
    zodiac = "a Cancer"
for Date_to_numbers(Month, Day, Year)in range(211, 241):
    zodiac = "a Leo"
for Date_to_numbers(Month, Day, Year)in range(242, 273):
    zodiac = "a Virgo"
for Date_to_numbers(Month, Day, Year)in range(274, 304):
    zodiac = "a Libra"
for Date_to_numbers(Month, Day, Year)in range(305, 335):
    zodiac = "a Scorpio"
for Date_to_numbers(Month, Day, Year)in range(336, 356):
    zodiac = "a Sagittarius"
else:
    print("I need dates from the human calendar,ya freak")
print("You are " + zodiac)
