# Write a program to write your name,rollno and marks in a text file named ‘Marks.doc'


file = open('Marks.txt', 'W + b')

name = 'Name: ' + input('enter Name: ') + '\n'
roll = 'Roll No: ' + input('enter Roll No.: ') + '\n'
marks = 'Marks: ' + input('enter Marks: ') + '\n'

text = [name, roll, marks, '\n']

file.writelines(text)
