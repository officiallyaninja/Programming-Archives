import time

print("default 11 ,1 ,0 ,0.05 ")
inpute1 = eval("["+input("Enter width,multiplier,interpace,framerate : ")+"]")
# default 11,1,0,0.05

print()

print("default 9830 ,32 ,61 ,32 ")
inpute2 = eval("["+input("Enter Char_code for block,space,filler,interspace : ")+"]")
# default 9830,32,61,32

setwidth = inpute1[0] # initializing value (odd) # CHANGABLE # 17
multiplier = inpute1[1] # CHANGABLE # 1
inter_space_num = inpute1[2] # CHANGABLE # 0
sleep_timer = inpute1[3] # CHANGABLE # 0.05

block = chr(inpute2[0]) # CHANGABLE # "♦"
space = chr(inpute2[1]) # RISKY # CHANGABLE # " "
filler = chr(inpute2[2]) # CHANGABLE # "="
inter_space_char = chr(inpute2[3]) # CHANGABLE # " "

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

