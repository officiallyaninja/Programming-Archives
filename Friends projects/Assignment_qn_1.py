while True:
    name = str(input('Input Name:'))
    roll_no = str(input('Input Roll No:'))
    marks = str(input('Input Marks:'))
    file = open('Marks.txt', 'a+')
    file.write('Name:'+name+'   Roll no:'+roll_no+'     Marks:'+marks+'\n')
    file.close()
