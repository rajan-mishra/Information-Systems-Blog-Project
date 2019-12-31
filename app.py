from flask import Flask, render_template, session, flash, request, redirect
from flask_bootstrap import Bootstrap
import mysql.connector
import os

import mysql.connector

#con = mysql.connector.connect(
#user = "ardit700_student",
#password="ardit700_student",
#host = "108.167.140.122",
#database = "ardit700_pm1database"
#)

mydb = mysql.connector.connect(
	host = "localhost",
	user = "root",
	passwd = "password@1",
	database = "blogbackend"
	)

my_cursor = mydb.cursor()

#my_cursor.execute("CREATE DATABASE blogbackend")

#my_cursor.execute("CREATE TABLE users (user_id INTEGER(255) auto_increment PRIMARY KEY , first_name VARCHAR(255), last_name VARCHAR(255), username VARCHAR(255) UNIQUE, email VARCHAR(255) UNIQUE, password VARCHAR(255))")
#my_cursor.execute("CREATE TABLE blog (blog_id INTEGER(255) auto_increment PRIMARY KEY, title VARCHAR(255), author VARCHAR(255), body VARCHAR(255))")

mydb.commit()

app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = os.urandom(24)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login/', methods=['GET','POST'])
def login():
    return render_template('login.html')

@app.route('/blogs/<int:id>/')
def blogs(id):
    return render_template('blogs.html', blog_id = id)

@app.route('/register/', methods=['GET','POST'] )
def register():
    if request.method == 'POST':
        userDetails = request.form
        if userDetails['password'] != userDetails['confirm_password']:
            flash('Passwords do not match! Please enter same password in both the feilds.','danger')
            return render_template('register.html')
    return render_template('register.html')


@app.route('/editblogs/<int:id>/', methods=['GET','POST'])
def editblogs():
    return render_template('editblogs.html')

@app.route('/deleteblogs/<int:id>/')
def deleteblogs():
    return render_template('deleteblogs.html')

@app.route('/myblogs/')
def myblogs():
    return render_template('myblogs.html')

@app.route('/logout/')
def logout():
    return render_template('logout.html')

@app.route('/writeblog/', methods=['GET','POST'])
def writeblog():
    return render_template('writeblog.html')

if __name__ == '__main__' :
    app.run(debug = True)
