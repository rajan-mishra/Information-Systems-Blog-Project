import mysql.connector

mydb = mysql.connector.connect(
	host = "localhost",
	user = "root",
	passwd = "Pythonproject123",
	database = "blogbackend"
	)

my_cursor = mydb.cursor()

#my_cursor.execute("CREATE DATABASE blogbackend")

my_cursor.execute("CREATE TABLE blog (blog_id INTEGER(255) PRIMARY KEY, title VARCHAR(255), author VARCHAR(255), body VARCHAR(255))")
