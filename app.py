from flask import Flask, render_template, session, flash, request, redirect
from flask_bootstrap import Bootstrap
import mysql.connector
import os

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
        my_cursor = mysql.connection.cursor()
        my_cursor.execute("INSERT INTO user(first_name, last_name, username, email, password) "\
        "VALUES(%s,%s,%s,%s,%s)",(userDetails['first_name'], userDetails['last_name'], \
        userDetails['username'], userDetails['email'], userDetails['password']))
        mydb.connection.commit()
        my_cursor.close()
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
