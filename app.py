from flask import Flask, render_template, session, flash, request, redirect
from flask_bootstrap import Bootstrap
import pymysql.cursors
import os
from flask_ckeditor import CKEditor
import pymysql
from werkzeug.security import generate_password_hash

host = "localhost"
user = "root"
port = 3306
password = "password@1"
dbname = "blogbackend"

conn = pymysql.connect(host, user=user, port=port,
                       password=password, db=dbname)
cursor = conn.cursor()


app = Flask(__name__)
Bootstrap(app)
ckeditor = CKEditor(app)

app.config['SECRET_KEY'] = os.urandom(24)
@app.route('/')
def index():
    result_blog = cursor.execute("SELECT * FROM blog")
    if result_blog > 0:
        blogs = cursor.fetchall()
        return render_template('index.html', blogs=blogs)        
    return render_template('index.html',blogs=None)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login/', methods=['GET','POST'])
def login():
	if request.method == 'POST':
		userDetails = request.form
		username = userDetails['username']
		res_data=cursor.execute("SELECT * FROM users WHERE username = %s", ([username]))
		#res_data = cursor.fetchall()
		if res_data > 0:
			user = cursor.fetchone()
			if userDetails['password'] == user[5]:
				session['login'] = True
				session['firstName'] = user[1]
				session['lastName'] = user[2]
				flash('Welcome ' + session['firstName'] +'! You have been successfully logged in', 'success')
			else:
				#conn.close()
				flash('Password does not match', 'danger')
				return render_template('login.html')
		else:
			#conn.close()
			flash('Username does not exist', 'danger')
			return render_template('login.html')
		#conn.close()
		return redirect('/')
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
		sql ="INSERT INTO users (first_name, last_name, username, email, password) VALUES (%s,%s,%s,%s,%s) "
		cursor.execute(sql, (userDetails['first_name'], userDetails['last_name'],userDetails['username'], userDetails['email'], generate_password_hash(userDetails['password'])))
		conn.commit()
		flash('Registration successful! Please login.', 'success')
		#conn.close()
		return redirect('/login')
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
    if request.method == 'POST':
        blogpost = request.form
        title = blogpost['title']
        body = blogpost['body']
        author = session['firstName'] + ' ' + session['lastName']
        cursor = conn.cursor()
        sql = "INSERT INTO blog (title, author, body) VALUES (%s,%s,%s)"
        cursor.execute(sql, (title, author, body))
        conn.commit()
        #conn.close()

    return render_template('writeblog.html')

if __name__ == '__main__' :
    app.run(debug = True)
