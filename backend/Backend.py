import mysql.connector

mydb = mysql.connector.connect(
	host = "localhost",
	user = "root",
	passwd = "Pythonproject123",
	database = "blogbackend"
	)

my_cursor = mydb.cursor()

#my_cursor.execute("CREATE DATABASE blogbackend")

my_cursor.execute("CREATE TABLE users (user_id INTEGER(255) auto_increment PRIMARY KEY , first_name VARCHAR(255), last_name VARCHAR(255), username VARCHAR(255) UNIQUE, email VARCHAR(255) UNIQUE, password VARCHAR(255))")
