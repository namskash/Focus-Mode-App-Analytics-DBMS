import mysql.connector

mydb = mysql.connector.connect(
	host="localhost",
	user="namskash",
	password="abcd",
	database="focusModeDBMS"
)

mycursor = mydb.cursor(buffered=True)

f = open('create_tables.sql')

sql_as_string = f.read()

try:
	mycursor.execute(sql_as_string)
except:
	print("Error has occured")