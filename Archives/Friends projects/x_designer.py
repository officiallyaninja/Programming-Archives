import time

"""
# Optional Input method
inpute = eval("["+input("Enter width,multiplier,interpace,framerate : ")+"]")
inpute[0] = width
inpute[1] = multiplier
inpute[2] = interspace
inpute[3] = framerate

block = char(inputee[0])
space = 
filler
interspace

"""



setwidth = 11 # initializing value (odd) # CHANGABLE
multiplier = 1 # CHANGABLE
inter_space_num = 0 # CHANGABLE
sleep_timer = 0.05 # CHANGABLE

block = "♦" # CHANGABLE
space = " " # RISKY # CHANGABLE
filler = "=" # CHANGABLE
inter_space_char = " " # CHANGABLE

n = int((setwidth - 1)/2)
while True :
    count = 0
    licht = list(space * (2*n-1))
    for i in range(n,-(n-1),-1):
        licht[count]=block
        if i > 0 :
            for x in range (count+1,count + 2*(i-1)):
                licht[x]= filler
        if i <= 0 :
            for x in range (count + 2*(i-1),count) :
                licht[x]= filler
        licht[count + 2*(i-1) ] = block
        licht.append(inter_space_char * inter_space_num)
        licht = licht * multiplier
        for z in licht:
            print (z , end = "")
        print()
        count+=1
        licht = list(space * (2*n-1))
        time.sleep(sleep_timer) # CHANGABLE

