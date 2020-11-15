import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd='root',
    database='testdatabase'
)

mycursor = db.cursor()
cmd = 'INSERT INTO student VALUES(%s)'
print(cmd % 2)
print()