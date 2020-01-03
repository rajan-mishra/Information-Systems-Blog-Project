from flask import Flask, render_template, session, flash, request, redirect
from flask_bootstrap import Bootstrap
import os
from flask_ckeditor import CKEditor
import pymysql
from pymysql import cursors
from werkzeug.security import generate_password_hash, check_password_hash
import stripe


host = "localhost"
user = "root"
port = 3306
password = "password@1"
dbname = "blogbackend"

conn = pymysql.connect(host, user=user, port=port,
                       password=password, db=dbname, cursorclass=pymysql.cursors.DictCursor)
cursor = conn.cursor()

cursor1 = conn.cursor(cursors.DictCursor)

#cursor.execute("ALTER TABLE blog ADD email VARCHAR(250) NOT NULL")

app = Flask(__name__)
Bootstrap(app)
ckeditor = CKEditor(app)

app.config['SECRET_KEY'] = os.urandom(24)

#stripe_keys = {
#  'secret_key': os.environ['SECRET_KEY'],
#  'publishable_key': os.environ['PUBLISHABLE_KEY']
#}



@app.route('/')
def index():
    result_blog = cursor1.execute("SELECT * FROM blog")
    if result_blog > 0:
        blogs = cursor1.fetchall()
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
		res_data=cursor1.execute("SELECT * FROM users WHERE username = %s", ([username]))
		#res_data = cursor.fetchall()
		if res_data > 0:
			user = cursor1.fetchone()
			if check_password_hash(user['password'],userDetails['password']):
				session['login'] = True
				session['firstName'] = user['first_name']
				session['lastName'] = user['last_name']
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
    result_blog = cursor1.execute("SELECT * FROM blog WHERE blog_id = {}".format(id))
    if result_blog > 0 :
        blog = cursor1.fetchone()
        return render_template('blogs.html', blog= blog)

    return "Blog Not Found"

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
def editblogs(id):
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        cursor.execute("UPDATE blog SET title = %s, body = %s where blog_id = %s",(title, body, id))
        conn.commit()
        flash('Blog updated successfully', 'success')
        return redirect('/blogs/{}'.format(id))
    result_value = cursor.execute("SELECT * FROM blog WHERE blog_id = {}".format(id))
    if result_value > 0:
        blog = cursor.fetchone()
        blog_form = {}
        blog_form['title'] = blog['title']
        blog_form['body'] = blog['body']
        return render_template('editblogs.html', blog_form=blog_form)


@app.route('/deleteblogs/<int:id>/')
def deleteblogs(id):
	cursor.execute("DELETE FROM blog WHERE blog_id = {}".format(id))
	conn.commit()
	flash ("Your Blog has been successfully deleted", "success")
	return redirect ('/myblogs')

@app.route('/myblogs/')
def myblogs():
    author = session['firstName'] + ' ' + session['lastName']
    myblog = cursor1.execute("SELECT * FROM blog WHERE author = %s",[author])
    if myblog > 0:
        my_blogs = cursor1.fetchall()
        return render_template('myblogs.html',my_blogs=my_blogs)
    return render_template('my_blogs.html',my_blogs=None)

@app.route('/logout/')
def logout():
    session.clear()
    flash("You have been logged out", 'info')
    return redirect('/')


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
        flash("Successfully posted new blog", 'success')
        #conn.close()
        return redirect('/')

    return render_template('writeblog.html')

if __name__ == '__main__' :
    app.run(debug = True)
